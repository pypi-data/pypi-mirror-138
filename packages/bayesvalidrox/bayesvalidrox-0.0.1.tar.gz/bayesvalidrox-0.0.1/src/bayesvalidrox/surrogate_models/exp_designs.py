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
import math
import itertools
import chaospy
import scipy.stats as st
from tqdm import tqdm

from .apoly_construction import apoly_construction


class ExpDesigns:
    def __init__(self, Input, meta_Model='pce', hdf5_file=None,
                 n_new_samples=1, n_max_samples=None, mod_LOO_threshold=1e-16,
                 tradeoff_scheme=None, n_canddidate=1, explore_method='random',
                 exploit_method='Space-filling', util_func='Space-filling',
                 n_cand_groups=4, n_replication=1, post_snapshot=False,
                 step_snapshot=1, max_a_post=[]):

        self.InputObj = Input
        self.meta_Model = meta_Model
        self.hdf5_file = hdf5_file
        self.n_new_samples = n_new_samples
        self.n_max_samples = n_max_samples
        self.mod_LOO_threshold = mod_LOO_threshold
        self.explore_method = explore_method
        self.exploit_method = exploit_method
        self.util_func = util_func
        self.tradeoff_scheme = tradeoff_scheme
        self.n_canddidate = n_canddidate
        self.n_cand_groups = n_cand_groups
        self.n_replication = n_replication
        self.post_snapshot = post_snapshot
        self.step_snapshot = step_snapshot
        self.max_a_post = max_a_post

    def generate_samples(self, n_samples, sampling_method='random',
                         transform=False):
        """
        Generates samples with given sampling method

        Parameters
        ----------
        n_samples : int
            Number of requested samples.
        sampling_method : TYPE, optional
            DESCRIPTION. The default is 'random'.
        transform : bool, optional
            Transformation via an isoprobabilistic transformation method. The
            default is False.

        Returns
        -------
        samples: array of shape (n_samples, n_params)
            Generated samples from defined model input object.

        """
        try:
            samples = chaospy.generate_samples(n_samples, domain=self.JDist,
                                               rule=sampling_method)
        except:
            samples = self.JDist.resample(n_samples)

        # Transform samples to the original space
        if transform:
            tr_samples = self.transform(samples.T)
            return samples.T, tr_samples
        else:
            return samples.T

    def generate_ED(self, n_samples, sample_method='random', transform=False,
                    max_pce_deg=None):
        """
        Generates experimental designs (training set) with the given method.

        Parameters
        ----------
        n_samples : int
            Number of requested training points.
        sample_method : string, optional
            Sampling method. The default is 'random'.
        transform : bool, optional
            Isoprobabilistic transformation. The default is False.
        max_pce_deg : TYPE, optional
            Maximum PCE polynomial degree. The default is None.

        Returns
        -------
        array of shape (n_samples, n_params)
            Selected training samples.

        """
        Inputs = self.InputObj
        self.ndim = len(Inputs.Marginals)
        if not hasattr(self, 'n_init_samples'):
            self.n_init_samples = self.ndim + 1
        n_samples = int(n_samples)
        if len(Inputs.Marginals[0].input_data) == 0:
            self.arbitrary = False
        else:
            self.arbitrary = True

        # Get the bounds if input_data are directly defined by user:
        if Inputs.Marginals[0].parameters is None:
            for i in range(self.ndim):
                low_bound = np.min(Inputs.Marginals[i].input_data)
                up_bound = np.max(Inputs.Marginals[i].input_data)
                Inputs.Marginals[i].Parameters = [low_bound, up_bound]

        if self.sampling_method == 'user':
            samples = self.X
            self.NrSamples = len(samples)

        # Sample the distribution of parameters
        if not self.arbitrary:
            # Case I = polytype not arbitrary
            # Execute initialization to get the boundtuples
            raw_data, bounds = self.Parameter_Initialization(max_pce_deg)
            self.raw_data = raw_data
            self.BoundTuples = bounds
            # Create ExpDesign in the actual space
            if self.sampling_method != 'user':
                samples = chaospy.generate_samples(n_samples, domain=self.JDist,
                                                   rule=sample_method).T
        elif self.arbitrary:
            # Case II: polytype arbitrary or Input values are directly given by
            # the user.

            # Generate the samples based on requested method
            if self.sampling_method == 'user':
                raw_data, bounds = self.Parameter_Initialization(max_pce_deg)
                self.raw_data = raw_data
                self.BoundTuples = bounds

            elif self.sampling_method == 'random':
                samples = self.MCSampling(n_samples, max_pce_deg)

            elif self.sampling_method == 'PCM' or self.sampling_method == 'LSCM':
                samples = self.PCMSampling(max_pce_deg)

            else:
                # Execute initialization to get the boundtuples
                raw_data, bounds = self.Parameter_Initialization(max_pce_deg)
                self.raw_data = raw_data
                self.BoundTuples = bounds

                # Create ExpDesign in the actual space using chaospy
                try:
                    samples = chaospy.generate_samples(n_samples,
                                                       domain=self.JDist,
                                                       rule=sample_method).T
                except:
                    samples = self.MCSampling(n_samples, max_pce_deg)

        # Transform samples to the original space
        if transform:
            tr_samples = self.transform(samples)
            return samples, tr_samples
        else:
            return samples

    def transform(self, X, params=None):
        """
        Transform the samples via either a Rosenblatt or an isoprobabilistic
        transformation.

        Parameters
        ----------
        X : ndarray of shape (n_samples,n_params)
            Samples to be transformed.

        Returns
        -------
        tr_X: ndarray of shape (n_samples,n_params)
            Transformed samples.

        """
        if self.InputObj.Rosenblatt:
            self.origJDist, _ = self.DistConstructor(False)
            tr_X = self.origJDist.inv(self.JDist.fwd(X.T)).T
        else:
            # Transform samples via an isoprobabilistic transformation
            n_samples, n_params = X.shape
            Inputs = self.InputObj
            origJDist = self.JDist
            poly_types = self.poly_types

            disttypes = []
            for par_i in range(n_params):
                disttypes.append(Inputs.Marginals[par_i].dist_type)

            # Pass non-transformed X, if arbitrary PCE is selected.
            if None in disttypes or self.arbitrary:
                return X

            cdfx = np.zeros((X.shape))
            tr_X = np.zeros((X.shape))

            for par_i in range(n_params):

                # Extract the parameters of the original space
                disttype = disttypes[par_i]
                if disttype is not None:
                    dist = origJDist[par_i]
                else:
                    dist = None
                polytype = poly_types[par_i]
                cdf = np.vectorize(lambda x: dist.cdf(x))

                # Extract the parameters of the transformation space based on
                # polyType
                if polytype == 'legendre' or disttype == 'uniform':
                    # Generate Y_Dists based
                    params_Y = [-1, 1]
                    dist_Y = st.uniform(loc=params_Y[0],
                                        scale=params_Y[1]-params_Y[0])
                    inv_cdf = np.vectorize(lambda x: dist_Y.ppf(x))

                elif polytype == 'hermite' or disttype == 'norm':
                    params_Y = [0, 1]
                    dist_Y = st.norm(loc=params_Y[0], scale=params_Y[1])
                    inv_cdf = np.vectorize(lambda x: dist_Y.ppf(x))

                elif polytype == 'laguerre' or disttype == 'gamma':
                    params_Y = [1, params[1]]
                    dist_Y = st.gamma(loc=params_Y[0], scale=params_Y[1])
                    inv_cdf = np.vectorize(lambda x: dist_Y.ppf(x))

                elif polytype == 'arbitrary' or disttype is None:
                    # mu_X = Inputs.Marginals[par_i].moments[0]
                    # stDev_X = Inputs.Marginals[par_i].moments[1]
                    # cdf = np.vectorize(lambda x: (x - mu_X) / stDev_X)
                    # # TODO: Unknown dist with gaussian_kde
                    # mu_Y = Y_marginals[par_i].moments[0]
                    # stDev_Y = Y_marginals[par_i].moments[1]
                    # inv_cdf = np.vectorize(lambda x: stDev_Y * x + mu_Y)
                    pass

                # Compute CDF_x(X)
                cdfx[:, par_i] = cdf(X[:, par_i])

                # Compute invCDF_y(cdfx)
                tr_X[:, par_i] = inv_cdf(cdfx[:, par_i])

        return tr_X

    def FitDist(self, y):
        dist_results = []
        params = {}
        dist_names = ['lognorm', 'norm', 'uniform', 'expon']
        for dist_name in dist_names:
            dist = getattr(st, dist_name)

            try:
                if dist_name != 'lognorm':
                    param = dist.fit(y)
                else:
                    param = dist.fit(np.exp(y), floc=0)
            except:
                param = dist.fit(y)

            params[dist_name] = param
            # Applying the Kolmogorov-Smirnov test
            D, p = st.kstest(y, dist_name, args=param)
            dist_results.append((dist_name, D))

        # select the best fitted distribution
        sel_dist, D = (min(dist_results, key=lambda item: item[1]))

        if sel_dist == 'uniform':
            params[sel_dist] = [params[sel_dist][0], params[sel_dist][0] +
                                params[sel_dist][1]]
        if D < 0.05:
            return sel_dist, params[sel_dist]
        else:
            return None, None

    def DistConstructor(self, rosenblatt):
        Inputs = self.InputObj
        all_data = []
        all_DistTypes = []
        origJoints = []
        poly_types = []

        for parIdx in range(self.ndim):

            if Inputs.Marginals[parIdx].dist_type is None:
                data = Inputs.Marginals[parIdx].input_data
                all_data.append(data)
                DistType, params = self.FitDist(data)
                Inputs.Marginals[parIdx].dist_type = DistType
                Inputs.Marginals[parIdx].parameters = params
            else:
                DistType = Inputs.Marginals[parIdx].dist_type
                params = Inputs.Marginals[parIdx].parameters

            if rosenblatt:
                polytype = 'hermite'
                Dist = chaospy.Normal()

            elif DistType is None:
                polytype = 'arbitrary'
                Dist = None

            elif 'unif' in DistType:
                polytype = 'legendre'
                Dist = chaospy.Uniform(lower=params[0], upper=params[1])

            elif DistType == 'norm':
                polytype = 'hermite'
                Dist = chaospy.Normal(mu=params[0], sigma=params[1])

            elif DistType == 'gamma':
                polytype = 'laguerre'
                Dist = chaospy.Gamma(shape=params[0],
                                     scale=params[1],
                                     shift=params[2])

            elif DistType == 'beta':
                polytype = 'jacobi'
                Dist = chaospy.Beta(alpha=params[0], beta=params[1],
                                    lower=params[2], upper=params[3])

            elif 'lognorm' in DistType:
                polytype = 'hermite'
                Mu = np.log(params[0]**2/np.sqrt(params[0]**2 + params[1]**2))
                Sigma = np.sqrt(np.log(1 + params[1]**2 / params[0]**2))
                Dist = chaospy.LogNormal(mu=Mu, sigma=Sigma)

            elif DistType == 'exponential' or 'expon' in DistType:
                polytype = 'arbitrary'
                Dist = chaospy.Exponential(scale=params[0], shift=params[1])

            elif DistType == 'weibull':
                polytype = 'arbitrary'
                Dist = chaospy.Weibull(shape=params[0], scale=params[1],
                                       shift=params[2])

            else:
                message = (f"DistType {DistType} for parameter"
                           f"{parIdx+1} is not available.")
                raise ValueError(message)

            if self.arbitrary:
                polytype = 'arbitrary'

            # Store dists and poly_types
            origJoints.append(Dist)
            poly_types.append(polytype)
            all_DistTypes.append(DistType)

        # Prepare final output to return
        if None in all_DistTypes:
            # Naive approach: Fit a gaussian kernel to the provided data
            Data = np.asarray(all_data)
            origSpaceDist = st.gaussian_kde(Data)
            self.priorSpace = origSpaceDist
        else:
            origSpaceDist = chaospy.J(*origJoints)
            self.priorSpace = st.gaussian_kde(origSpaceDist.sample(10000))

        return origSpaceDist, poly_types

    def Parameter_Initialization(self, MaxPceDegree=None, OptDesignFlag=False):
        """
        Initialization Uncertain Parameters in case arbitrary polytype is
        selected.
        """
        Inputs = self.InputObj
        ndim = self.ndim
        Rosenblatt = Inputs.Rosenblatt
        self.MCSize = 10000

        # Create a multivariate probability distribution
        if MaxPceDegree is not None:
            JDist, poly_types = self.DistConstructor(rosenblatt=Rosenblatt)
            self.JDist, self.poly_types = JDist, poly_types

        if self.arbitrary:

            self.MCSize = len(Inputs.Marginals[0].input_data)
            self.raw_data = np.zeros((ndim, self.MCSize))
            self.par_names = []

            for parIdx in range(ndim):
                # Save parameter names
                self.par_names.append(Inputs.Marginals[parIdx].name)
                try:
                    self.raw_data[parIdx] = np.array(Inputs.Marginals[parIdx].input_data)
                except:
                    self.raw_data[parIdx] = self.JDist[parIdx].sample(self.MCSize)

            # Create orthogonal polynomial coefficients if necessary
            if self.meta_Model.lower() != 'gpe' \
                and MaxPceDegree is not None \
                    and Inputs.polycoeffsFlag:
                self.polycoeffs = {}
                for parIdx in tqdm(range(ndim), ascii=True, desc="Computing orth. polynomial coeffs"):
                    self.polycoeffs[f'p_{parIdx+1}'] = apoly_construction(self.raw_data[parIdx], MaxPceDegree)
        else:
            # Generate random samples based on parameter distributions
            self.raw_data = chaospy.generate_samples(self.MCSize,
                                                     domain=self.JDist)
        # Extract moments
        for parIdx in range(ndim):
            mu = np.mean(self.raw_data[parIdx])
            std = np.std(self.raw_data[parIdx])
            self.InputObj.Marginals[parIdx].moments = [mu, std]

        # Generate the bounds based on given inputs for marginals
        BoundTuples = []
        for i in range(ndim):
            if Inputs.Marginals[i].dist_type == 'unif':
                low_bound, up_bound = Inputs.Marginals[i].Parameters
            else:
                low_bound = np.min(self.raw_data[i])
                up_bound = np.max(self.raw_data[i])

            BoundTuples.append((low_bound, up_bound))

        self.BoundTuples = tuple(BoundTuples)

        return self.raw_data, self.BoundTuples

    def MCSampling(self, NrSamples, MaxPceDegree):
        """
        Compute the requested number of sampling points.
        Arguments
        ---------
        NrSamples : int
            Number of points requested.
        Returns
        -------
        ndarray[NrSamples, NofPa]
            The sampling locations in the input space.
        """

        # Execute initialization to get the boundtuples
        raw_data, BoundTuples = self.Parameter_Initialization(MaxPceDegree)
        self.raw_data, self.BoundTuples = raw_data, BoundTuples

        Samples = np.zeros((NrSamples, self.ndim))

        for idxPa in range(self.ndim):
            # input_data given
            sample_size = len(self.raw_data[idxPa])
            randIdx = np.random.randint(0, sample_size, NrSamples)
            Samples[:, idxPa] = self.raw_data[idxPa, randIdx]

        return Samples

    def PCMSampling(self, MaxPceDegree):

        raw_data = self.raw_data

        # Guess the closest degree to self.NrSamples
        def M_uptoMax(deg):
            result = []
            for d in range(1, deg+1):
                result.append(math.factorial(self.ndim+d) //
                              (math.factorial(self.ndim) * math.factorial(d)))
            return np.array(result)

        guess_Deg = np.where(M_uptoMax(MaxPceDegree) > self.NrSamples)[0][0]

        Cpoints = np.zeros(shape=[guess_Deg+1, self.ndim])

        def PolynomialPa(parIdx):
            return aPoly_Construction(self.raw_data[parIdx], MaxPceDegree)

        for i in range(self.ndim):
            poly_coeffs = PolynomialPa(i)[guess_Deg+1][::-1]
            Cpoints[:, i] = np.trim_zeros(np.roots(poly_coeffs))

        #  Construction of optimal integration points
        Prod = itertools.product(np.arange(1, guess_Deg+2), repeat=self.ndim)
        SortDigUniqueCombos = np.array(list(filter(lambda x: x, Prod)))

        # Ranking relatively mean
        Temp = np.empty(shape=[0, guess_Deg+1])
        for j in range(self.ndim):
            s = abs(Cpoints[:, j]-np.mean(raw_data[j]))
            Temp = np.append(Temp, [s], axis=0)
        temp = Temp.T

        index_CP = np.sort(temp, axis=0)
        SortCpoints = np.empty(shape=[0, guess_Deg+1])

        for j in range(self.ndim):
            SortCp = Cpoints[index_CP[:, j], j]
            SortCpoints = np.vstack((SortCpoints, SortCp))

        # Mapping of Combination to Cpoint Combination
        SortUniqueCombos = np.empty(shape=[0, self.ndim])
        for i in range(len(SortDigUniqueCombos)):
            SortUnComb = []
            for j in range(self.ndim):
                SortUC = SortCpoints[j, SortDigUniqueCombos[i, j]-1]
                SortUnComb.append(SortUC)
                SortUnicomb = np.asarray(SortUnComb)
            SortUniqueCombos = np.vstack((SortUniqueCombos, SortUnicomb))

        # Output the collocation points
        if self.sampling_method == 'LSCM':
            OptimalCollocationPointsBase = SortUniqueCombos
        else:
            OptimalCollocationPointsBase = SortUniqueCombos[0:self.NrSamples]

        return OptimalCollocationPointsBase
