#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 09:42:33 2021

@author: farid
"""
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern,RBF,RationalQuadratic
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler

class Bias():
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def fit_bias(self, EDX, ED_Y, Data):
        print('')
        outNames = [*ED_Y][1:]
        self.norm_weights = {}
        self.all_gp = {}
        self.all_kernels = {}
        self.best_gp = {}
        self.all_scales = {}
        for out in tqdm(outNames, ascii=True, desc ="Fitting the GPR based bias model"):
            scale = {}
            gp = {}
            kernels = {}
            weights = []
            # Select kernel
            # kernel = Matern(length_scale=1.0, length_scale_bounds=(1e-15, 1e5),
            #                     nu=0.5)
            kernel = RBF(length_scale=1.0, length_scale_bounds=(1e-15, 1e5))
            for i in range(ED_Y[out].shape[1]):
            
                # Prepare the input matrix
                scale[i] = MinMaxScaler()
                EDX_S = scale[i].fit_transform(EDX)

                # Prepare target from data and Remove NaN
                try:
                    data = Data[out].to_numpy()[~np.isnan(Data[out])]
                except:
                    data = Data[out][~np.isnan(Data[out])]
                
                delta = data[i] - ED_Y[out][:,i]
                
                # Initiate the GPR class
                gp[i] = GaussianProcessRegressor(kernel=np.var(data)*kernel, n_restarts_optimizer=5,
                                                 alpha = 1e-15,
                                                 normalize_y=False, random_state=5)

                # Fit the GPR
                gp[i].fit(EDX_S, delta)

                # Save log_marginal_likelihood as a weight
                weights.append(1)
                # weights.append(gp[i].log_marginal_likelihood_value_)
                
                # kernels
                kernels[i] = gp[i].kernel_
                
            # Save GPR objects and normalized weights in dicts
            self.all_scales[out]   = scale
            self.all_gp[out]       = gp
            self.all_kernels[out]  = kernels
            self.norm_weights[out] = weights#/np.max(weights)
            self.best_gp[out]      = gp[np.argmax(weights/np.sum(weights))]
        
        return 
        
    def predict(self,X,Output,return_std=True):
        X = np.atleast_2d(X)
        all_gp = self.all_gp[Output]
        all_scale = self.all_scales[Output]
        def predict_GPE(args):
            (idx,gp),weight = args
            D_new_T = all_scale[idx].transform(X)
            return gp.predict(D_new_T,return_std) 
        map_f = map(predict_GPE, zip(list(all_gp.items()),self.norm_weights[Output]))
        all_results = list(map_f)

        if not return_std:
            y_hat = np.array(all_results).reshape(1,-1)
            return y_hat
        else:
            y_hats = np.array([predict[0] for predict in all_results])
            covs = np.array([predict[1][0]**2 for predict in all_results])

            return y_hats.reshape(1,-1), np.diag(covs)