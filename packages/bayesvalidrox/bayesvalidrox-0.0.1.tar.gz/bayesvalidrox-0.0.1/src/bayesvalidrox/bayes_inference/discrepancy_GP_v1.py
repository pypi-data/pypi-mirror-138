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
    
    def fit_bias(self, BiasInputs, ED_Y, Data):
        print('')
        self.BiasInputs = BiasInputs
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
            kernel = Matern(length_scale=1.0, length_scale_bounds=(1e-15, 1e5),
                                nu=0.5)
            # kernel = RBF(length_scale=1.0, length_scale_bounds=(1e-15, 1e5))
            for i, y in enumerate(ED_Y[out]):
            
                # Prepare the input matrix
                D = np.hstack((BiasInputs[out],y.reshape(-1,1)))
                
                scale[i] = MinMaxScaler()
                D_T = scale[i].fit_transform(D)

                # Prepare data Remove NaN
                try:
                    data = Data[out].to_numpy()[~np.isnan(Data[out])]
                except:
                    data = Data[out][~np.isnan(Data[out])]
                
                # Initiate the GPR class
                gp[i] = GaussianProcessRegressor(kernel=np.var(data)*kernel, n_restarts_optimizer=5,
                                                 alpha = 1e-15,
                                                 normalize_y=False, random_state=5)

                # Fit the GPR
                gp[i].fit(D_T, data)

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
    
    def oldpredict(self,Y,Output,BiasInputs=None,return_cov=True):
        Y = np.atleast_2d(Y)
        BiasInputs = self.BiasInputs if BiasInputs is None else BiasInputs
        D_new = np.hstack((BiasInputs[Output],Y.reshape(-1,1)))
        
        return self.best_gp[Output].predict(D_new,return_cov=return_cov)
        
    def predict(self,Y,Output,BiasInputs=None,return_cov=True):
        Y = np.atleast_2d(Y)
        BiasInputs = self.BiasInputs if BiasInputs is None else BiasInputs
        all_gp = self.all_gp[Output]
        all_scale = self.all_scales[Output]
        D_new = np.hstack((BiasInputs[Output],Y.reshape(-1,1)))
        def predict_GPE(args):
            (idx,gp),weight = args
            D_new_T = all_scale[idx].transform(D_new)
            return gp.predict(D_new_T,return_cov=True) 
        map_f = map(predict_GPE, zip(list(all_gp.items()),self.norm_weights[Output]))
        all_results = list(map_f)

        if not return_cov:
            y_hat = np.mean(np.array(all_results),axis=0)
            return y_hat
        else:
            formatting_function = np.vectorize(lambda f: format(f, '6.2E'))
            # print(formatting_function(np.array([predict[0] for predict in all_results])))
            y_hat = np.average(np.array([predict[0] for predict in all_results]),axis=0,
                               weights=self.norm_weights[Output])
            
            # Equation 13c Gardner et al. (2021)
            y_hats = np.array([predict[0] for predict in all_results])
            covs = np.array([predict[1] for predict in all_results])
            cov=0
            print(formatting_function(covs))
            for cov_,y_ in zip(covs,y_hats):
                cov += cov_ + np.dot( y_.reshape(-1,1), y_.reshape(1,-1))
            cov /= len(covs)
            cov -= np.dot(y_hat.reshape(-1,1),y_hat.reshape(1,-1))
            
            return y_hat.reshape(1,-1), cov