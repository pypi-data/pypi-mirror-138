#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class offers helper functions for post-processing the metamodels.

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
import os
from itertools import combinations, cycle
import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
SIZE = 30
plt.rc('figure', figsize=(24, 16))
plt.rc('font', family='serif', serif='Arial')
plt.rc('font', size=SIZE)
plt.rc('axes', grid=True)
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


class PostProcessing:
    def __init__(self, PCEModel, Name='calib'):
        self.PCEModel = PCEModel
        self.Name = Name
        self.PCEMeans = {}
        self.PCEStd = {}
        self.NrofSamples = None
        self.Samples = []
        self.Samplesu = []
        self.ModelOutputs = {}
        self.PCEOutputs = []
        self.PCEOutputs_std = []
        self.sobol_cell = {}
        self.total_sobol = {}
        self.Likelihoods = []

    # -------------------------------------------------------------------------
    def PCEMoments(self):
        
        PCEModel = self.PCEModel
        Model = PCEModel.ModelObj 
        
        for Outkey, ValuesDict in PCEModel.coeffs_dict.items():
            
            PCEMean = np.zeros((len(ValuesDict)))
            PCEVar = np.zeros((len(ValuesDict)))
            
            for Inkey, InIdxValues in ValuesDict.items():
                idx = int(Inkey.split('_')[1]) - 1
                coeffs = PCEModel.coeffs_dict[Outkey][Inkey]
                
                # Mean = c_0
                PCEMean[idx] = coeffs[0] if coeffs[0]!=0 else PCEModel.clf_poly[Outkey][Inkey].intercept_
                # Var = sum(coeffs[1:]**2)
                PCEVar[idx] = np.sum(np.square(coeffs[1:]))
            
            if PCEModel.dim_red_method.lower() == 'pca':
                PCA = PCEModel.pca[Outkey]
                self.PCEMeans[Outkey] = PCA.mean_ + np.dot(PCEMean, PCA.components_)
                self.PCEStd[Outkey] = np.sqrt(np.dot(PCEVar, PCA.components_**2))
            else:
                self.PCEMeans[Outkey] = PCEMean
                self.PCEStd[Outkey] = np.sqrt(PCEVar)
        try:  
            self.Reference = Model.read_mc_reference()
        except:
            pass
        
    # -------------------------------------------------------------------------
    def plotMoments(self, xlabel='Time [s]', plotType=None, SaveFig=True):

        barPlot = True if plotType == 'bar' else False
        metaModel = self.PCEModel.meta_model_type

        # Set the x values
        x_values_orig = self.PCEModel.ExpDesign.x_values

        # Compute the moments with the PCEModel object
        self.PCEMoments()

        # Get the variables
        Keys = list(self.PCEMeans.keys())

        # Open a pdf for the plots
        if SaveFig:
            newpath = (f'Outputs_PostProcessing_{self.Name}/')
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # create a PdfPages object
            pdf = PdfPages(f'./{newpath}Mean_Std_PCE.pdf')

        # Plot the best fit line, set the linewidth (lw), color and
        # transparency (alpha) of the line
        for idx, key in enumerate(Keys):
            fig, ax = plt.subplots(nrows=1, ncols=2)

            # Extract mean and std
            mean_data = self.PCEMeans[key]
            std_data = self.PCEStd[key]

            # Extract a list of x values
            if type(x_values_orig) is dict:
                x = x_values_orig[key]
            else:
                x = x_values_orig

            # Plot: bar plot or line plot
            if barPlot:
                ax[0].bar(list(map(str, x)), mean_data, color='b',
                          width=0.25)
                ax[1].bar(list(map(str, x)), std_data, color='b',
                          width=0.25)
                ax[0].legend(labels=[metaModel])
                ax[1].legend(labels=[metaModel])
            else:
                ax[0].plot(x, mean_data, lw=3, color='k', marker='x',
                           label=metaModel)
                ax[1].plot(x, std_data, lw=3, color='k', marker='x',
                           label=metaModel)

            if hasattr(self, 'Reference'):
                if barPlot:
                    ax[0].bar(list(map(str, x)), self.Reference['mean'],
                              color='r', width=0.25)
                    ax[1].bar(list(map(str, x)), self.Reference['std'],
                              color='r', width=0.25)
                    ax[0].legend(labels=[metaModel])
                    ax[1].legend(labels=[metaModel])
                else:
                    ax[0].plot(x, self.Reference['mean'], lw=3, marker='x',
                               color='r', label='Ref.')
                    ax[1].plot(x, self.Reference['std'], lw=3, marker='x',
                               color='r', label='Ref.')

            # Label the axes and provide a title
            ax[0].set_xlabel(xlabel)
            ax[1].set_xlabel(xlabel)
            ax[0].set_ylabel(Keys[idx])
            ax[1].set_ylabel(Keys[idx])

            # Provide a title
            ax[0].set_title('Mean of ' + key)
            ax[1].set_title('Std of ' + key)

            if not barPlot:
                ax[0].legend(loc='best')
                ax[1].legend(loc='best')

            plt.tight_layout()

            if SaveFig:
                # save the current figure
                pdf.savefig(fig, bbox_inches='tight')

                # Destroy the current plot
                plt.clf()

        pdf.close()

    # -------------------------------------------------------------------------
    def get_Sample(self):
        
        PCEModel = self.PCEModel
        
        NrSamples = self.NrofSamples
        
        self.Samples = PCEModel.ExpDesign.generate_samples(NrSamples, 'random')

        return self.Samples
    
    # -------------------------------------------------------------------------
    def eval_PCEmodel_3D(self, SaveFig=True):
        
        self.NrofSamples = 1000
        
        PCEModel = self.PCEModel
        Model = self.PCEModel.ModelObj
        NrofSamples = self.NrofSamples
        
        
        # Create 3D-Grid
        # TODO: Make it general
        x = np.linspace(-5, 10, NrofSamples)
        y = np.linspace(0, 15, NrofSamples)

    
        X, Y = np.meshgrid(x, y)
        PCE_Z = np.zeros((self.NrofSamples, self.NrofSamples))
        Model_Z = np.zeros((self.NrofSamples, self.NrofSamples))
                
        for idxMesh in range(self.NrofSamples):
            
            SampleMesh = np.vstack((X[:,idxMesh], Y[:,idxMesh])).T
        
            
            
            univ_p_val = PCEModel.univ_basis_vals(SampleMesh)
        
            for Outkey, ValuesDict in PCEModel.coeffs_dict.items():
                
                
                
                
                PCEOutputs_mean = np.zeros((len(SampleMesh), len(ValuesDict)))
                PCEOutputs_std = np.zeros((len(SampleMesh), len(ValuesDict)))
                ModelOutputs = np.zeros((len(SampleMesh), len(ValuesDict)))
                
                for Inkey, InIdxValues in ValuesDict.items():
                    idx = int(Inkey.split('_')[1]) - 1
                    PolynomialDegrees = PCEModel.basis_dict[Outkey][Inkey]
                    clf_poly = PCEModel.clf_poly[Outkey][Inkey]
                    
                    PSI_Val = PCEModel.PCE_create_Psi(PolynomialDegrees, univ_p_val)
                    # Perdiction with error bar 
                    y_mean, y_std = clf_poly.predict(PSI_Val, return_std=True)
                    
                    PCEOutputs_mean[:, idx] = y_mean
                    PCEOutputs_std[:, idx] = y_std
                    
                    # Model evaluation
                    ModelOutputsDict, _ = Model.run_model_parallel(SampleMesh, keyString='Valid3D')
                    ModelOutputs[:,idx]= ModelOutputsDict[Outkey].T
                    
                    
                PCE_Z[:,idxMesh] = y_mean
                Model_Z[:,idxMesh] =  ModelOutputs[:,0] 
        # ---------------- 3D plot for PCEModel -----------------------
        from mpl_toolkits import mplot3d
        fig_PCE = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, PCE_Z, rstride=1, cstride=1,
                         cmap='viridis', edgecolor='none')
        ax.set_title('PCEModel');
        ax.set_xlabel('$x_1$')
        ax.set_ylabel('$x_2$')
        ax.set_zlabel('$f(x_1,x_2)$');

        plt.grid()
        plt.show()
        
        if SaveFig:
            #  Saving the figure
            newpath = (r'Outputs_PostProcessing_{0}/'.format(self.Name)) 
            if not os.path.exists(newpath): os.makedirs(newpath)
            
            # 3D-plot PCEModel
            fig_PCE.savefig('./'+newpath+'/3DPlot_PCEModel.pdf', format="pdf",
                        bbox_inches='tight')   # save the figure to file
            plt.close(fig_PCE)
        
        # ---------------- 3D plot for Model -----------------------
        fig_Model = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, PCE_Z, rstride=1, cstride=1,
                         cmap='viridis', edgecolor='none')
        ax.set_title('Model');
        ax.set_xlabel('$x_1$')
        ax.set_ylabel('$x_2$')
        ax.set_zlabel('$f(x_1,x_2)$');
        
        
        plt.grid()
        plt.show()
        
        if SaveFig is True:
            # ---------------- Saving the figure and text files -----------------------
            # 3D-plot Model
            fig_Model.savefig('./'+newpath+'/3DPlot_Model.pdf', format="pdf",
                        bbox_inches='tight')   # save the figure to file
            plt.close(fig_Model)
        
        return
    
    
    # -------------------------------------------------------------------------
    def eval_Model(self, Samples=None, keyString='Valid'):
        """
        Evaluate Forward Model
        
        """
        Model = self.PCEModel.ModelObj
        
        if Samples is None:
            Samples = self.get_Sample()
            self.Samples = Samples
        else:
            Samples = Samples
            self.NrofSamples = len(Samples)

        ModelOutputs,  CollocationPoints = Model.run_model_parallel(Samples, keyString=keyString)
        
        self.ModelOutputs = ModelOutputs
        
        return self.ModelOutputs
    
    # -------------------------------------------------------------------------
    def validMetamodel(self, nValidSamples=1, samples=None, x_axis="Time [s]"):
        """
        Evaluate the meta model and the PCEModel
        """
        metaModel = self.PCEModel
        
        if samples is None:
            self.NrofSamples = nValidSamples
            samples = self.get_Sample()
        else:
            self.NrofSamples = samples.shape[0]
        
        
        x_values = self.PCEModel.ExpDesign.x_values
        
        self.ModelOutputs = self.eval_Model(samples, keyString='valid')
        self.PCEOutputs, self.PCEOutputs_std = metaModel.eval_metamodel(samples=samples)
        
        try:
            key = list(self.ModelOutputs.keys())[1]
        except:
            key = list(self.ModelOutputs.keys())[0]
            
        NrofOutputs = self.ModelOutputs[key].shape[1]
        
        if NrofOutputs == 1:
            self.plotValidation()
        else:
            self.plotValidationMulti(x_values=x_values, x_axis=x_axis)
                
    # -------------------------------------------------------------------------
    def accuracyCheckMetaModel(self, nSamples=None, Samples=None, validOutputsDict=None):
        """
        Evaluate the relative error of the PCEModel
        """
        metaModel = self.PCEModel
        
        # Set the number of samples
        self.NrofSamples = nSamples if nSamples is not None else Samples.shape[0]
        
        # Generate random samples
        Samples = self.get_Sample() if Samples is None else Samples
        
        # Run the original model with the generated samples
        ModelOutputs = self.eval_Model(Samples, keyString='validSet') if validOutputsDict is None else validOutputsDict

        # Run the PCE model with the generated samples
        PCEOutputs, PCEOutputs_std = metaModel.eval_metamodel(samples=Samples)

        self.RMSE = {}
        self.validErr = {}
        # Loop over the keys and compute RMSE error.
        for key in list(ModelOutputs.keys())[1:]:
            
            self.RMSE[key] = mean_squared_error(ModelOutputs[key], PCEOutputs[key], squared=False, multioutput='raw_values')

            self.validErr[key] = (self.RMSE[key]**2 / self.NrofSamples) / \
                np.var(ModelOutputs[key],ddof=1, axis=0)
            
            # Print a report table
            print("\n>>>>> Errors of {} <<<<<".format(key))
            print("\nIndex  |  RMSE   |  Validation Error")
            print('-'*35)
            print('\n'.join('{0}  |  {1:.3e}  |  {2:.3e}'.format(i+1,k,j) for i,(k,j) \
                            in enumerate(zip(self.RMSE[key], self.validErr[key]))))
        # Save error dicts in PCEModel object
        self.PCEModel.RMSE = self.RMSE
        self.PCEModel.validErr = self.validErr
        
    # -------------------------------------------------------------------------
    def plotValidation(self, SaveFig=True):
        """

        """
        PCEModel = self.PCEModel
        
        
        # get the samples
        X_Val = self.Samples
        
        
        Y_PC_Val = self.PCEOutputs
        Y_Val = self.ModelOutputs
        
        # Open a pdf for the plots
        if SaveFig:
            newpath = (r'Outputs_PostProcessing_{0}/'.format(self.Name))
            if not os.path.exists(newpath): os.makedirs(newpath)
            
            # create a PdfPages object
            pdf1 = PdfPages('./'+newpath+'/Model_vs_PCEModel.pdf')
            
        fig = plt.figure()
        # Fit the data(train the model)
        for key in Y_PC_Val.keys():
        
            Y_PC_Val_ = Y_PC_Val[key]
            Y_Val_ = Y_Val[key]
            
            regression_model = LinearRegression()
            regression_model.fit(Y_PC_Val_, Y_Val_)
            
            # Predict
            x_new = np.linspace(np.min(Y_PC_Val_), np.max(Y_Val_), 100)
            y_predicted = regression_model.predict(x_new[:, np.newaxis])
            
            plt.scatter(Y_PC_Val_, Y_Val_, color='gold', linewidth=2)
            plt.plot(x_new, y_predicted, color = 'k')
            
            # Calculate the adjusted R_squared and RMSE
            # the total number of explanatory variables in the model (not including the constant term)
            length_list = [len(value) for Key, value in PCEModel.basis_dict[key].items()]
            NofPredictors = min(length_list)
            TotalSampleSize = X_Val.shape[0] #sample size
            
            R2 = r2_score(Y_PC_Val_, Y_Val_)
            AdjR2 = 1 - (1 - R2) * (TotalSampleSize - 1)/(TotalSampleSize - NofPredictors - 1)
            RMSE = np.sqrt(mean_squared_error(Y_PC_Val_, Y_Val_))
            
            plt.annotate('RMSE = '+ str(round(RMSE, 3)) + '\n' + r'Adjusted $R^2$ = '+ str(round(AdjR2, 3)), xy=(0.05, 0.85), xycoords='axes fraction')
        
            plt.ylabel("Original Model")
            plt.xlabel("PCE Model")
            
            plt.grid()
            plt.show()
   
            if SaveFig:
                # save the current figure
                pdf1.savefig(fig, bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
            
        # Close the pdfs            
        pdf1.close()

    # -------------------------------------------------------------------------
    def regQualityCheck(self, nValidSamples=1000, samples=None, SaveFig=True):
        """
        1) https://towardsdatascience.com/how-do-you-check-the-quality-of-your-regression-model-in-python-fa61759ff685

        """
        metaModel = self.PCEModel
        
        if samples is None:
            self.NrofSamples = nValidSamples
            samples = self.get_Sample()
        else:
            self.NrofSamples = samples.shape[0]
        
        
        # Evaluate the original and the surrogate model
        Y_Val = self.eval_Model(samples, keyString='valid')
        Y_PC_Val, _ = metaModel.eval_metamodel(samples=samples,name=self.Name)

        # Open a pdf for the plots
        if SaveFig:
            newpath = (r'Outputs_PostProcessing_{0}/'.format(self.Name))
            if not os.path.exists(newpath): os.makedirs(newpath)
            
        # Fit the data(train the model)
        for key in Y_PC_Val.keys():
        
            Y_PC_Val_ = Y_PC_Val[key]
            Y_Val_ = Y_Val[key]
            
            # ------ Residuals vs. predicting variables ------
            # Check the assumptions of linearity and independence
            fig1 = plt.figure()
            plt.title(key+": Residuals vs. predicting variables")
            residuals = Y_Val_ - Y_PC_Val_
            plt.scatter(x=Y_Val_,y=residuals,color='blue',edgecolor='k')
            plt.grid(True)
            xmin=min(Y_Val_)
            xmax = max(Y_Val_)
            plt.hlines(y=0,xmin=xmin*0.9,xmax=xmax*1.1,color='red',linestyle='--',lw=3)
            plt.xlabel(key)
            plt.ylabel('Residuals')
            plt.show()
            
            if SaveFig:
                # save the current figure
                fig1.savefig('./'+newpath+'/Residuals_vs_PredVariables.pdf', bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
            
            # ------ Fitted vs. residuals ------
            # Check the assumptions of linearity and independence
            fig2 = plt.figure()
            plt.title(key+": Residuals vs. predicting variables")
            residuals = Y_Val_ - Y_PC_Val_
            plt.scatter(x=Y_PC_Val_,y=residuals,color='blue',edgecolor='k')
            plt.grid(True)
            xmin=min(Y_Val_)
            xmax = max(Y_Val_)
            plt.hlines(y=0,xmin=xmin*0.9,xmax=xmax*1.1,color='red',linestyle='--',lw=3)
            plt.xlabel(key)
            plt.ylabel('Residuals')
            plt.show()

            if SaveFig:
                # save the current figure
                fig2.savefig('./'+newpath+'/Fitted_vs_Residuals.pdf', bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
                
            # ------ Histogram of normalized residuals ------
            fig3 = plt.figure()
            resid_pearson = residuals / (max(residuals)-min(residuals))
            plt.hist(resid_pearson,bins=20,edgecolor='k')
            plt.ylabel('Count')
            plt.xlabel('Normalized residuals')
            plt.title(key+": Histogram of normalized residuals")
            
            # Normality (Shapiro-Wilk) test of the residuals
            ax = plt.gca()
            _,p=stats.shapiro(residuals)
            if p<0.01:
                annText= "The residuals seem to come from Gaussian process."
            else:
                annText= "The normality assumption may not hold."
            from matplotlib.offsetbox import AnchoredText
            at = AnchoredText(annText,
                              prop=dict(size=30), frameon=True,
                              loc='upper left',
                              )
            at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
            ax.add_artist(at)
            
            plt.show()
            
            if SaveFig:
                # save the current figure
                fig3.savefig('./'+newpath+'/Hist_NormResiduals.pdf', bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
            
            # ------ Q-Q plot of the normalized residuals ------
            from statsmodels.graphics.gofplots import qqplot
            plt.figure()
            fig4=qqplot(resid_pearson,line='45',fit='True')
            plt.xticks()
            plt.yticks()
            plt.xlabel("Theoretical quantiles")
            plt.ylabel("Sample quantiles")
            plt.title(key+": Q-Q plot of normalized residuals")
            plt.grid(True)
            plt.show()
            
            if SaveFig:
                # save the current figure
                fig4.savefig('./'+newpath+'/QQPlot_NormResiduals.pdf', bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
        
    # -------------------------------------------------------------------------
    def plotValidationMulti(self, x_values=[], x_axis="x [m]", SaveFig=True):
        
        Model = self.PCEModel.ModelObj
        
        if SaveFig:
            newpath = (r'Outputs_PostProcessing_{0}/'.format(self.Name))
            if not os.path.exists(newpath): os.makedirs(newpath)
            
            # create a PdfPages object
            pdf = PdfPages('./'+newpath+'/Model_vs_PCEModel.pdf')

        # List of markers and colors
        color = cycle((['b', 'g', 'r', 'y', 'k']))
        marker = cycle(('x', 'd', '+', 'o', '*')) 
        
        
        Y_PC_Val = self.PCEOutputs
        Y_PC_Val_std =  self.PCEOutputs_std
        
        Y_Val = self.ModelOutputs

        OutNames = list(Y_Val.keys())
        if len(OutNames) == 1: OutNames.insert(0, x_axis)
        try:
            x_values =  Y_Val[OutNames[0]]
        except:
            x_values =  x_values
        
        fig = plt.figure(figsize=(24, 16))
        
        # Plot the model vs PCE model
        for keyIdx, key in enumerate(OutNames[1:]):

            Y_PC_Val_ = Y_PC_Val[key]
            Y_PC_Val_std_ = Y_PC_Val_std[key]
            Y_Val_ = Y_Val[key]
            try:
                x = x_values[key]
            except:
                x = x_values
            
            for idx in range(Y_Val_.shape[0]):
                Color = next(color)
                Marker = next(marker)
                
                plt.plot(x, Y_Val_[idx,:], color=Color, marker=Marker, label='$Y_{%s}^{M}$'%(idx+1))
                
                plt.plot(x, Y_PC_Val_[idx,:], color=Color, marker=Marker, linestyle='--', label='$Y_{%s}^{PCE}$'%(idx+1))
                plt.fill_between(x, Y_PC_Val_[idx,:]-1.96*Y_PC_Val_std_[idx,:], 
                                 Y_PC_Val_[idx,:]+1.96*Y_PC_Val_std_[idx,:], color=Color,alpha=0.15)
            
            # Calculate the RMSE
            RMSE = mean_squared_error(Y_PC_Val_, Y_Val_, squared=False)
            R2 = r2_score(Y_PC_Val_[idx,:].reshape(-1,1), Y_Val_[idx,:].reshape(-1,1))
            
            plt.annotate('RMSE = '+ str(round(RMSE, 3)) + '\n' + r'$R^2$ = '+ str(round(R2, 3)),
                         xy=(0.2, 0.75), xycoords='axes fraction')
        
            
            plt.ylabel(key)
            plt.xlabel(x_axis)
            plt.legend(loc='best')
            plt.grid()
            
            #plt.show()
            
            if SaveFig:
                # save the current figure
                pdf.savefig(fig, bbox_inches='tight')
                
                # Destroy the current plot
                plt.clf()
                
        pdf.close()
        
        # Cleanup
        #Zip the subdirectories
        try:
            dir_name = Model.name + 'valid'
            key = dir_name + '_'
            Model.zip_subdirs(dir_name, key)
        except:
            pass
    
    # -------------------------------------------------------------------------
    def seqDesignDiagnosticPlots(self, refBME_KLD=None, SaveFig=True):
        """
        Plot the Kullback-Leibler divergence in the sequential design.
        
        """
        PCEModel = self.PCEModel
        NrofInitSamples = PCEModel.ExpDesign.n_init_samples
        totalNSamples = PCEModel.ExpDesign.X.shape[0]
        
        if SaveFig:
            newpath = (r'Outputs_PostProcessing_{0}/'.format(self.Name))
            if not os.path.exists(newpath): os.makedirs(newpath)
            
            # create a PdfPages object
            pdf = PdfPages('./'+newpath+'/seqPCEModelDiagnostics.pdf')
        
        plotList = ['Modified LOO error', 'Validation error', 'KLD', 'BME', 
                    'RMSEMean', 'RMSEStd', 'Hellinger distance']
        seqList = [PCEModel.SeqModifiedLOO,PCEModel.seqValidError, PCEModel.SeqKLD,
                   PCEModel.SeqBME, PCEModel.seqRMSEMean, PCEModel.seqRMSEStd,
                   PCEModel.SeqDistHellinger]
        
        markers = ('x', 'o', 'd', '*', '+')
        colors = ('k', 'darkgreen', 'b', 'navy', 'darkred')
        
        # Plot the evolution of the diagnostic criteria of the Sequential Experimental Design.
        for plotidx, plot in enumerate(plotList): 
            fig, ax = plt.subplots()
            SeqDict = seqList[plotidx]
            nameUtil = list(SeqDict.keys())
            
            if len(nameUtil) == 0:
                continue
            
            # Box plot when Replications have been detected.
            if any(int(name.split("rep_",1)[1])>1 for name in nameUtil):
                # Extract the values from dict
                sortedSeqOpt = {}
                # Number of replications
                nReps = PCEModel.ExpDesign.nReprications
                
                # Get the list of utility function names
                # Handle if only one UtilityFunction is provided
                if not isinstance(PCEModel.ExpDesign.UtilityFunction, list): 
                    UtilFuncs = [PCEModel.ExpDesign.UtilityFunction]
                else:
                    UtilFuncs = PCEModel.ExpDesign.UtilityFunction
                
                for keyOpt in UtilFuncs:
                    sortedSeq = {}
                    # min number of runs available from reps
                    nRuns = min([SeqDict[keyOpt +'_rep_'+str(i+1)].shape[0] for i in range(nReps)]) 
                    
                    for runIdx in range(nRuns):
                        values = []
                        for key in SeqDict.keys():
                            if keyOpt in key:
                                values.append(SeqDict[key][runIdx].mean())
                        sortedSeq['SeqItr_'+str(runIdx)]  = np.array(values)
                    sortedSeqOpt[keyOpt] = sortedSeq
                
                # BoxPlot
                def draw_plot(data, labels, edge_color, fill_color, idx):
                    pos = labels - (idx-1)
                    bp = plt.boxplot(data, positions=pos, labels=labels,
                                     patch_artist=True , sym='', widths=0.75)
                    
                    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
                        plt.setp(bp[element], color=edge_color[idx])
                
                    for patch in bp['boxes']:
                        patch.set(facecolor=fill_color[idx])
                    
                    
                step1 = PCEModel.ExpDesign.n_new_samples if PCEModel.ExpDesign.n_new_samples!=1 else 5
                step2 = 1 if PCEModel.ExpDesign.n_new_samples!=1 else 5
                edge_color = ['red', 'blue', 'green']
                fill_color = ['tan', 'cyan', 'lightgreen']
                
                plotLabel = plot
                # Plot for different Utility Functions
                for idx, util in enumerate(UtilFuncs):
                    allErrors = np.empty((nReps, 0))
                    
                    for key in list(sortedSeqOpt[util].keys()):
                        allErrors = np.hstack((allErrors, sortedSeqOpt.get(util, {}).get(key)[:,None]))
                    
                    # Special cases for BME and KLD
                    if plot == 'KLD' or plot == 'BME':
                        # BME convergence if refBME is provided
                        if refBME_KLD is not None:
                            if plot == 'BME': refValue, plotLabel = refBME_KLD[0], r'$BME/BME^{Ref.}$'
                            if plot == 'KLD': refValue, plotLabel = refBME_KLD[1], r'$D_{KL}[p(\theta|y_*),p(\theta)] / D_{KL}^{Ref.}[p(\theta|y_*), p(\theta)]$'
                            
                            # Difference between BME/KLD and the ref. values
                            allErrors = np.divide(allErrors,np.full((allErrors.shape), refValue))

                            # Plot baseline for zero, i.e. no difference
                            plt.axhline(y=1.0, xmin=0, xmax=1, c='green', ls='--', lw=2)
                    
                    # Plot each UtilFuncs
                    labels = np.arange(NrofInitSamples, totalNSamples+1, step1)
                    draw_plot(allErrors[:,::step2], labels, edge_color, fill_color, idx)
                 
                plt.xticks(labels, labels)
                # Set the major and minor locators
                ax.xaxis.set_major_locator(ticker.AutoLocator())
                ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
                ax.xaxis.grid(True, which='major', linestyle='-')
                ax.xaxis.grid(True, which='minor', linestyle='--')
                
                from matplotlib.patches import Patch
                legend_elements = [Patch(facecolor=fill_color[idx], edgecolor=edge_color[idx],
                                         label=util) for idx,util in enumerate(UtilFuncs)]
                plt.legend(handles=legend_elements[::-1], loc='best')
                
                if plot != 'BME' and plot != 'KLD': plt.yscale('log')
                plt.autoscale(True)
                plt.xlabel('\# of training samples')
                plt.ylabel(plotLabel)
                plt.title(plot)
                
                if SaveFig:
                    # save the current figure
                    pdf.savefig(fig, bbox_inches='tight')
                    
                    # Destroy the current plot
                    plt.clf()
                    
                    # Save arrays into files
                    #np.savetxt('./'+newpath+'/Seq'+plot+'.txt', sortedSeqOpt)
                    f = open('./'+newpath+'/Seq'+plot+'.txt',"w")
                    f.write( str(sortedSeqOpt) )
                    f.close()
                
                
            else:    
                # fig,ax = plt.subplots()
                
                for idx, name in enumerate(nameUtil):
                    SeqValues = SeqDict[name]
                    step = PCEModel.ExpDesign.n_new_samples if PCEModel.ExpDesign.n_new_samples!=1 else 1
                    x_idx = np.arange(NrofInitSamples, totalNSamples+1, step)
                    x_idx = np.hstack((x_idx, totalNSamples)) if totalNSamples not in x_idx else x_idx

                    if plot == 'KLD' or plot == 'BME':
                        # BME convergence if refBME is provided
                        if refBME_KLD is not None:
                            if plot == 'BME': refValue, plotLabel = refBME_KLD[0], r'$BME/BME^{Ref.}$'
                            if plot == 'KLD': refValue, plotLabel = refBME_KLD[1], r'$D_{KL}[p(\theta|y_*),p(\theta)] / D_{KL}^{Ref.}[p(\theta|y_*), p(\theta)]$'
                            
                            # Difference between BME/KLD and the ref. values
                            values = np.divide(SeqValues,np.full((SeqValues.shape), refValue))
                                
                            # Plot baseline for zero, i.e. no difference
                            plt.axhline(y=1.0, xmin=0, xmax=1, c='green', ls='--', lw=2)
                            
                            # Set the limits
                            plt.ylim([1e-1, 1e1])
                            
                            # Create the plots
                            plt.semilogy(x_idx, values, marker=markers[idx], color=colors[idx],
                                 ls='--', lw=2, label=name.split("_rep",1)[0])
                        else:
                            plotLabel = plot
                        
                            # Create the plots
                            plt.plot(x_idx, SeqValues, marker=markers[idx], color=colors[idx],
                                     ls='--', lw=2, label=name.split("_rep",1)[0])
                        
                        
                    else:
                        plotLabel = plot
                        SeqValues = np.nan_to_num(SeqValues)
                        
                        # Plot the error evolution for each output
                        for i in range(SeqValues.shape[1]):
                            plt.semilogy(x_idx, SeqValues[:,i], marker=markers[idx],
                                      ls='--', lw=2, color=colors[idx], alpha=0.15)
                        
                        plt.semilogy(x_idx, SeqValues, marker=markers[idx],
                                     ls='--', lw=2, color=colors[idx], label=name.split("_rep",1)[0])
                        
                        
                # Set the major and minor locators
                ax.xaxis.set_major_locator(ticker.AutoLocator())
                ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
                ax.xaxis.grid(True, which='major', linestyle='-')
                ax.xaxis.grid(True, which='minor', linestyle='--')
                
                ax.tick_params(axis='both', which='major', direction='in', width=3, length=10)
                ax.tick_params(axis='both', which='minor', direction='in', width=2, length=8)
                
                plt.xlabel('Number of runs')
                plt.ylabel(plotLabel)
                plt.title(plot)
                plt.legend(frameon=True)
            
                
                if SaveFig:
                    # save the current figure
                    pdf.savefig(fig, bbox_inches='tight')
                    
                    # Destroy the current plot
                    plt.clf()

                    # ---------------- Saving arrays into files ---------------
                    np.save('./'+newpath+'/Seq'+plot+'.npy', SeqValues)
                
        # Close the pdf
        pdf.close()
        return
    
    # -------------------------------------------------------------------------
    def sobolIndicesPCE(self, xlabel='Time [s]', plotType=None, SaveFig=True):
        """
        Provides Sobol indices as a sensitivity measure to infer the importance
        of the input parameters. See Eq. 27 in [1] for more details.

        1. Global sensitivity analysis: A flexible and efficient framework with
        an example from stochastic hydrogeology S. Oladyshkin, F.P. de Barros,
        W. Nowak  https://doi.org/10.1016/j.advwatres.2011.11.001

        2. Nagel, J.B., Rieckermann, J. and Sudret, B., 2020. Principal
        component analysis and sparse polynomial chaos expansions for global
        sensitivity analysis and model calibration: Application to urban
        drainage simulation. Reliability Engineering & System Safety, 195,
        p.106737.
        """
        # Extract the necessary variables
        PCEModel = self.PCEModel
        basis_dict = PCEModel.basis_dict
        coeffs_dict = PCEModel.coeffs_dict
        NofPa = PCEModel.n_params
        max_order = np.max(PCEModel.pce_deg)

        for Output in PCEModel.ModelObj.Output.names:

            n_meas_points = len(coeffs_dict[Output])

            # Initialize the (cell) array containing the (total) Sobol indices.
            sobol_array = dict.fromkeys(range(1, max_order+1), [])
            sobol_cell_array = dict.fromkeys(range(1, max_order+1), [])

            for i_order in range(1, max_order+1):
                n_comb = math.comb(NofPa, i_order)

                sobol_cell_array[i_order] = np.zeros((n_comb, n_meas_points))

            total_sobol_array = np.zeros((NofPa, n_meas_points))

            # Initialize the cell to store the names of the variables
            TotalVariance = np.zeros((n_meas_points))

            # Loop over all measurement points and calculate sobol indices
            for pIdx in range(n_meas_points):

                # Extract the basis indices (alpha) and coefficients
                Basis = basis_dict[Output][f'y_{pIdx+1}']

                try:
                    clf_poly = PCEModel.clf_poly[Output][f'y_{pIdx+1}']
                    PCECoeffs = clf_poly.coef_
                except:
                    PCECoeffs = coeffs_dict[Output][f'y_{pIdx+1}']

                # Compute total variance
                TotalVariance[pIdx] = np.sum(np.square(PCECoeffs[1:]))

                nzidx = np.where(PCECoeffs != 0)[0]
                # Set all the Sobol indices equal to zero in the presence of a
                # null output.
                if len(nzidx) == 0:
                    # This is buggy.
                    for i_order in range(1, max_order+1):
                        sobol_cell_array[i_order][:, pIdx] = 0

                # Otherwise compute them by summing well-chosen coefficients
                else:
                    nz_basis = Basis[nzidx]
                    for i_order in range(1, max_order+1):
                        idx = np.where(np.sum(nz_basis > 0, axis=1) == i_order)
                        subbasis = nz_basis[idx]
                        Z = np.array(list(combinations(range(NofPa), i_order)))

                        for q in range(Z.shape[0]):
                            Zq = Z[q]
                            subsubbasis = subbasis[:, Zq]
                            subidx = np.prod(subsubbasis, axis=1) > 0
                            sum_ind = nzidx[idx[0][subidx]]
                            if TotalVariance[pIdx] == 0.0:
                                sobol_cell_array[i_order][q, pIdx] = 0.0
                            else:
                                sobol = np.sum(np.square(PCECoeffs[sum_ind]))
                                sobol /= TotalVariance[pIdx]
                                sobol_cell_array[i_order][q, pIdx] = sobol

                    # Compute the TOTAL Sobol indices.
                    for ParIdx in range(NofPa):
                        idx = nz_basis[:, ParIdx] > 0
                        sum_ind = nzidx[idx]

                        if TotalVariance[pIdx] == 0.0:
                            total_sobol_array[ParIdx, pIdx] = 0.0
                        else:
                            sobol = np.sum(np.square(PCECoeffs[sum_ind]))
                            sobol /= TotalVariance[pIdx]
                            total_sobol_array[ParIdx, pIdx] = sobol

                # ----- if PCA selected: Compute covariance -----
                if PCEModel.dim_red_method.lower() == 'pca':
                    cov_Z_p_q = np.zeros((NofPa))
                    # Extract the basis indices (alpha) and coefficients for 
                    # next component
                    if pIdx < n_meas_points-1:
                        nextBasis = basis_dict[Output][f'y_{pIdx+2}']

                        try:
                            clf_poly = PCEModel.clf_poly[Output][f'y_{pIdx+2}']
                            nextPCECoeffs = clf_poly.coef_
                        except:
                            nextPCECoeffs = coeffs_dict[Output][f'y_{pIdx+2}']

                        # Choose the common non-zero basis
                        mask = (Basis[:, None] == nextBasis).all(-1).any(-1)
                        similar_basis = Basis[mask]
                        # Compute the TOTAL Sobol indices.
                        for ParIdx in range(NofPa):
                            idx = similar_basis[:, ParIdx] > 0
                            try:
                                sum_is = nzidx[idx]
                                cov_Z_p_q[ParIdx] = np.sum(PCECoeffs[sum_ind] *
                                                           nextPCECoeffs[sum_is])
                            except:
                                cov_Z_p_q[ParIdx] = 0.0

            # Compute the sobol indices according to Ref. 2
            if PCEModel.dim_red_method.lower() == 'pca':
                n_c_points = PCEModel.ExpDesign.Y[Output].shape[1]
                PCA = PCEModel.pca[Output]
                compPCA = PCA.components_
                nComp = compPCA.shape[0]
                var_Z_p = PCA.explained_variance_

                # Extract the sobol index of the components
                for i_order in range(1, max_order+1):
                    n_comb = math.comb(NofPa, i_order)
                    sobol_array[i_order] = np.zeros((n_comb, n_c_points))
                    Z = np.array(list(combinations(range(NofPa), i_order)))

                    for q in range(Z.shape[0]):
                        S_Z_i = sobol_cell_array[i_order][q]

                        for tIdx in range(n_c_points):
                            var_Y_t = np.var(PCEModel.ExpDesign.Y[Output][:, tIdx])
                            if var_Y_t == 0.0:
                                term1, term2 = 0.0, 0.0
                            else:
                                term1 = np.sum([S_Z_i[i]*(var_Z_p[i]*(compPCA[i, tIdx]**2)/var_Y_t) for i in range(nComp)])

                                # Term 2
                                # cov_Z_p_q = np.ones((nComp))# TODO: from coeffs
                                Phi_t_p = compPCA[:nComp-1]
                                Phi_t_q = compPCA
                                term2 = 2 * np.sum([cov_Z_p_q[ParIdx] * Phi_t_p[i,tIdx] * Phi_t_q[i,tIdx]/var_Y_t for i in range(nComp-1)])

                            sobol_array[i_order][q, tIdx] = term1 #+ term2

                # Compute the TOTAL Sobol indices.
                total_sobol = np.zeros((NofPa, n_c_points))
                for ParIdx in range(NofPa):
                    S_Z_i = total_sobol_array[ParIdx]

                    for tIdx in range(n_c_points):
                        var_Y_t = np.var(PCEModel.ExpDesign.Y[Output][:, tIdx])
                        if var_Y_t == 0.0:
                            term1, term2 = 0.0, 0.0
                        else:
                            term1 = 0
                            for i in range(nComp):
                                term1 += S_Z_i[i] * var_Z_p[i] * \
                                    (compPCA[i, tIdx]**2) / var_Y_t

                            # Term 2
                            # cov_Z_p_q = np.ones((nComp))# TODO: from coeffs
                            Phi_t_p = compPCA[:nComp-1]
                            Phi_t_q = compPCA
                            term2 = 0
                            for i in range(nComp-1):
                                term2 += cov_Z_p_q[ParIdx] * Phi_t_p[i, tIdx] \
                                    * Phi_t_q[i, tIdx] / var_Y_t
                            term2 *= 2

                        total_sobol[ParIdx, tIdx] = term1 + term2

                self.sobol_cell[Output] = sobol_array
                self.total_sobol[Output] = total_sobol
            else:
                self.sobol_cell[Output] = sobol_cell_array
                self.total_sobol[Output] = total_sobol_array

        # ---------------- Plot -----------------------
        par_names = PCEModel.ExpDesign.par_names
        x_values_orig = PCEModel.ExpDesign.x_values

        cases = ['']

        for case in cases:
            newpath = (f'Outputs_PostProcessing_{self.Name}/')
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            if SaveFig:
                # create a PdfPages object
                name = case+'_' if 'Valid' in cases else ''
                pdf = PdfPages('./'+newpath+name+'Sobol_indices.pdf')

            fig = plt.figure()

            for outIdx, Output in enumerate(PCEModel.ModelObj.Output.names):

                # Extract total Sobol indices
                total_sobol = self.total_sobol[Output]

                # Extract a list of x values
                if type(x_values_orig) is dict:
                    x = x_values_orig[Output]
                else:
                    x = x_values_orig

                if plotType == 'bar':
                    ax = fig.add_axes([0, 0, 1, 1])
                    dict1 = {xlabel: x}
                    dict2 = {param: sobolIndices for param, sobolIndices
                             in zip(par_names, total_sobol)}

                    df = pd.DataFrame({**dict1, **dict2})
                    df.plot(x=xlabel, y=par_names, kind="bar", ax=ax, rot=0,
                            colormap='Dark2')
                    ax.set_ylabel('Total Sobol indices, $S^T$')

                else:
                    for i, sobolIndices in enumerate(total_sobol):
                        plt.plot(x, sobolIndices, label=par_names[i],
                                 marker='x', lw=2.5)

                    plt.ylabel('Total Sobol indices, $S^T$')
                    plt.xlabel(xlabel)

                plt.title(f'Sensitivity analysis of {Output}')
                if plotType != 'bar':
                    plt.legend(loc='best', frameon=True)

                # Save indices
                np.savetxt(f'./{newpath}{name}totalsobol_' +
                           Output.replace('/', '_') + '.csv',
                           total_sobol.T, delimiter=',',
                           header=','.join(par_names), comments='')

                if SaveFig:
                    # save the current figure
                    pdf.savefig(fig, bbox_inches='tight')

                    # Destroy the current plot
                    plt.clf()

            pdf.close()

        return self.sobol_cell, self.total_sobol
