#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Author: Farid Mohammadi, M.Sc.
E-Mail: farid.mohammadi@iws.uni-stuttgart.de
Department of Hydromechanics and Modelling of Hydrosystems (LH2)
Institute for Modelling Hydraulic and Environmental Systems (IWS), University
of Stuttgart, www.iws.uni-stuttgart.de/lh2/
Pfaffenwaldring 61
70569 Stuttgart

Created on Sat Aug 24 2019
"""
import numpy as np
import os
import copy
import pandas as pd
from tqdm import tqdm
from scipy import stats
import scipy.linalg as spla

import seaborn as sns
import corner
import h5py
import gc
from joblib import Parallel, delayed
from scipy.stats import multivariate_normal
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics.pairwise import rbf_kernel
from sklearn import preprocessing
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt
SIZE = 30
plt.rc('figure', figsize=(24, 16))
plt.rc('font', family='serif', serif='Arial')
plt.rc('font', size=SIZE)
plt.rc('text', usetex=True)
plt.rc('axes', linewidth=3)
plt.rc('axes', grid=True)
plt.rc('grid', linestyle="-")
plt.rc('axes', titlesize=SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SIZE)    # legend fontsize
plt.rc('figure', titlesize=SIZE)  # fontsize of the figure title


from .discrepancy import Discrepancy
from .mcmc import MCMC
from bayesvalidrox.surrogate_models.exp_designs import ExpDesigns


class BayesInference:
    def __init__(self, PCEModel):
        self.PCEModel = PCEModel
        self.Name = 'Calib'
        self.SamplingMethod = 'rejection'
        self.MAP = 'Mean'
        self.PCEMeans = {}
        self.PCEStd = {}
        self.Discrepancy = None
        self.ReqOutputType = None
        self.NrofSamples = 500000
        self.Samples = None
        self.MCMCnSteps = None
        self.MCMCnwalkers = None
        self.MCMCinitSamples = None
        self.MCMCmoves = None
        self.MCMCverbose = False
        self.ModelOutputs = []

        self.perturbedData = []
        self.MeasuredData = None
        self.MeasurementError = []
        self.selectedIndices = None

        self.logLikelihoods = []
        self.logBME = []
        self.KLD = []
        self.infEntropy = []
        self.MAPorigModel = []
        self.MAPpceModelMean = []
        self.MAPpceModelStd = []
        self.logTOMBME = []
        self.Posterior_df = {}
        self.PCEPriorPred = {}

        self.PlotPostPred = True
        self.PlotMAPPred = False
        self.emulator = True
        self.Bootstrap = False
        self.BayesLOOCV = False
        self.BootstrapItrNr = 1
        self.BootstrapNoise = 0.05
        self.MultiProcessMCMC = None
        self.Corner_title_fmt = '.3f'

    # -------------------------------------------------------------------------
    def _logpdf(self, x, mean, cov):
        n = len(mean)
        L = spla.cholesky(cov, lower=True)
        beta = np.sum(np.log(np.diag(L)))
        dev = x - mean
        alpha = dev.dot(spla.cho_solve((L, True), dev))
        return -0.5 * alpha - beta - n / 2. * np.log(2 * np.pi)

    # -------------------------------------------------------------------------
    def get_Sample(self):

        PCEModel = self.PCEModel

        NrSamples = self.NrofSamples

        self.Samples = PCEModel.ExpDesign.generate_samples(NrSamples, 'random')

        return self.Samples

    # -------------------------------------------------------------------------
    def eval_Model(self, Samples=None, key='MAP'):
        """
        Evaluate Forward Model

        """
        index = self.PCEModel.index
        Model = self.PCEModel.ModelObj

        if Samples is None:
            Samples = self.get_Sample()
            self.Samples = Samples
        else:
            Samples = Samples
            self.NrofSamples = len(Samples)

        ModelOutputs, _ = Model.run_model_parallel(Samples,
                                                   keyString=key+self.Name)

        if index is not None:
            if self.Name == 'Valid':
                self.ModelOutputs = {key: ModelOutputs[key][index:] for key in [list(ModelOutputs.keys())[0]]}
                Outputs = {key: ModelOutputs[key][:,index:] for key in Model.Output.Names}
            else:
                self.ModelOutputs = {key: ModelOutputs[key][:index] for key in [list(ModelOutputs.keys())[0]]}
                Outputs = {key: ModelOutputs[key][:,:index] for key in Model.Output.Names}
            self.ModelOutputs.update(Outputs)
        else:
            self.ModelOutputs = ModelOutputs

        # Clean up
        # Zip the subdirectories
        try:
            dir_name = f'{Model.name}MAP{self.Name}'
            key = dir_name + '_'
            Model.zip_subdirs(dir_name, key)
        except:
            pass

        return self.ModelOutputs

    # -------------------------------------------------------------------------
    def RBF_kernel(self, X, Sigma2):
        """
        Isotropic squared exponential kernel.

        Higher l values lead to smoother functions and therefore to coarser
        approximations of the training data. Lower l values make functions
        more wiggly with wide uncertainty regions between training data points.

        sigma_f controls the marginal variance of b(x)

        Parameters
        ----------
        X : ndarray of shape (n_samples_X, n_features)

        hyperparameters : Dict
            Lambda characteristic length
            sigma_f controls the marginal variance of b(x)
            sigma_0 unresolvable error) nugget term that is interpreted as random
                    error that cannot be attributed to measurement error.
        Returns
        -------
        var_cov_matrix : ndarray of shape (n_samples_X,n_samples_X)
            Kernel k(X, X).

        """
        from sklearn.gaussian_process.kernels import RBF
        min_max_scaler = preprocessing.MinMaxScaler()
        X_minmax = min_max_scaler.fit_transform(X)

        nparams = len(Sigma2)
        # characteristic length (0,1]
        Lambda = Sigma2[0]
        # sigma_f controls the marginal variance of b(x)
        sigma2_f = Sigma2[1]

        # cov_matrix = sigma2_f*rbf_kernel(X_minmax, gamma = 1/Lambda**2)

        rbf = RBF(length_scale=Lambda)
        cov_matrix = sigma2_f * rbf(X_minmax)
        if nparams > 2:
            # (unresolvable error) nugget term that is interpreted as random
            # error that cannot be attributed to measurement error.
            sigma2_0 = Sigma2[2:]
            for i, j in np.ndindex(cov_matrix.shape):
                cov_matrix[i, j] += np.sum(sigma2_0) if i==j else 0

        return cov_matrix

    # -------------------------------------------------------------------------
    def normpdf(self, Outputs, Data, TotalSigma2s, Sigma2=None, std=None):

        Model = self.PCEModel.ModelObj
        logLik = 0.0
        formatting_function = np.vectorize(lambda f: format(f, '6.2e'))

        # Extract the requested model outputs for likelihood calulation
        if self.ReqOutputType is None:
            OutputType = Model.Output.Names
        else:
            OutputType = list(self.ReqOutputType)

        # Loop over the outputs
        for idx, out in enumerate(OutputType):

            # (Meta)Model Output
            nsamples, nout = Outputs[out].shape

            # Prepare data and remove NaN
            try:
                data = Data[out].to_numpy()[~np.isnan(Data[out])]
            except:
                data = Data[out][~np.isnan(Data[out])]
            totalSigma2s = TotalSigma2s[out][~np.isnan(TotalSigma2s[out])][:nout]

            # If sigma2 is not given, use given TotalSigma2s
            if Sigma2 is None:
                logLik += stats.multivariate_normal.logpdf(Outputs[out], data,
                                                           np.diag(totalSigma2s))
                continue

            # Loop over each run/sample and calculate logLikelihood
            logliks = np.zeros(nsamples)
            for s_idx in range(nsamples):

                # Simulation run
                TotalOutputs = Outputs[out]

                # Covariance Matrix
                covMatrix = np.diag(totalSigma2s)

                if Sigma2 is not None:
                    # Check the type error term
                    if hasattr(self, 'BiasInputs') and not hasattr(self, 'errorModel'):
                        # TODO: Infer a Bias model usig Gaussian Process Regression
                        BiasInputs = np.hstack((self.BiasInputs[out],
                                                TotalOutputs[s_idx].reshape(-1,1)))
                        # EDY = self.PCEModel.ExpDesign.Y[out]
                        # BiasInputs = np.hstack((self.BiasInputs[out],EDY.T))
                        params = Sigma2[s_idx,:3] if idx==0 else Sigma2[s_idx,3:]
                        covMatrix = self.RBF_kernel(BiasInputs, params)
                        # covMatrix = self.RBF_kernel(self.BiasInputs[out], Sigma2)
                    else:
                        # Infer equal sigma2s
                        try:
                            sigma2 = Sigma2[s_idx, idx]
                        except:
                            sigma2 = 0.0

                        covMatrix += sigma2 * np.eye(nout)
                        # covMatrix = np.diag(sigma2 * totalSigma2s)

                # Add the std of the PCE is chosen as emulator.
                if self.emulator:
                    stdPCE = std[out] if std is not None else np.mean(self._stdPCEPriorPred[out], axis=0)
                    # Expected value of variance (Assump: i.i.d stds)
                    covMatrix += np.diag(stdPCE**2)

                # print(formatting_function(covMatrix))
                # Select the data points to compare
                if self.selectedIndices is not None:
                    indices = self.selectedIndices[out]
                    covMatrix = np.diag(covMatrix[indices, indices])
                else:
                    indices = list(range(nout))

                # Compute loglikelihood
                logliks[s_idx] = self._logpdf(TotalOutputs[s_idx, indices],
                                              data[indices], covMatrix)

            logLik += logliks

        return logLik

    # -------------------------------------------------------------------------
    def normpdferror(self, deviation, stds):
        PCEModel = self.PCEModel
        Model = PCEModel.ModelObj

        # Extract the requested model outputs for likelihood calulation
        if self.ReqOutputType is None:
            OutputType = Model.Output.Names
        else:
            OutputType = list(self.ReqOutputType)
        SampleSize, ndata = deviation[OutputType[0]].shape

        # # Flatten the Output
        # TotalDeviation = np.empty((SampleSize,0))
        # TotalStd = np.empty((SampleSize,0))
        # for idx, outputType in enumerate(OutputType):
        #     TotalDeviation = np.hstack((TotalDeviation, deviation[outputType]))
        #     TotalStd = np.hstack((TotalStd, stds[outputType]))
        # Likelihoods = np.zeros(SampleSize)
        # for i in range(SampleSize):
        #     dev = TotalDeviation[i]
        #     std = TotalStd[i]
        #     covMatrix = np.diag(std**2)
        #     denom2 = (((2*np.pi)**(ndata/2)) * np.sqrt(np.linalg.det(covMatrix)))
        #     Likelihoods[i] = np.exp(-0.5 * np.dot(np.dot(dev, np.linalg.pinv(covMatrix)), dev[:,np.newaxis]))[0]/denom2
        logLik = np.zeros((SampleSize, len(OutputType)))
        for outIdx, out in enumerate(OutputType):
            dev = deviation[out]
            ndata = dev.shape[1]
            for idx in range(ndata):
                beta = PCEModel.clf_poly['Z']['y_'+str(idx+1)].alpha_
                std = np.sqrt(1./beta)
                logLik[:, outIdx] = stats.norm(0, std).logpdf(dev[:, idx])

        logLik = np.sum(logLik, axis=1)
        return logLik

    # -------------------------------------------------------------------------
    def normpdfSigma2(self, Outputs, Data, TotalSigma2s, Sigma2=None, std=None):

        Model = self.PCEModel.ModelObj
        logLik = 0.0

        # Extract the requested model outputs for likelihood calulation
        if self.ReqOutputType is None:
            OutputType = Model.Output.Names
        else:
            OutputType = list(self.ReqOutputType)

        # Loop over the outputs and calculate logLikelihood
        for idx, out in enumerate(OutputType):

            # (Meta)Model Output
            TotalOutputs = Outputs[out]
            nout = TotalOutputs.shape[1]

            # Remove NaN
            try:
                data = Data[out].to_numpy()[~np.isnan(Data[out])]
            except:
                data = Data[out][~np.isnan(Data[out])]
            totalSigma2s = TotalSigma2s[out][~np.isnan(TotalSigma2s[out])][:nout]

            # Covariance diagonal entries
            biasSigma2s = np.zeros((len(Sigma2), nout))
            # biasSigma2s = np.repeat(totalSigma2s.reshape(1,-1),len(Sigma2),axis=0)

            for sidx,sigma2s in enumerate(Sigma2):
                # Check the type error term
                if hasattr(self, 'BiasInputs'):
                    # TODO: Infer a Bias model usig Gaussian Process Regression
                    BiasInputs = np.hstack((self.BiasInputs[out],TotalOutputs.T))
                    biasSigma2s = self.RBF_kernel(BiasInputs, Sigma2)
                    # biasSigma2s = self.RBF_kernel(self.BiasInputs[out], Sigma2)
                else:
                    # Infer equal sigma2s
                    try:
                        sigma2 = sigma2s[idx]
                    except:
                        sigma2 = 0.0

                    # Convert biasSigma2s to a covMatrix
                    # biasSigma2s[sidx] = sigma2 * np.ones(shape=nout)
                    biasSigma2s[sidx] = sigma2 * totalSigma2s

                # Add the std of the PCE is chosen as emulator.
                if self.emulator:
                    stdPCE = std[out] if std is not None else np.mean(self._stdPCEPriorPred[out], axis=0)
                    # Expected value of variance (Assump: i.i.d stds)
                    biasSigma2s[sidx] += stdPCE**3

                # Select the data points to compare
                if self.selectedIndices is not None:
                    biasSigma2s[sidx] = biasSigma2s[self.selectedIndices[out]]

            # Select the data points to compare
            if self.selectedIndices is not None:
                TotalOutputs = TotalOutputs[:, self.selectedIndices[out]]
                data = data[self.selectedIndices[out]]

            # Compute loglikelihood
            split_Outputs = np.array_split(TotalOutputs, 8)
            split_cov = np.array_split(biasSigma2s, 8)
            outList = Parallel(n_jobs=-1, prefer='threads')(
                    delayed(stats.multivariate_normal.logpdf)(output, data, np.diag(cov))
                            for output, cov in zip(split_Outputs,split_cov))
            logLik += np.concatenate(outList).ravel()

        return logLik

    # -------------------------------------------------------------------------
    def BME_Corr_Weight(self, Data, TotalSigma2s, posterior):
        """
        Calculates the correction factor for BMEs.
        """
        PCEModel = self.PCEModel
        OrigModelOutput = PCEModel.ExpDesign.Y
        Model = PCEModel.ModelObj

        # Posterior with guassian-likelihood
        postDist = stats.gaussian_kde(posterior.T)

        # Remove NaN
        Data = Data[~np.isnan(Data)]
        TotalSigma2s = TotalSigma2s[~np.isnan(TotalSigma2s)]

        # Covariance Matrix
        covMatrix = np.diag(TotalSigma2s[:self.ntotMeasurement])

        # Extract the requested model outputs for likelihood calulation
        if self.ReqOutputType is None:
            OutputType = Model.Output.Names
        else:
            OutputType = list(self.ReqOutputType)

        # SampleSize = OrigModelOutput[OutputType[0]].shape[0]


        # Flatten the OutputType for OrigModel
        TotalOutputs = np.concatenate([OrigModelOutput[x] for x in OutputType], 1)

        NrofBayesSamples = self.NrofSamples
        # Evaluate PCEModel on the experimental design
        Samples = PCEModel.ExpDesign.X
        OutputRS, stdOutputRS = PCEModel.eval_metamodel(samples=Samples,name=self.Name)

        # Reset the NrofSamples to NrofBayesSamples
        self.NrofSamples = NrofBayesSamples

        # Flatten the OutputType for PCEModel
        TotalPCEOutputs = np.concatenate([OutputRS[x] for x in OutputRS], 1)
        TotalPCEstdOutputRS= np.concatenate([stdOutputRS[x] for x in stdOutputRS], 1)

        logweight = 0
        for i,sample in enumerate(Samples):
            # Compute likelilhood output vs RS
            covMatrix = np.diag(TotalPCEstdOutputRS[i]**2)
            logLik = self._logpdf(TotalOutputs[i], TotalPCEOutputs[i], covMatrix)
            # Compute posterior likelihood of the collocation points
            logpostLik = np.log(postDist.pdf(sample[:,None]))[0]
            if logpostLik != -np.inf:
                logweight += logLik + logpostLik
        return logweight
#         # Initialization
#         covMatrix=np.zeros((NofMeasurements, NofMeasurements), float)
#         BME_RM_Model_Weight = np.zeros((SampleSize))
#         BME_RM_Data_Weight = np.zeros((SampleSize))
#         BME_Corr = np.zeros((1))


#         # Deviation Computations
#         RM_Model_Deviation = np.zeros((SampleSize,NofMeasurements))
#         RM_Data_Deviation = np.zeros((SampleSize,NofMeasurements))
#         for i in range(SampleSize):
#             RM_Model_Deviation[i] = TotalOutputs[i][:NofMeasurements] - TotalPCEOutputs[i, :] # Reduce model- Full Model
#             RM_Data_Deviation[i] = Observations - TotalPCEOutputs[i, :] # Reduce model- Measurement Data


#         # Initialization  of Co-Variance Matrix
#         # For BME_RM_ModelWeight
#         if NofMeasurements == 1:
#             RM_Model_Error = np.zeros((NofMeasurements, NofMeasurements), float)
#             np.fill_diagonal(RM_Model_Error, np.cov(RM_Model_Deviation.T))
#         else:
#             RM_Model_Error = np.cov(RM_Model_Deviation.T)


#         # Computation of Weight according to the deviations
#         for i in range(SampleSize):
#             # For BME_RM_DataWeight
#             try:
#                 var = Sigma[i]
#                 if len(var)==1:
#                     np.fill_diagonal(covMatrix, var)
#                 else:
#                     row,col = np.diag_indices(covMatrix.shape[0])
#                     covMatrix[row,col] = np.hstack((np.repeat(var[0], NofMeasurements*0.5),np.repeat(var[1], NofMeasurements*0.5)))

#             except:
#                 var = Sigma

#             np.fill_diagonal(covMatrix,  var)

#             # Add the std of the PCE is emulator is chosen.
# #            if self.emulator:
# #                covMatrix_PCE = np.zeros((NofMeasurements, NofMeasurements), float)
# #                stdPCE = np.empty((SampleSize,0))
# #                for outputType in OutputType:
# #                    stdPCE = np.hstack((stdPCE, stdOutputRS[outputType]))
# #
# #                stdPCE = np.mean(stdPCE, axis=1)
# #                np.fill_diagonal(covMatrix_PCE, stdPCE**2)
# #
# #                covMatrix = covMatrix + covMatrix_PCE

#             # Calculate the denomitor
#             denom1 = (np.sqrt(2*np.pi)) ** NofMeasurements
#             denom2 = (((2*np.pi)**(NofMeasurements/2)) * np.sqrt(np.linalg.det(covMatrix)))

#             BME_RM_Model_Weight[i] =  (np.exp(-0.5 * np.dot(np.dot(RM_Model_Deviation[i], np.linalg.pinv(RM_Model_Error)), RM_Model_Deviation[i])))/denom1
#             BME_RM_Data_Weight[i] =  (np.exp(-0.5 * np.dot(np.dot(RM_Data_Deviation[i], np.linalg.pinv(covMatrix)), RM_Data_Deviation[i][:,np.newaxis])))/denom2

#         for i in range(SampleSize):
#             BME_Corr[0] += BME_RM_Model_Weight[i] * BME_RM_Data_Weight[i] / np.nansum(BME_RM_Data_Weight)

#         return np.log(BME_Corr[0])

    #--------------------------------------------------------------------------------------------------------
    def Rejection_Sampling(self):

        PCEModel = self.PCEModel
        try:
            Sigma2Prior = self.Discrepancy.Sigma2Prior
        except:
            Sigma2Prior = None

        # Check if the discrepancy is defined as a distribution:
        MCSamples = self.Samples

        if Sigma2Prior is not None:
            MCSamples = np.hstack((MCSamples, Sigma2Prior))

        # Take the first column of Likelihoods (Observation data without noise)
        Likelihoods = np.exp(self.logLikelihoods[:,0])
        NrofSamples = len(Likelihoods)
        NormLikelihoods = Likelihoods / np.max(Likelihoods)

        # Normalize based on min if all Likelihoods are zero
        if all(Likelihoods == 0.0):
            Likelihoods = self.logLikelihoods[:,0]
            NormLikelihoods = Likelihoods / np.min(Likelihoods)

        # Random numbers between 0 and 1
        unif = np.random.rand(1, NrofSamples)[0]

        # Reject the poorly performed prior
        acceptedSamples = MCSamples[NormLikelihoods >= unif]

        # Output the Posterior

        InputNames = [PCEModel.input_obj.Marginals[i].Name for i in range(len(PCEModel.input_obj.Marginals))]
        if Sigma2Prior is not None:
            for name in self.Discrepancy.Name:
                InputNames.append(name)

        return pd.DataFrame(acceptedSamples, columns=InputNames)

    #--------------------------------------------------------------------------------------------------------
    def PosteriorPredictive(self):

        PCEModel = self.PCEModel
        Model = PCEModel.ModelObj

        # Make a directory to save the prior/posterior predictive
        OutputDir = (r'Outputs_Bayes_' + Model.Name + '_' + self.Name)
        if not os.path.exists(OutputDir): os.makedirs(OutputDir)

        # Read observation data and perturb it if requested
        if self.MeasuredData is None:
            self.MeasuredData = Model.read_observation(case=self.Name)

        if not isinstance(self.MeasuredData, pd.DataFrame):
            self.MeasuredData = pd.DataFrame(self.MeasuredData)

        # X_values
        x_values = PCEModel.ExpDesign.x_values

        try:
            Sigma2Prior = self.Discrepancy.Sigma2Prior
        except:
            Sigma2Prior = None

        Posterior_df = self.Posterior_df

        # Take care of the sigma2
        if Sigma2Prior is not None:
            try:
                sigma2s = Posterior_df[self.Discrepancy.Name].to_numpy()
                Posterior_df = Posterior_df.drop(labels=self.Discrepancy.Name, axis=1)
            except:
                sigma2s = self.sigma2s

        # Posterior predictive
        if self.emulator:
            if self.SamplingMethod == 'rejection':
                PriorPred = self.__meanPCEPriorPred
            if self.Name != 'Calib':
                PosteriorPred, PosteriorPred_std = self.__meanPCEPriorPred,self._stdPCEPriorPred
            else:
                PosteriorPred, PosteriorPred_std = PCEModel.eval_metamodel(samples=Posterior_df.to_numpy(),
                                                           name=self.Name)
                # TODO: Correct the predictions with Model discrepancy
                if hasattr(self, 'errorModel') and self.errorModel:
                    PosteriorPred, PosteriorPred_std = self.errorMetaModel.eval_model_error(self.BiasInputs,
                                                                              PosteriorPred)
        else:
            if self.SamplingMethod == 'rejection':
                PriorPred = self.__ModelPriorPred
            if self.Name != 'Calib':
                PosteriorPred, PosteriorPred_std = self.__meanPCEPriorPred,self._stdPCEPriorPred
            else:
                PosteriorPred = self.eval_Model(Samples=Posterior_df.to_numpy(),key='PostPred')

                # TODO: Correct the predictions with Model discrepancy
                if hasattr(self, 'errorModel') and self.errorModel:
                    PosteriorPred, PosteriorPred_std = self.errorMetaModel.eval_model_error(self.BiasInputs,
                                                                              PosteriorPred)

        # Add discrepancy from likelihood Sample to the current posterior runs
        TotalSigma2 = self.Discrepancy.TotalSigma2
        PosteriorPred_withnoise = copy.deepcopy(PosteriorPred)
        for varIdx, var in enumerate(Model.Output.Names):
            for i in range(len(PosteriorPred[var])):
                pred = PosteriorPred[var][i]

                # Known sigma2s
                totalSigma2 = TotalSigma2[var][~np.isnan(TotalSigma2[var])][:len(pred)]
                cov = np.diag(totalSigma2)

                # Check the type error term
                if Sigma2Prior is not None:
                    # Inferred sigma2s
                    if hasattr(self, 'BiasInputs') and not hasattr(self, 'errorModel'):
                        # TODO: Infer a Bias model usig Gaussian Process Regression
                        EDY = self.PCEModel.ExpDesign.Y[var]
                        # BiasInputs = np.hstack((self.BiasInputs[var],EDY.T))
                        BiasInputs = np.hstack((self.BiasInputs[var],pred.reshape(-1,1)))
                        sigma2 = sigma2s[i,:3] if varIdx==0 else sigma2s[i,3:]
                        cov = self.RBF_kernel(BiasInputs, sigma2)
                        # cov = self.RBF_kernel(self.BiasInputs[var], sigma2s[i])
                    else:
                        # Infer equal sigma2s
                        try:
                            sigma2 = sigma2s[i, varIdx]
                        except:
                            sigma2 = 0.0

                        # Convert biasSigma2s to a covMatrix
                        cov += sigma2 * np.eye(len(pred))
                        # cov = np.diag(sigma2 * totalSigma2)

                if self.emulator:
                    stdPCE = PCEModel.RMSE[var] if PCEModel.RMSE is not None else PosteriorPred_std[var][i]
                    # Expected value of variance (Assump: i.i.d stds)
                    cov += np.diag(stdPCE**2)

                # Sample a multi-variate normal distribution with mean of prediction and variance of cov
                PosteriorPred_withnoise[var][i] = np.random.multivariate_normal(pred, cov, 1)

        # ----- Prior Predictive -----
        if self.SamplingMethod == 'rejection':
            # Create hdf5 metadata
            hdf5file = OutputDir+'/priorPredictive.hdf5'
            hdf5_exist = os.path.exists(hdf5file)
            if hdf5_exist: os.remove(hdf5file)
            file = h5py.File(hdf5file, 'a')

            # Store x_values
            if type(x_values) is dict:
                grp_x_values = file.create_group("x_values/")
                for varIdx, var in enumerate(Model.Output.Names):
                    grp_x_values.create_dataset(var, data=x_values[var])
            else:
                file.create_dataset("x_values", data=x_values)

            # Store posterior predictive
            grpY = file.create_group("EDY/")
            for varIdx, var in enumerate(Model.Output.Names):
                grpY.create_dataset(var, data=PriorPred[var])

        # ----- Posterior Predictive -----
        # Create hdf5 metadata
        hdf5file = OutputDir+'/postPredictive_wo_noise.hdf5'
        hdf5_exist = os.path.exists(hdf5file)
        if hdf5_exist: os.remove(hdf5file)
        file = h5py.File(hdf5file, 'a')

        # Store x_values
        if type(x_values) is dict:
            grp_x_values = file.create_group("x_values/")
            for varIdx, var in enumerate(Model.Output.Names):
                grp_x_values.create_dataset(var, data=x_values[var])
        else:
            file.create_dataset("x_values", data=x_values)

        # Store posterior predictive
        grpY = file.create_group("EDY/")
        for varIdx, var in enumerate(Model.Output.Names):
            grpY.create_dataset(var, data=PosteriorPred[var])

        # ----- Posterior Predictive -----
        # Create hdf5 metadata
        hdf5file = OutputDir+'/postPredictive.hdf5'
        hdf5_exist = os.path.exists(hdf5file)
        if hdf5_exist: os.remove(hdf5file)
        file = h5py.File(hdf5file, 'a')

        # Store x_values
        if type(x_values) is dict:
            grp_x_values = file.create_group("x_values/")
            for varIdx, var in enumerate(Model.Output.Names):
                grp_x_values.create_dataset(var, data=x_values[var])
        else:
            file.create_dataset("x_values", data=x_values)

        # Store posterior predictive
        grpY = file.create_group("EDY/")
        for varIdx, var in enumerate(Model.Output.Names):
            grpY.create_dataset(var, data=PosteriorPred_withnoise[var])

        return

    #--------------------------------------------------------------------------------------------------------
    def create_Inference(self):

        # Set some variables
        PCEModel = self.PCEModel
        Model = PCEModel.ModelObj
        NofPa = PCEModel.NofPa
        OutputNames = Model.Output.Names
        par_names = PCEModel.ExpDesign.par_names

        # If the prior is set by the user, take it.
        if self.Samples is None:
            self.Samples = self.get_Sample()
        else:
            try:
                SamplesAllParameters = self.Samples.to_numpy()
            except:
                SamplesAllParameters = self.Samples

            try:
                # Take care of an additional Sigma2s
                self.Samples = SamplesAllParameters[:,:NofPa]
            except:
                self.Samples = SamplesAllParameters

            self.NrofSamples = self.Samples.shape[0]

        # ---------- Preparation of observation data ----------
        # Read observation data and perturb it if requested
        if self.MeasuredData is None:
            self.MeasuredData = Model.read_observation(case=self.Name)

        if not isinstance(self.MeasuredData, pd.DataFrame):
            self.MeasuredData = pd.DataFrame(self.MeasuredData)
        ObservationData = self.MeasuredData[OutputNames].to_numpy()

        nMeasurement, nOutputs = ObservationData.shape
        self.ntotMeasurement = ObservationData[~np.isnan(ObservationData)].shape[0]
        BootstrapItrNr = self.BootstrapItrNr if not self.BayesLOOCV else self.ntotMeasurement
        perturbedData = np.zeros((BootstrapItrNr,self.ntotMeasurement ))
        perturbedData[0] = ObservationData.T[~np.isnan(ObservationData.T)]

        if len(self.MeasurementError) == 0:
            if isinstance(self.Discrepancy, dict):
                Disc = self.Discrepancy['known']
            else:
                Disc = self.Discrepancy
            if isinstance(Disc, dict):
                self.MeasurementError = {k:np.sqrt(Disc.Parameters[k]) for k in
                                         Disc.Parameters.keys()}
            else:
                try:
                    self.MeasurementError = np.sqrt(Disc.Parameters)
                except:
                    pass

        # ---------- Preparation of variance for covariance matrix ----------
        # TODO: Modification required.
        # Independent and identically distributed

        TotalSigma2 = dict()
        optSigmaFlag = isinstance(self.Discrepancy, dict)
        optSigma = None
        for keyIdx, key in enumerate(OutputNames):

            # Find optSigma
            if optSigmaFlag and optSigma is None:
                # Option A: known error with unknown bias term
                optSigma = 'A'
                knownDiscrepancy = self.Discrepancy['known']
                self.Discrepancy = self.Discrepancy['infer']
                sigma2 = np.array(knownDiscrepancy.Parameters[key])

            elif optSigma == 'A' or self.Discrepancy.Parameters is not None:
                # Option B: The sigma2 is known (no bias term)
                if optSigma == 'A':
                    sigma2 = np.array(knownDiscrepancy.Parameters[key])
                else:
                    optSigma = 'B'
                    sigma2 = np.array(self.Discrepancy.Parameters[key])

            elif not isinstance(self.Discrepancy.InputDisc, str):
                # Option C: The sigma2 is unknown (bias term including error)
                optSigma = 'C'
                self.Discrepancy.optSigma = optSigma
                sigma2 = np.zeros((nMeasurement))

            TotalSigma2[key] = sigma2

            self.Discrepancy.optSigma = optSigma
            self.Discrepancy.TotalSigma2 = TotalSigma2

        # If inferred sigma2s obtained from e.g. calibration are given
        try:
            self.sigma2s = self.Discrepancy.get_Sample(self.NrofSamples)
        except:
            pass

        # ---------------- Bootstrap & TOM --------------------
        if self.Bootstrap or self.BayesLOOCV:
            if len(self.perturbedData) == 0:
                # zero mean noise Adding some noise to the observation function
                BootstrapNoise = self.BootstrapNoise
                for itrIdx in range(1,BootstrapItrNr):
                    data = np.zeros((nMeasurement, nOutputs))
                    for idx in range(len(OutputNames)):
                        if self.BayesLOOCV:
                            data[:,idx] = ObservationData[:,idx]
                        else:
                            std = np.nanstd(ObservationData[:,idx])
                            if std == 0: std = 0.001
                            noise = std * BootstrapNoise
                            data[:,idx] = np.add(ObservationData[:,idx] , np.random.normal(0, 1, ObservationData.shape[0]) * noise)


                    perturbedData[itrIdx] = data.T[~np.isnan(data.T)]
                self.perturbedData = perturbedData

            # -------- Model Discrepancy -----------
            if hasattr(self, 'errorModel') and self.errorModel \
                and self.Name.lower()!='calib':
                # Select posterior mean as MAP
                MAP_theta = self.Samples.mean(axis=0).reshape((1,NofPa))
                # MAP_theta = stats.mode(self.Samples,axis=0)[0]

                # Evaluate the (meta-)model at the MAP
                y_MAP, y_std_MAP = PCEModel.eval_metamodel(samples=MAP_theta,name=self.Name)

                # Train a GPR meta-model using MAP
                self.errorMetaModel = PCEModel.create_model_error(self.BiasInputs,y_MAP,
                                                                  Name=self.Name)

            # -----------------------------------------------------
            # ----- Loop over the perturbed observation data ------
            # -----------------------------------------------------
            # Initilize arrays
            logLikelihoods = np.zeros((self.NrofSamples,BootstrapItrNr),dtype=np.float16)
            BME_Corr =  np.zeros((BootstrapItrNr))
            logBME = np.zeros((BootstrapItrNr))
            KLD = np.zeros((BootstrapItrNr))
            infEntropy = np.zeros((BootstrapItrNr))
            surrError = dict()

            # Evaluate the PCEModel
            if self.emulator:
                self.__meanPCEPriorPred, self._stdPCEPriorPred = PCEModel.eval_metamodel(samples=self.Samples,
                                                                                         name=self.Name)
                # TODO: Correct the predictions with Model discrepancy
                if hasattr(self, 'errorModel') and self.errorModel:
                    self.__meanPCEPriorPred, self._stdPCEPriorPred = self.errorMetaModel.eval_model_error(self.BiasInputs,
                                                                              self.__meanPCEPriorPred)

                # Surrogate model's error using RMSE of test data
                surrError = PCEModel.RMSE if hasattr(PCEModel,'RMSE') else None
            else:
                self.__ModelPriorPred = self.eval_Model(Samples=self.Samples,key='PriorPred')

            for itrIdx, data in tqdm(enumerate(self.perturbedData), ascii=True, desc ="Boostraping the BME calculations"):

                # ---------------- Likelihood calculation ----------------
                modelEvaluations = self.__meanPCEPriorPred if self.emulator else self.__ModelPriorPred

                # TODO: Leave one out / Justifiability analysis
                if self.BayesLOOCV:
                    self.selectedIndices = np.nonzero(data)[0]
                    # self.selectedIndices = np.delete(list(range(len(self.perturbedData))),itrIdx)

                # Prepare data dataframe
                nobs = list(self.MeasuredData.count().to_numpy()[1:])
                numbers = list(map(sum, zip([0] + nobs, nobs)))
                indices = list(zip([0] + numbers, numbers))
                data_dict = {OutputNames[i]:data[j:k] for i,(j,k) in enumerate(indices)}

                # unknown sigma2
                if optSigma == 'C' or hasattr(self, 'sigma2s'):
                    logLikelihoods[:,itrIdx] = self.normpdfSigma2(modelEvaluations, data_dict, TotalSigma2,Sigma2=self.sigma2s, std=surrError)
                else:
                    # known sigma2
                    logLikelihoods[:,itrIdx] = self.normpdf(modelEvaluations, data_dict, TotalSigma2, std=surrError)

                    # y,std = PCEModel.eval_model_error(self.Samples)
                    # logLikError = self.normpdferror(y, std)

                # ---------------- BME Calculations ----------------
                # BME (log)
                logBME[itrIdx] = np.log(np.nanmean(np.exp(logLikelihoods[:,itrIdx],dtype=np.float128)))

                # Rejection Step
                # Random numbers between 0 and 1
                unif = np.random.rand(1, self.NrofSamples)[0]

                # Reject the poorly performed prior
                Likelihoods = np.exp(logLikelihoods[:,itrIdx],dtype=np.float64)
                accepted = (Likelihoods/np.max(Likelihoods)) >= unif
                X_Posterior = self.Samples[accepted]

                # Posterior-based expectation of likelihoods
                postExpLikelihoods = np.mean(logLikelihoods[:,itrIdx][accepted])

                # Posterior-based expectation of prior densities
                # postExpPrior = np.mean([PCEModel.ExpDesign.JDist(sample)[0] for sample in X_Posterior])
                # postExpPrior = np.mean(np.log([PCEModel.ExpDesign.JDist.pdf(X_Posterior.T)]))

                # Calculate Kullback-Leibler Divergence
                #KLD = np.mean(np.log(Likelihoods[Likelihoods!=0])- logBME)
                KLD[itrIdx] = postExpLikelihoods - logBME[itrIdx]

                # Information Entropy based on Entropy paper Eq. 38
                # infEntropy[itrIdx] = logBME[itrIdx] - postExpPrior - postExpLikelihoods

                # TODO: BME correction when using Emulator
                # if self.emulator:
                #     BME_Corr[itrIdx] = self.BME_Corr_Weight(data,TotalSigma2, X_Posterior)

                # Clear memory
                gc.collect(generation=2)

            # ---------------- Store BME, Likelihoods for all ----------------
            # Likelihoods (Size: NrofSamples,BootstrapItrNr)
            self.logLikelihoods = logLikelihoods

            # BME (log), KLD, infEntropy (Size: 1,BootstrapItrNr)
            self.logBME = logBME
            self.KLD = KLD
            self.infEntropy = infEntropy
            # TODO: BMECorrFactor (log) (Size: 1,BootstrapItrNr)
            # if self.emulator: self.BMECorrFactor = BME_Corr

            # BME = BME + BMECorrFactor
            if self.emulator: self.logBME = self.logBME #+ self.BMECorrFactor

        # ---------------- Parameter Bayesian inference ----------------
        if self.SamplingMethod.lower() == 'mcmc':

            # Convert the pandas data frame to numpy, if it's applicable.
            if self.MCMCinitSamples is not None and isinstance(self.MCMCinitSamples, pd.DataFrame):
                self.MCMCinitSamples = self.MCMCinitSamples.to_numpy()

            # MCMC
            initsamples = None if self.MCMCinitSamples is None else self.MCMCinitSamples
            nsteps = 100000 if self.MCMCnSteps is None else self.MCMCnSteps
            nwalkers = 50*self.PCEModel.NofPa if self.MCMCnwalkers is None else self.MCMCnwalkers
            multiprocessing = False if self.MultiProcessMCMC is None else self.MultiProcessMCMC
            MCMC_ = MCMC(self, initsamples=initsamples, nwalkers=nwalkers, verbose=self.MCMCverbose,
                         nsteps = nsteps, moves=self.MCMCmoves, multiprocessing=multiprocessing)
            self.Posterior_df = MCMC_.run_sampler(self.MeasuredData, TotalSigma2)

        elif self.Name.lower() == 'valid':
            self.Posterior_df = pd.DataFrame(self.Samples, columns=par_names)

        else: # Rejection sampling
            self.Posterior_df = self.Rejection_Sampling()


        # Provide posterior's summary
        print('\n')
        print('-'*15 + 'Posterior summary' + '-'*15)
        pd.options.display.max_columns = None
        pd.options.display.max_rows = None
        print(self.Posterior_df.describe())
        print('-'*50)

        # -------- Model Discrepancy -----------
        if hasattr(self, 'errorModel') and self.errorModel \
            and self.Name.lower()=='calib':
            if self.SamplingMethod.lower() == 'mcmc':
                self.errorMetaModel = MCMC_.errorMetaModel
            else:
                # Select posterior mean as MAP
                Posterior_df = self.Posterior_df.to_numpy() if optSigma == "B" else self.Posterior_df.to_numpy()[:,:-len(Model.Output.Names)]
                MAP_theta = Posterior_df.mean(axis=0).reshape((1,NofPa))
                # MAP_theta = stats.mode(Posterior_df,axis=0)[0]

                # Evaluate the (meta-)model at the MAP
                y_MAP, y_std_MAP = PCEModel.eval_metamodel(samples=MAP_theta,name=self.Name)

                # Train a GPR meta-model using MAP
                self.errorMetaModel = PCEModel.create_model_error(self.BiasInputs,y_MAP,
                                                                  Name=self.Name)

        # -------- Posterior perdictive -----------
        self.PosteriorPredictive()

        # -----------------------------------------------------
        # ------------------ Visualization --------------------
        # -----------------------------------------------------
        OutputDir = (r'Outputs_Bayes_' + Model.Name + '_' + self.Name)
        if not os.path.exists(OutputDir): os.makedirs(OutputDir)

        # -------- Posteior parameters --------
        if optSigma != "B":
            par_names.extend([self.Discrepancy.InputDisc.Marginals[i].Name for i in range(len(self.Discrepancy.InputDisc.Marginals))])

        figPosterior = corner.corner(self.Posterior_df.to_numpy(), labels=par_names,
                                     quantiles=[0.15, 0.5, 0.85],show_titles=True,
                                     title_fmt=self.Corner_title_fmt,
                                     labelpad=0.2,
                                     use_math_text=True,
                                     title_kwargs={"fontsize": 28},
                                     plot_datapoints=False,
                                     plot_density=False,
                                     fill_contours=True,
                                     smooth=0.5,
                                     smooth1d=0.5)

        # Loop over axes and set x limits
        if optSigma == "B":
            axes = np.array(figPosterior.axes).reshape((len(par_names), len(par_names)))
            for yi in range(len(par_names)):
                ax = axes[yi, yi]
                ax.set_xlim(PCEModel.BoundTuples[yi])
                for xi in range(yi):
                    ax = axes[yi, xi]
                    ax.set_xlim(PCEModel.BoundTuples[xi])

        # Extract the axes
        # axes = np.array(figPosterior.axes).reshape((NofPa, NofPa))

        # # Loop over the diagonal
        # for i in range(NofPa):
        #     ax = axes[i, i]
        #     ax.axvline(MAP_theta[0,i], ls='--', color="r")

        # # Rotate the axis label
        # for i in range(NofPa):
        #     #ax_x = axes[-1, i]
        #     ax_y = axes[i, 0]
        #     if i != 0:
        #         ax_y.set_ylabel(parNames[i],rotation=45)

        # Loop over the histograms
        # for yi in range(NofPa):
        #     for xi in range(yi):
        #         ax = axes[yi, xi]
        #         ax.set_xlabel(parNames[xi],rotation=45)
        #         ax.set_ylabel(parNames[yi],rotation=45)
        #         ax.axvline(MAP_theta[0,xi], ls='--', color="r")
        #         ax.axhline(MAP_theta[0,yi], ls='--', color="r")
        #         ax.plot(MAP_theta[0,xi], MAP_theta[0,yi], "sr")

        # plt.yticks(rotation=45, horizontalalignment='right')
        figPosterior.set_size_inches((24,16))

        # Turn off gridlines
        for ax in figPosterior.axes:
            ax.grid(False)

        if self.emulator:
            plotname = '/Posterior_Dist_'+Model.Name+'_emulator'
        else:
            plotname = '/Posterior_Dist_'+Model.Name

        figPosterior.savefig('./'+OutputDir+ plotname + '.pdf',
                             bbox_inches='tight')


        # -------- Plot MAP --------
        if self.PlotMAPPred:

            # -------- Find MAP and run PCEModel and origModel --------
            # Compute the MAP
            if self.MAP.lower() =='mean':
                Posterior_df = self.Posterior_df.to_numpy() if optSigma == "B" else self.Posterior_df.to_numpy()[:,:-len(Model.Output.Names)]
                MAP_theta = Posterior_df.mean(axis=0).reshape((1,NofPa))
            else:
                MAP_theta = stats.mode(Posterior_df.to_numpy(),axis=0)[0]

            print("\nPoint estimator:\n", MAP_theta[0])

            # Run the models for MAP
            # PCEModel
            MAP_PCEModel, MAP_PCEModelstd = PCEModel.eval_metamodel(samples=MAP_theta,name=self.Name)
            self.MAPpceModelMean = MAP_PCEModel
            self.MAPpceModelStd = MAP_PCEModelstd

            # origModel
            MAP_origModel = self.eval_Model(Samples=MAP_theta)
            self.MAPorigModel = MAP_origModel


            # Extract slicing index
            index = PCEModel.index
            x_values = MAP_origModel['x_values']

            # List of markers and colors
            Color = ['k','b', 'g', 'r']
            Marker = 'x'


            # create a PdfPages object
            pdf = PdfPages('./'+OutputDir+ 'MAP_PCE_vs_Model_'+ self.Name + '.pdf')
            fig = plt.figure()
            for i, key in enumerate(Model.Output.Names):

                Y_Val_ = MAP_origModel[key]
                Y_PC_Val_ = MAP_PCEModel[key]
                Y_PC_Val_std_ = MAP_PCEModelstd[key]

                plt.plot(x_values, Y_Val_, color=Color[i], marker=Marker, lw=2.0, label='$Y_{MAP}^{M}$')

                plt.plot(x_values, Y_PC_Val_[idx,:], color=Color[i], marker=Marker, lw=2.0, linestyle='--', label='$Y_{MAP}^{PCE}$')
                plt.fill_between(x_values, Y_PC_Val_[idx,:]-1.96*Y_PC_Val_std_[idx,:],
                                  Y_PC_Val_[idx,:]+1.96*Y_PC_Val_std_[idx,:], color=Color[i],alpha=0.15)


                # Calculate the adjusted R_squared and RMSE
                R2 = r2_score(Y_PC_Val_.reshape(-1,1), Y_Val_.reshape(-1,1))
                RMSE = np.sqrt(mean_squared_error(Y_PC_Val_, Y_Val_))

                plt.ylabel(key)
                plt.xlabel("Time [s]")
                plt.title('Model vs PCEModel '+ key)

                ax = fig.axes[0]
                leg = ax.legend(loc='best', frameon=True)
                fig.canvas.draw()
                p = leg.get_window_extent().inverse_transformed(ax.transAxes)
                ax.text(p.p0[1]-0.05, p.p1[1]-0.25, 'RMSE = '+ str(round(RMSE, 3)) + '\n' + r'$R^2$ = '+ str(round(R2, 3)),
                        transform=ax.transAxes, color='black', bbox=dict(facecolor='none', edgecolor='black',
                                                 boxstyle='round,pad=1'))

                plt.show()

                # save the current figure
                pdf.savefig(fig, bbox_inches='tight')

                # Destroy the current plot
                plt.clf()

            pdf.close()


        # -------- Plot logBME dist --------
        if self.Bootstrap:
            # # Computing the TOM performance
            # x_values = np.linspace(np.min(self.logBME), np.max(self.logBME), 1000)
            dof = ObservationData.shape[0]
            # self.logTOMBME = stats.chi2(dof).logpdf(-1*x_values)#pdf(x_values)
            self.logTOMBME = stats.chi2.rvs(dof, size=self.logBME.shape[0])

            fig, ax = plt.subplots()
            sns.kdeplot(self.logTOMBME, ax=ax, color="green", shade=True)
            sns.kdeplot(self.logBME, ax=ax, color="blue", shade=True,label='Model BME')

            ax.set_xlabel('log$_{10}$(BME)')
            ax.set_ylabel('Probability density')

            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor='green', edgecolor='green',label='TOM BME'),
                                Patch(facecolor='blue', edgecolor='blue',label='Model BME')]
            ax.legend(handles=legend_elements)

            if self.emulator:
                plotname = '/BME_hist_'+Model.Name+'_emulator'
            else:
                plotname = '/BME_hist_'+Model.Name

            plt.savefig('./'+OutputDir+plotname+'.pdf', bbox_inches='tight')
            plt.show()
            plt.close()

        # -------- Posteior perdictives --------
        if self.PlotPostPred:
            # sns.set_context("paper")
            # Plot the posterior predictive
            for Out_idx, OutputName in enumerate(Model.Output.Names):
                fig, ax = plt.subplots()
                with sns.axes_style("ticks"): #whitegrid
                    x_key = list(self.MeasuredData)[0]

                    # --- Read prior and posterior predictive ---
                    if self.SamplingMethod == 'rejection':
                        #  --- Prior ---
                        # Load posterior predictive
                        f = h5py.File(OutputDir+'/'+"priorPredictive.hdf5", 'r+')

                        try:
                            x_coords = np.array(f["x_values"])
                        except:
                            x_coords = np.array(f["x_values/"+OutputName])

                        X_values = np.repeat(x_coords , np.array(f["EDY/"+OutputName]).shape[0])

                        priorPred_df = {}
                        priorPred_df[x_key] = X_values
                        priorPred_df[OutputName] = np.array(f["EDY/"+OutputName]).flatten('F')
                        priorPred_df = pd.DataFrame(priorPred_df)

                        tags_post = ['prior'] * len(priorPred_df)
                        priorPred_df.insert(len(priorPred_df.columns), "Tags", tags_post, True)


                        # --- Posterior ---
                        f = h5py.File(OutputDir+'/'+"postPredictive.hdf5", 'r+')
                        try:
                            x_coords = np.array(f["x_values"])
                        except:
                            x_coords = np.array(f["x_values/"+OutputName])

                        X_values = np.repeat(x_coords , np.array(f["EDY/"+OutputName]).shape[0])

                        postPred_df = {}
                        postPred_df[x_key] = X_values
                        postPred_df[OutputName] = np.array(f["EDY/"+OutputName]).flatten('F')
                        postPred_df = pd.DataFrame(postPred_df)

                        tags_post = ['posterior'] * len(postPred_df)
                        postPred_df.insert(len(postPred_df.columns), "Tags", tags_post, True)

                        # Concatenate two dataframes based on x_values
                        frames = [priorPred_df,postPred_df]
                        AllPred_df = pd.concat(frames)

                        # --- Plot posterior predictive ---
                        sns.violinplot(x_key, y=OutputName, hue="Tags", legend=False,
                                        ax=ax, split=True, inner=None, data=AllPred_df, color=".8")


                        # # --- Plot MAP (PCEModel) ---
                        # Find the x,y coordinates for each point
                        x_coords = np.arange(x_coords.shape[0])

                        # sns.pointplot(x=x_coords, y=MAP_PCEModel[OutputName][0], color='lime',markers='+',
                        #               linestyles='', capsize=16, ax=ax)

                        # ax.errorbar(x_coords, MAP_PCEModel[OutputName][0],
                        #               yerr=1.96*MAP_PCEModelstd[OutputName][0],
                        #               ecolor='lime', fmt=' ', zorder=-1)

                        # # --- Plot MAP (origModel) ---
                        # sns.pointplot(x=x_coords, y=MAP_origModel[OutputName][0], color='r', markers='+',
                        #               linestyles='' , capsize=14, ax=ax)

                        # --- Plot Data ---
                        first_header = list(self.MeasuredData)[0]
                        ObservationData = self.MeasuredData.round({first_header: 6})
                        sns.pointplot(x=first_header, y=OutputName, color='g', markers='x',
                                      linestyles='', capsize=16, data=ObservationData, ax=ax)

                        ax.errorbar(x_coords, ObservationData[OutputName].to_numpy(),
                                      yerr=1.96*self.MeasurementError[OutputName].to_numpy(),
                                      ecolor='g', fmt=' ', zorder=-1)

                        # Add labels to the legend
                        handles, labels = ax.get_legend_handles_labels()
                        # labels.append('point estimate (PCE Model)')
                        # labels.append('point estimate (Orig. Model)')
                        labels.append('Data')

                        import matplotlib.lines as mlines
                        #red_patch = mpatches.Patch(color='red')
                        data_marker = mlines.Line2D([], [], color='lime', marker='+', linestyle='None',
                                                    markersize=10)
                        # handles.append(data_marker)
                        # data_marker = mlines.Line2D([], [], color='r', marker='+', linestyle='None',
                        #                             markersize=10)
                        # handles.append(data_marker)
                        # data_marker = mlines.Line2D([], [], color='g', marker='x', linestyle='None',
                                                    # markersize=10)
                        handles.append(data_marker)

                        # Add legend
                        ax.legend(handles=handles, labels=labels, loc='best',
                                  fontsize='large', frameon=True)

                    else:
                        # Load posterior predictive
                        f = h5py.File(OutputDir+'/'+"postPredictive.hdf5", 'r+')

                        try:
                            x_coords = np.array(f["x_values"])
                        except:
                            x_coords = np.array(f["x_values/"+OutputName])

                        mu = np.mean(np.array(f["EDY/"+OutputName]), axis=0)
                        std = np.std(np.array(f["EDY/"+OutputName]), axis=0)

                        # --- Plot posterior predictive ---
                        plt.plot(x_coords, mu, marker='o', color='b', label='Mean Post. Predictive')
                        plt.fill_between(x_coords, mu-1.96*std, mu+1.96*std, color='b', alpha=0.15)

                        # --- Plot Data ---
                        ax.plot(x_coords, self.MeasuredData[OutputName].to_numpy(),'ko',label ='data',markeredgecolor='w')

                        # --- Plot ExpDesign ---
                        index = self.PCEModel.index
                        if index is not None:
                            if self.Name == 'Valid':
                                origOutExpDesign = self.PCEModel.ExpDesign.Y[key][:,index:]
                            else:
                                origOutExpDesign = self.PCEModel.ExpDesign.Y[key][:,:index]
                        else:
                            origOutExpDesign = self.PCEModel.ExpDesign.Y[key]

                        for output in origOutExpDesign:
                            plt.plot(x_coords, output, color='grey', alpha=0.15)

                        # # --- Plot MAP (PCEModel) ---
                        # ax.plot(x_coords, MAP_PCEModel[OutputName][0],ls='--', marker='o',c = 'lime' ,label ='point estimate (PCE Model)',markeredgecolor='w')

                        # # --- Plot MAP (origModel) ---
                        # ax.plot(x_coords, MAP_origModel[OutputName][0],ls='-', marker='o',c = 'r',label ='point estimate (Orig. Model)',markeredgecolor='w')


                        # Add labels for axes
                        plt.xlabel('Time [s]')
                        plt.ylabel(key)

                        # Add labels to the legend
                        handles, labels = ax.get_legend_handles_labels()

                        import matplotlib.lines as mlines
                        import matplotlib.patches as mpatches
                        patch = mpatches.Patch(color='b',alpha=0.15)
                        handles.insert(1,patch)
                        labels.insert(1,'95 $\%$ CI')

                        # data_marker = mlines.Line2D([], [], color='grey',alpha=0.15)
                        # handles.append(data_marker)
                        # labels.append('Orig. Model Responses')

                        # Add legend
                        ax.legend(handles=handles, labels=labels, loc='best',
                                  frameon=True)



                    # Save figure in pdf format
                    if self.emulator:
                        plotname = '/Post_Prior_Perd_'+Model.Name+'_emulator'
                    else:
                        plotname = '/Post_Prior_Perd_'+Model.Name

                    fig.savefig('./'+OutputDir+plotname+ '_' +OutputName +'.pdf', bbox_inches='tight')

        return self
