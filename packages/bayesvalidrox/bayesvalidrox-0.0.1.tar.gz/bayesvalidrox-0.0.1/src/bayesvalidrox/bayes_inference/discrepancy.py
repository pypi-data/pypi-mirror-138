#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discrepancy class for Bayesian inference method

Option A:
    With no explicitly-specified model

Option B:
    With known redidual variance sigma2 (Gaussian or others)

Option C:
    With unknown residual variance sigma2 (Gaussian)
    with given distribution

Author: Farid Mohammadi, M.Sc.
E-Mail: farid.mohammadi@iws.uni-stuttgart.de
Department of Hydromechanics and Modelling of Hydrosystems (LH2)
Institute for Modelling Hydraulic and Environmental Systems (IWS), University
of Stuttgart, www.iws.uni-stuttgart.de/lh2/
Pfaffenwaldring 61
70569 Stuttgart

Created on Mon Sep  2 10:48:35 2019
"""
import scipy.stats as stats
from bayesvalidrox.surrogate_models.exp_designs import ExpDesigns
from bayesvalidrox.surrogate_models.inputs import Input


class Discrepancy:
    def __init__(self, InputDisc):
        self.Type = 'Gaussian'
        self.Parameters = None
        self.Name = 'Sigma2'
        self.Prior = None
        self.Marginals = []
        self.InputDisc = InputDisc
        self.NrofSamples = 10000
        self.Sigma2Prior = None

    def create_inputDisc(self):
        InputClass = Input()
        InputClass.addMarginals()

        return InputClass

    # -------------------------------------------------------------------------
    def get_Sample(self, nSamples):
        self.NrofSamples = nSamples
        ExpDesign = ExpDesigns(self.InputDisc)
        self.Sigma2Prior = ExpDesign.GetSample(nSamples,
                                               SamplingMethod='random',
                                               MaxPceDegree=1)
        # Store BoundTuples
        self.ExpDesign = ExpDesign

        # Naive approach: Fit a gaussian kernel to the provided data
        self.ExpDesign.JDist = stats.gaussian_kde(ExpDesign.raw_data)

        # Save the names of sigmas
        if len(self.InputDisc.Marginals) != 0:
            self.Name = []
            for Marginalidx in range(len(self.InputDisc.Marginals)):
                self.Name.append(self.InputDisc.Marginals[Marginalidx].Name)

        return self.Sigma2Prior

    # -------------------------------------------------------------------------
    def create_Discrepancy(self):

        self.get_Sample()
        return self
