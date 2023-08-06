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


class Input:
    def __init__(self):
        self.Marginals = []
        self.polycoeffsFlag = True
        self.Rosenblatt = False

    def addMarginals(self):
        self.Marginals.append(Marginal())


# Nested class
class Marginal:
    def __init__(self):
        self.name = None
        self.dist_type = None
        self.moments = None
        self.input_data = []
        self.parameters = [0, 1]
