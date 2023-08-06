#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCMC class for Bayes inference with emcee package using an Affine Invariant
Markov chain Monte Carlo (MCMC) Ensemble sampler [1].

1. Foreman-Mackey, D., Hogg, D.W., Lang, D. and Goodman, J., 2013. emcee: the
MCMC hammer. Publications of the Astronomical Society of the Pacific, 125(925),
p.306. https://emcee.readthedocs.io/en/stable/

Author: Farid Mohammadi, M.Sc.
E-Mail: farid.mohammadi@iws.uni-stuttgart.de
Department of Hydromechanics and Modelling of Hydrosystems (LH2)
Institute for Modelling Hydraulic and Environmental Systems (IWS), University
of Stuttgart, www.iws.uni-stuttgart.de/lh2/
Pfaffenwaldring 61
70569 Stuttgart

Created on Wed Jun 3 2020
"""

import os
import numpy as np
import emcee
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import multiprocessing
import scipy.stats as st
from scipy.linalg import cholesky as chol
import warnings
import shutil
os.environ["OMP_NUM_THREADS"] = "1"


class MCMC():
    """
    nwalkers = 20  # number of MCMC walkers
    nburn = 100 # "burn-in" period to let chains stabilize
    nsteps = 1000  # number of MCMC steps to take
    ntemps = 20
    """

    def __init__(self, BayesOpts, initsamples=None, nwalkers=100, nburn=200,
                 nsteps=100000, moves=None, multiprocessing=False,
                 verbose=False):

        self.BayesOpts      = BayesOpts
        self.initsamples    = initsamples
        self.nwalkers       = nwalkers
        self.nburn          = nburn
        self.nsteps         = nsteps
        self.moves          = moves
        self.mp             = multiprocessing
        self.verbose        = verbose

    def run_sampler(self, Observation, TotalSigma2):

        BayesObj = self.BayesOpts
        PCEModel = BayesObj.PCEModel
        Model = PCEModel.ModelObj
        Discrepancy = self.BayesOpts.Discrepancy
        nrCPUs = Model.nrCPUs
        priorDist = PCEModel.ExpDesign.JDist
        ndim = PCEModel.NofPa
        self.counter = 0
        OutputDir = (r'Outputs_Bayes_' + Model.Name + '_' + self.BayesOpts.Name)
        if not os.path.exists(OutputDir):
            os.makedirs(OutputDir)

        self.Observation = Observation
        self.TotalSigma2 = TotalSigma2

        # Set initial samples
        np.random.seed(0)
        if self.initsamples is None:
            try:
                initsamples = priorDist.sample(self.nwalkers).T
            except:
                # when aPCE selected - gaussian kernel distribution
                inputSamples = PCEModel.ExpDesign.raw_data.T
                random_indices = np.random.choice(len(inputSamples),
                                                  size=self.nwalkers,
                                                  replace=False)
                initsamples = inputSamples[random_indices]

        else:
            if self.initsamples.ndim == 1:
                # When MAL is given.
                theta = self.initsamples
                initsamples = [theta + 1e-1*np.multiply(np.random.randn(ndim),
                                                        theta) for i in
                               range(self.nwalkers)]
            else:
                # Pick samples based on a uniform dist between min and max of
                # each dim
                initsamples = np.zeros((self.nwalkers, ndim))
                BoundTuples = []
                for idxDim in range(ndim):
                    lower = np.min(self.initsamples[:, idxDim])
                    upper = np.max(self.initsamples[:, idxDim])
                    BoundTuples.append((lower, upper))
                    dist = st.uniform(loc=lower, scale=upper-lower)
                    initsamples[:, idxDim] = dist.rvs(size=self.nwalkers)

                # Update lower and upper
                PCEModel.ExpDesign.BoundTuples = BoundTuples

        # Check if sigma^2 needs to be inferred
        if Discrepancy.optSigma != 'B':
            sigma2Samples = Discrepancy.get_Sample(self.nwalkers)

            # Update initsamples
            initsamples = np.hstack((initsamples, sigma2Samples))

            # Update ndim
            ndim = initsamples.shape[1]

            # Update BoundTuples
            PCEModel.ExpDesign.BoundTuples += Discrepancy.ExpDesign.BoundTuples

        print("\n>>>> Bayesian inference with MCMC for "
              f"{self.BayesOpts.Name} started. <<<<<<")

        # Set up the backend
        filename = OutputDir+"/emcee_sampler.h5"
        backend = emcee.backends.HDFBackend(filename)
        # Clear the backend in case the file already exists
        backend.reset(self.nwalkers, ndim)

        # Define emcee sampler
        # Here we'll set up the computation. emcee combines multiple "walkers",
        # each of which is its own MCMC chain. The number of trace results will
        # be nwalkers * nsteps
        if self.mp:
            # Run in parallel
            if nrCPUs is None:
                nrCPUs = multiprocessing.cpu_count()

            with multiprocessing.Pool(nrCPUs) as pool:
                sampler = emcee.EnsembleSampler(self.nwalkers, ndim,
                                                self.log_posterior,
                                                moves=self.moves,
                                                pool=pool, backend=backend)

                # Check if a burn-in phase is needed!
                if self.initsamples is None:
                    # Burn-in
                    print("\n Burn-in period is starting:")
                    pos = sampler.run_mcmc(initsamples,
                                           self.nburn,
                                           progress=True)

                    # Reset sampler
                    sampler.reset()
                    pos = pos.coords
                else:
                    pos = initsamples

                # Production run
                print("\n Production run is starting:")
                pos, prob, state = sampler.run_mcmc(pos,
                                                    self.nsteps,
                                                    progress=True)

        else:
            # Run in series and monitor the convergence
            sampler = emcee.EnsembleSampler(self.nwalkers, ndim,
                                            self.log_posterior,
                                            moves=self.moves,
                                            backend=backend,
                                            vectorize=True)

            # Check if a burn-in phase is needed!
            if self.initsamples is None:
                # Burn-in
                print("\n Burn-in period is starting:")
                pos = sampler.run_mcmc(initsamples, self.nburn, progress=True)

                # Reset sampler
                sampler.reset()
                pos = pos.coords
            else:
                pos = initsamples

            # Production run
            print("\n Production run is starting:")

            # Track how the average autocorrelation time estimate changes
            autocorrIdx = 0
            autocorr = np.empty(self.nsteps)
            tauold = np.inf
            autocorreverynsteps = 50

            # sample step by step using the generator sampler.sample
            for sample in sampler.sample(pos,
                                         iterations=self.nsteps,
                                         tune=True,
                                         progress=True):

                # only check convergence every autocorreverynsteps steps
                if sampler.iteration % autocorreverynsteps:
                    continue

                # Train model discrepancy/error
                if hasattr(BayesObj, 'errorModel') and BayesObj.errorModel \
                   and not sampler.iteration % 3 * autocorreverynsteps:
                    try:
                        self.errorMetaModel = self.train_errorModel(sampler)
                    except:
                        pass

                # Print the current mean acceptance fraction
                if self.verbose:
                    print("\nStep: {}".format(sampler.iteration))
                    acc_fr = np.mean(sampler.acceptance_fraction)
                    print(f"Mean acceptance fraction: {acc_fr:.3f}")

                # compute the autocorrelation time so far
                # using tol=0 means that we'll always get an estimate even if
                # it isn't trustworthy
                tau = sampler.get_autocorr_time(tol=0)
                # average over walkers
                autocorr[autocorrIdx] = np.nanmean(tau)
                autocorrIdx += 1

                # output current autocorrelation estimate
                if self.verbose:
                    print(f"Mean autocorr time estimate: {np.nanmean(tau):.3f}")
                    list_gr = np.round(self.gelman_rubin(sampler.chain), 3)
                    print("Gelman-Rubin Test*: ", list_gr)

                # check convergence
                converged = np.all(tau*autocorreverynsteps < sampler.iteration)
                converged &= np.all(np.abs(tauold - tau) / tau < 0.01)
                converged &= np.all(self.gelman_rubin(sampler.chain) < 1.1)

                if converged:
                    break
                tauold = tau

        # Posterior diagnostics
        try:
            tau = sampler.get_autocorr_time(tol=0)
        except emcee.autocorr.AutocorrError:
            tau = 5

        if all(np.isnan(tau)):
            tau = 5

        burnin = int(2*np.nanmax(tau))
        thin = int(0.5*np.nanmin(tau)) if int(0.5*np.nanmin(tau)) != 0 else 1
        finalsamples = sampler.get_chain(discard=burnin, flat=True, thin=thin)
        acc_fr = np.nanmean(sampler.acceptance_fraction)
        list_gr = np.round(self.gelman_rubin(sampler.chain[:, burnin:]), 3)

        # Print summary
        print('\n')
        print('-'*15 + 'Posterior diagnostics' + '-'*15)
        print(f"mean auto-correlation time: {np.nanmean(tau):.3f}")
        print(f"thin: {thin}")
        print(f"burn-in: {burnin}")
        print(f"flat chain shape: {finalsamples.shape}")
        print(f"Mean acceptance fraction: {acc_fr:.3f}")
        print("Gelman-Rubin Test*: ", list_gr)

        print("\n* This value must lay between 0.234 and 0.5.")
        print("* These values must be smaller than 1.1.")
        print('-'*50)

        print(f"\n>>>> Bayesian inference with MCMC for {self.BayesOpts.Name} "
              "successfully completed. <<<<<<\n")

        # Extract parameter names and their prior ranges
        par_names = PCEModel.ExpDesign.par_names

        if Discrepancy.optSigma != 'B':
            for i in range(len(Discrepancy.InputDisc.Marginals)):
                par_names.append(Discrepancy.InputDisc.Marginals[i].Name)

        params_range = PCEModel.ExpDesign.BoundTuples

        # Plot traces
        if self.verbose and self.nsteps < 10000:
            pdf = PdfPages(OutputDir+'/traceplots.pdf')
            fig = plt.figure()
            for parIdx in range(ndim):
                # Set up the axes with gridspec
                fig = plt.figure()
                grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
                main_ax = fig.add_subplot(grid[:-1, :3])
                y_hist = fig.add_subplot(grid[:-1, -1], xticklabels=[],
                                         sharey=main_ax)

                for i in range(self.nwalkers):
                    samples = sampler.chain[i, :, parIdx]
                    main_ax.plot(samples, '-')

                    # histogram on the attached axes
                    y_hist.hist(samples[burnin:], 40, histtype='stepfilled',
                                orientation='horizontal', color='gray')

                main_ax.set_ylim(params_range[parIdx])
                main_ax.set_title('traceplot for ' + par_names[parIdx])
                main_ax.set_xlabel('step number')

                # save the current figure
                pdf.savefig(fig, bbox_inches='tight')

                # Destroy the current plot
                plt.clf()

            pdf.close()

        # plot development of autocorrelation estimate
        if not self.mp:
            fig1 = plt.figure()
            steps = autocorreverynsteps*np.arange(1, autocorrIdx+1)
            taus = autocorr[:autocorrIdx]
            plt.plot(steps, steps / autocorreverynsteps, "--k")
            plt.plot(steps, taus)
            plt.xlim(0, steps.max())
            plt.ylim(0, np.nanmax(taus)+0.1*(np.nanmax(taus)-np.nanmin(taus)))
            plt.xlabel("number of steps")
            plt.ylabel(r"mean $\hat{\tau}$")
            fig1.savefig(f"{OutputDir}/autocorrelation_time.pdf",
                         bbox_inches='tight')

        # logml_dict = self.Marginal_llk_emcee(sampler, self.nburn, logp=None,
        # maxiter=5000)
        # print('\nThe Bridge Sampling Estimation is "
        #       f"{logml_dict['logml']:.5f}.')

        # # Posterior-based expectation of posterior probablity
        # postExpPostLikelihoods = np.mean(sampler.get_log_prob(flat=True)
        # [self.nburn*self.nwalkers:])

        # # Posterior-based expectation of prior densities
        # postExpPrior = np.mean(self.log_prior(emcee_trace.T))

        # # Posterior-based expectation of likelihoods
        # postExpLikelihoods_emcee = postExpPostLikelihoods - postExpPrior

        # # Calculate Kullback-Leibler Divergence
        # KLD_emcee = postExpLikelihoods_emcee - logml_dict['logml']
        # print("Kullback-Leibler divergence: %.5f"%KLD_emcee)

        # # Information Entropy based on Entropy paper Eq. 38
        # infEntropy_emcee = logml_dict['logml'] - postExpPrior -
        #                    postExpLikelihoods_emcee
        # print("Information Entropy: %.5f" %infEntropy_emcee)

        Posterior_df = pd.DataFrame(finalsamples, columns=par_names)

        return Posterior_df

    def log_prior(self, theta):

        PCEModel = self.BayesOpts.PCEModel
        Discrepancy = self.BayesOpts.Discrepancy
        nSigma2 = len(Discrepancy.ExpDesign.BoundTuples) if Discrepancy.optSigma != 'B' else -len(theta)
        priorDist = PCEModel.ExpDesign.priorSpace
        params_range = PCEModel.ExpDesign.BoundTuples
        ndimTheta = theta.ndim
        theta = theta if ndimTheta != 1 else theta.reshape((1,-1))
        nsamples = theta.shape[0]
        logprior = -np.inf*np.ones(nsamples)

        for i in range(nsamples):
            # Check if the sample is within the parameters' range
            if self.check_ranges(theta[i], params_range):
                # Check if all dists are uniform, if yes priors are equal.
                if all(PCEModel.input_obj.Marginals[i].DistType == 'uniform' for i in \
                   range(PCEModel.NofPa)):
                    logprior[i] = 0.0
                else:
                    logprior[i] = np.log(priorDist.pdf(theta[i,:-nSigma2].T))

                # Check if bias term needs to be inferred
                if Discrepancy.optSigma != 'B':
                    if self.check_ranges(theta[i,-nSigma2:], 
                                         Discrepancy.ExpDesign.BoundTuples):
                        if all('unif' in Discrepancy.ExpDesign.InputObj.Marginals[i].DistType  for i in \
                            range(Discrepancy.ExpDesign.ndim)):
                            logprior[i] = 0.0
                        else:
                            logprior[i] += np.log(Discrepancy.ExpDesign.priorSpace.pdf(theta[i,-nSigma2:]))

        if nsamples == 1:
            return logprior[0]
        else:
            return logprior

    def log_likelihood(self, theta):

        BayesOpts = self.BayesOpts
        PCEModel = BayesOpts.PCEModel
        Discrepancy = self.BayesOpts.Discrepancy
        if Discrepancy.optSigma != 'B':
            nSigma2 = len(Discrepancy.ExpDesign.BoundTuples)
        else:
            nSigma2 = -len(theta)
        # Check if bias term needs to be inferred
        if Discrepancy.optSigma != 'B':
            Sigma2 = theta[:, -nSigma2:]
            theta = theta[:, :-nSigma2]
        else:
            Sigma2 = None
        ndimTheta = theta.ndim
        theta = theta if ndimTheta != 1 else theta.reshape((1, -1))

        # Evaluate Model/PCEModel at theta
        meanPCEPriorPred, BayesOpts._stdPCEPriorPred = self.eval_model(theta)

        # Surrogate model's error using RMSE of test data
        surrError = PCEModel.RMSE if hasattr(PCEModel, 'RMSE') else None

        # Likelihood
        return BayesOpts.normpdf(meanPCEPriorPred, self.Observation,
                                 self.TotalSigma2, Sigma2, std=surrError)

    def log_posterior(self, theta):
        """
        Computes the posterior likelihood for the given parameterset.

        Parameters
        ----------
        theta : TYPE
            DESCRIPTION.
        Observation : TYPE
            DESCRIPTION.
        TotalSigma2 : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        ndimTheta = theta.ndim
        nsamples = 1 if ndimTheta == 1 else theta.shape[0]

        if nsamples == 1:
            if self.log_prior(theta) == -np.inf:
                return -np.inf
            else:
                # Compute log prior
                log_prior = self.log_prior(theta)
                # Compute log Likelihood
                log_likelihood = self.log_likelihood(theta)

                return log_prior + log_likelihood
        else:
            # Compute log prior
            log_prior = self.log_prior(theta)

            # Initialize log_likelihood
            log_likelihood = -np.inf*np.ones(nsamples)

            # find the indices for -inf sets
            nonInfIdx = np.where(log_prior != -np.inf)[0]

            # Compute loLikelihoods
            if nonInfIdx.size != 0:
                log_likelihood[nonInfIdx] = self.log_likelihood(theta[nonInfIdx])

            return log_prior + log_likelihood

    def eval_model(self, theta):

        BayesObj = self.BayesOpts
        PCEModel = BayesObj.PCEModel
        Model = PCEModel.ModelObj

        if BayesObj.emulator:
            # Evaluate the PCEModel
            meanPred, stdPred = PCEModel.eval_metamodel(samples=theta,
                                                        name=BayesObj.Name)
        else:
            # Evaluate the origModel

            # Prepare the function
            meanPred, stdPred = dict(), dict()
            OutputNames = Model.Output.Names

            try:
                Filename = Model.pyFile
                Function = getattr(__import__(Filename), Filename)

                # Run function for theta
                modelOuts = Function(theta.reshape(1, -1))
            except:
                modelOuts, _ = Model.run_model_parallel(theta[0],
                                                        prevRun_No=self.counter,
                                                        keyString='_MCMC',
                                                        mp=False)
            # Save outputs in respective dicts
            for varIdx, var in enumerate(OutputNames):
                meanPred[var] = modelOuts[var]
                stdPred[var] = np.zeros((meanPred[var].shape))

            # Remove the folder
            shutil.rmtree(Model.Name + '_MCMC_' + str(self.counter+1))

            # Add one to the counter
            self.counter += 1

        if hasattr(self, 'errorMetaModel') and BayesObj.errorModel:
            meanPred, stdPred = self.errorMetaModel.eval_model_error(
                BayesObj.BiasInputs, meanPred)

        return meanPred, stdPred

    def train_errorModel(self, sampler):
        BayesObj = self.BayesOpts
        PCEModel = BayesObj.PCEModel

        # Prepare the poster samples
        try:
            tau = sampler.get_autocorr_time(tol=0)
        except emcee.autocorr.AutocorrError:
            tau = 5

        if all(np.isnan(tau)):
            tau = 5

        burnin = int(2*np.nanmax(tau))
        thin = int(0.5*np.nanmin(tau)) if int(0.5*np.nanmin(tau)) != 0 else 1
        finalsamples = sampler.get_chain(discard=burnin, flat=True, thin=thin)
        Posterior_df = finalsamples[:, :PCEModel.NofPa]

        # Select posterior mean as MAP
        MAP_theta = Posterior_df.mean(axis=0).reshape((1, PCEModel.NofPa))
        # MAP_theta = st.mode(Posterior_df,axis=0)[0]

        # Evaluate the (meta-)model at the MAP
        y_MAP, y_std_MAP = PCEModel.eval_metamodel(samples=MAP_theta,
                                                   name=BayesObj.Name)

        # Train a GPR meta-model using MAP
        errorMetaModel = PCEModel.create_model_error(BayesObj.BiasInputs,
                                                     y_MAP, Name='Calib')
        return errorMetaModel

    def Marginal_llk_emcee(self, sampler, nburn=None, logp=None, maxiter=1000):
        """
        The Bridge Sampling Estimator of the Marginal Likelihood.

        Parameters
        ----------
        mtrace : MultiTrace, result of MCMC run
        model : PyMC Model
            Optional model. Default None, taken from context.
        logp : Model Log-probability function, read from the model by default
        maxiter : Maximum number of iterations

        Returns
        -------
        marg_llk : Estimated Marginal log-Likelihood.
        """
        r0, tol1, tol2 = 0.5, 1e-10, 1e-4
        
        if logp is None:
            logp = sampler.log_prob_fn
    
        
        # Split the samples into two parts  
        # Use the first 50% for fiting the proposal distribution and the second 50% 
        # in the iterative scheme.
        if nburn is None:
            mtrace = sampler.chain
        else:
            mtrace = sampler.chain[:, nburn:, :]
            
        nchain, len_trace, nrofVars = mtrace.shape
        
        N1_ = len_trace // 2
        N1 = N1_*nchain
        N2 = len_trace*nchain - N1
        
        samples_4_fit = np.zeros((nrofVars, N1))
        samples_4_iter = np.zeros((nrofVars, N2))
        effective_n = np.zeros((nrofVars))
    
        # matrix with already transformed samples
        for var in range(nrofVars):
            
            # for fitting the proposal
            x = mtrace[:,:N1_,var]
            
            samples_4_fit[var, :] = x.flatten()
            # for the iterative scheme
            x2 = mtrace[:,N1_:,var]
            samples_4_iter[var, :] = x2.flatten()
    
            # effective sample size of samples_4_iter, scalar 
            #(https://github.com/jwalton3141/jwalton3141.github.io/blob/master/assets/posts/ESS/rwmh.py)
            effective_n[var] = self.my_ESS(x2)
    
        # median effective sample size (scalar)
        neff = np.median(effective_n)
        
        # get mean & covariance matrix and generate samples from proposal
        m = np.mean(samples_4_fit, axis=1)
        V = np.cov(samples_4_fit)
        L = chol(V, lower=True)
    
        # Draw N2 samples from the proposal distribution
        gen_samples = m[:, None] + np.dot(L, st.norm.rvs(0, 1, 
                                             size=samples_4_iter.shape))
    
        # Evaluate proposal distribution for posterior & generated samples
        q12 = st.multivariate_normal.logpdf(samples_4_iter.T, m, V)
        q22 = st.multivariate_normal.logpdf(gen_samples.T, m, V)
    
        # Evaluate unnormalized posterior for posterior & generated samples
        q11 = logp(samples_4_iter.T)
        q21 = logp(gen_samples.T)
        
        # Run iterative scheme:
        tmp = self.iterative_scheme(N1, N2, q11, q12, q21, q22, r0, neff, tol1, maxiter, 'r')
        if ~np.isfinite(tmp['logml']):
            warnings.warn("""logml could not be estimated within maxiter, rerunning with 
                          adjusted starting value. Estimate might be more variable than usual.""")
            # use geometric mean as starting value
            r0_2 = np.sqrt(tmp['r_vals'][-2]*tmp['r_vals'][-1])
            tmp = self.iterative_scheme(q11, q12, q21, q22, r0_2, neff, tol2, maxiter, 'logml')
    
        return dict(logml = tmp['logml'], niter = tmp['niter'], method = "normal", 
                    q11 = q11, q12 = q12, q21 = q21, q22 = q22)
    
    
    def iterative_scheme(self,N1, N2, q11, q12, q21, q22, r0, neff, tol, maxiter, criterion):
        """
        Iterative scheme as proposed in Meng and Wong (1996) to estimate the marginal likelihood    
    
        Parameters
        ----------
        N1 : TYPE
            DESCRIPTION.
        N2 : TYPE
            DESCRIPTION.
        q11 : TYPE
            DESCRIPTION.
        q12 : TYPE
            DESCRIPTION.
        q21 : TYPE
            DESCRIPTION.
        q22 : TYPE
            DESCRIPTION.
        r0 : TYPE
            DESCRIPTION.
        neff : TYPE
            DESCRIPTION.
        tol : TYPE
            DESCRIPTION.
        maxiter : TYPE
            DESCRIPTION.
        criterion : TYPE
            DESCRIPTION.
    
        Returns
        -------
        TYPE
            DESCRIPTION.
    
        """
        l1 = q11 - q12
        l2 = q21 - q22
        lstar = np.median(l1) # To increase numerical stability, 
                              # subtracting the median of l1 from l1 & l2 later
        s1 = neff/(neff + N2)
        s2 = N2/(neff + N2)
        r = r0
        r_vals = [r]
        logml = np.log(r) + lstar
        criterion_val = 1 + tol
    
        i = 0
        while (i <= maxiter) & (criterion_val > tol):
            rold = r
            logmlold = logml
            numi = np.exp(l2 - lstar)/(s1 * np.exp(l2 - lstar) + s2 * r)
            deni = 1/(s1 * np.exp(l1 - lstar) + s2 * r)
            if np.sum(~np.isfinite(numi))+np.sum(~np.isfinite(deni)) > 0:
                warnings.warn("""Infinite value in iterative scheme, returning NaN. 
                Try rerunning with more samples.""")
            r = (N1/N2) * np.sum(numi)/np.sum(deni)
            r_vals.append(r)
            logml = np.log(r) + lstar
            i += 1
            if criterion=='r':
                criterion_val = np.abs((r - rold)/r)
            elif criterion=='logml':
                criterion_val = np.abs((logml - logmlold)/logml)
    
        if i >= maxiter:
            return dict(logml = np.NaN, niter = i, r_vals = np.asarray(r_vals))
        else:
            return dict(logml = logml, niter = i)
        
    
    def my_gelman_rubin(self, x):
        """ Estimate the marginal posterior variance. Vectorised implementation. """
        m_chains, n_iters = x.shape
    
        # Calculate between-chain variance
        B_over_n = ((np.mean(x, axis=1) - np.mean(x))**2).sum() / (m_chains - 1)
    
        # Calculate within-chain variances
        W = ((x - x.mean(axis=1, keepdims=True))**2).sum() / (m_chains*(n_iters - 1))
    
        # (over) estimate of variance
        s2 = W * (n_iters - 1) / n_iters + B_over_n
        
        return s2
    
    def my_ESS(self, x):
        """ 
        Compute the effective sample size of estimand of interest. 
        Vectorised implementation. 
        """
        m_chains, n_iters = x.shape
    
        variogram = lambda t: ((x[:, t:] - x[:, :(n_iters - t)])**2).sum() / (m_chains * (n_iters - t))
    
        post_var = self.my_gelman_rubin(x)
    
        t = 1
        rho = np.ones(n_iters)
        negative_autocorr = False
    
        # Iterate until the sum of consecutive estimates of autocorrelation is negative
        while not negative_autocorr and (t < n_iters):
            rho[t] = 1 - variogram(t) / (2 * post_var)
    
            if not t % 2:
                negative_autocorr = sum(rho[t-1:t+1]) < 0
    
            t += 1
        
        return int(m_chains*n_iters / (1 + 2*rho[1:t].sum()))
    
    def check_ranges(self, theta, ranges):
        """
        This function checks if theta lies in the given ranges

        Parameters
        ----------
        theta : numpy array
            Proposed parameter set.
        ranges : TYPE
            DESCRIPTION.

        Returns
        -------
        c : bool
            If it lies in the given range, it return True else False.

        """
        c = True
        #sigma = theta[-1]
        # traverse in the list1 
        for i, bounds in enumerate(ranges): 
            x = theta[i]
            # condition check
            if x < bounds[0] or x > bounds[1]: #or sigma < 0:
                c = False
                return c
        return c
    
    def gelman_rubin(self, chain):
        """
        The potential scale reduction factor (PSRF) defined by the variance within 
        one chain, W, with the variance between chains B. 
        Both variances are combined in a weighted sum to obtain 
        an estimate of the variance of a parameter θ.The square root of the ratio 
        of this estimates variance to the within chain variance is called the 
        potential scale reduction. 
        For a well converged chain it should approach 1. Values greater than 
        typically 1.1 indicate that the chains have not yet fully converged.
        
        Source: http://joergdietrich.github.io/emcee-convergence.html
        
        Parameters
        ----------
        chain : array (nWalkers, nSteps, nparams)
            DESCRIPTION.

        Returns
        -------
        R_hat : float
            The Gelman-Robin values.

        """
        ssq = np.var(chain, axis=1, ddof=1)
        W = np.mean(ssq, axis=0)
        θb = np.mean(chain, axis=1)
        θbb = np.mean(θb, axis=0)
        m = chain.shape[0]
        n = chain.shape[1]
        B = n / (m - 1) * np.sum((θbb - θb)**2, axis=0)
        var_θ = (n - 1) / n * W + B / n
        R_hat = np.sqrt(var_θ / W)
        
        return R_hat