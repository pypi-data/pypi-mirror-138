#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created based on the Surrogate Modeling Toolbox ("SUMO Toolbox")

publication:
>   - A Surrogate Modeling and Adaptive Sampling Toolbox for Computer Based Design
>   D. Gorissen, K. Crombecq, I. Couckuyt, T. Dhaene, P. Demeester,
>   Journal of Machine Learning Research,
>   Vol. 11, pp. 2051-2055, July 2010. 
>
> Contact : sumo@sumo.intec.ugent.be - http://sumo.intec.ugent.be

@author: farid
"""

import numpy as np
import copy
import scipy.stats as stats
from scipy.spatial import distance

from .ExpDesigns import ExpDesigns

class Exploration:
    def __init__(self, PCEModel, NCandidate):
        self.PCEModel = PCEModel
        self.Marginals = []
        self.OldExpDesign = PCEModel.ExpDesign.X
        self.Bounds = PCEModel.BoundTuples
        self.numNewSamples = NCandidate
        self.mcCriterion = 'mc-intersite-proj-th' #'mc-intersite-proj'
        
        self.allCandidates = []
        self.newSamples = []
        
        self.areas = []
        self.closestPoints = []
        self.perc = None
        self.errors = None
    
        self.w = 100
        
    def getExplorationSamples(self):
        """
        This function generates prospective candidates to be selected as new design
        and their associated exploration scores.
        """
        PCEModel = self.PCEModel
        explore_method = PCEModel.ExpDesign.explore_method
        
        if explore_method == 'Voronoi':
            print("\n")
            print(' The Voronoi-based method is selected as the exploration method.')
            print("\n")
            
            # Generate samples using the Voronoi method
            allCandidates, scoreExploration = self.getVornoiSamples()
                
        else:
            print("\n")
            print(f' The {explore_method}-Method is selected as the exploration method.')
            print("\n")
            # Generate samples using the MC method
            allCandidates, scoreExploration = self.getMCSamples()

        return allCandidates, scoreExploration
            
    #--------------------------------------------------------------------------------------------------------
    
    def getVornoiSamples(self):
        
        mcCriterion = self.mcCriterion
        numNewSamples = self.numNewSamples
        # Get the Old ExpDesign #samples
        OldExpDesign = self.OldExpDesign
        ndim = OldExpDesign.shape[1]
        
        # calculate error #averageErrors
        errorVoronoi, allCandidates = self.approximateVoronoi(self.w,OldExpDesign)
        
        
        # get amount of samples
        sortederrorVoronoi = errorVoronoi #np.sort(copy.copy(errorVoronoi))[::-1]
        bestSamples = range(len(errorVoronoi)) #np.argsort(errorVoronoi)[::-1]
        

        # for each best sample, pick the best candidate point in the voronoi cell
        selectedSamples = np.empty((0, ndim))
        badSamples = []
        
        for i, index in enumerate(bestSamples):

            # get candidate new samples from voronoi tesselation
            candidates = self.closestPoints[index]
            
            # get total number of candidates
            nNewSamples = candidates.shape[0]
            
            
            # still no candidate samples around this one, skip it!
            if nNewSamples == 0:
                print('Sample %s skipped because there were no candidate samples around it...'%OldExpDesign[index])
                badSamples.append(index)
                continue
            
            # find candidate that is farthest away from any existing sample
            maxMinDistance = 0
            bestCandidate = 0
            minIntersiteDist = np.zeros((nNewSamples))
            minprojectedDist = np.zeros((nNewSamples))
            
            for j in range(nNewSamples):
                NewSamples = np.vstack((OldExpDesign, selectedSamples))
                # find min distorted distance from all other samples
                euclideanDist = self.buildDistanceMatrixPoint(NewSamples, candidates[j], doSqrt=True)
                mineuclideanDist = np.min(euclideanDist)
                minIntersiteDist[j] = mineuclideanDist
                
                # see if this is the maximal minimum distance from all other samples
                if mineuclideanDist >= maxMinDistance:
                    maxMinDistance = mineuclideanDist
                    bestCandidate = j
                
                # Projected distance
                projectedDist =  distance.cdist(NewSamples, [candidates[j]], 'chebyshev')
                minprojectedDist[j] = np.min(projectedDist)
                
            
            if mcCriterion == 'mc-intersite-proj': 
                weightEuclideanDist = 0.5 * ((nNewSamples+1)**(1/ndim) - 1)
                weightProjectedDist = 0.5 * (nNewSamples+1)
                totalDistScores= weightEuclideanDist * minIntersiteDist + weightProjectedDist * minprojectedDist
            
            elif mcCriterion == 'mc-intersite-proj-th':
                alpha = 0.5 # chosen (tradeoff)
                d_min = 2 * alpha / nNewSamples
                if any(minprojectedDist < d_min):
                    candidates = np.delete(candidates, [minprojectedDist < d_min], axis=0)
                    totalDistScores = np.delete(minIntersiteDist, [minprojectedDist < d_min], axis=0)
                else:
                    totalDistScores = minIntersiteDist
           
            else:
                raise NameError('The MC-Criterion you requested is not available.')
           
            
            # add the best candidate to the list of new samples
            bestCandidate = np.argsort(totalDistScores)[::-1][:numNewSamples]
            selectedSamples = np.vstack((selectedSamples, candidates[bestCandidate]))

            #print('\nBest candidate around sample %s was chosen to be %s, with minDistance %s'%(OldExpDesign[index], candidates[bestCandidate], totalDistScores[bestCandidate]))
            
        self.newSamples = selectedSamples #candidates 
        self.explorationScore = np.delete(sortederrorVoronoi, badSamples, axis=0)
        
        
        return self.newSamples, self.explorationScore    
            
    #--------------------------------------------------------------------------------------------------------

    def getMCSamples(self, allCandidates=None):
        """
        This function generates random samples based on Global Monte Carlo methods
        and their corresponding scores.
        
        Implemented methods to compute scores:
            1) mc-intersite-proj
            2) mc-intersite-proj-th
        
        Based on the following paper:
            Crombecq, K., Laermans, E., & Dhaene, T. (2011). Efficient space-filling and non-collapsing sequential design strategies for simulation-based modeling.
            European Journal of Operational Research, 214(3), 683-696.
            DOI: https://doi.org/10.1016/j.ejor.2011.05.032
        
        """
        PCEModel = self.PCEModel
        explore_method = PCEModel.ExpDesign.explore_method
        mcCriterion = self.mcCriterion
        if allCandidates is None:
            nNewSamples = self.numNewSamples
        else: 
            nNewSamples = allCandidates.shape[0] 
            
        # Get the Old ExpDesign #samples
        OldExpDesign = self.OldExpDesign
        ndim = OldExpDesign.shape[1]
        
        # ----- Compute the number of random points -----
        if allCandidates is None:
            # Generate MC Samples
            allCandidates = PCEModel.ExpDesign.generate_samples(self.numNewSamples,
                                                                explore_method)
        self.allCandidates = allCandidates
        
        # initialization
        newSamples = np.empty((0, ndim))
        minIntersiteDist = np.zeros((nNewSamples))
        minprojectedDist = np.zeros((nNewSamples))
            
        
        for i, candidate in enumerate(allCandidates):
            
            # find candidate that is farthest away from any existing sample
            maxMinDistance = 0
            bestCandidate = 0
            
            
            NewSamples = np.vstack((OldExpDesign, newSamples))
            # find min distorted distance from all other samples
            euclideanDist = self.buildDistanceMatrixPoint(NewSamples, candidate, doSqrt=True)
            mineuclideanDist = np.min(euclideanDist)
            minIntersiteDist[i] = mineuclideanDist
            
            # see if this is the maximal minimum distance from all other samples
            if mineuclideanDist >= maxMinDistance:
                maxMinDistance = mineuclideanDist
                bestCandidate = i
            
            # Projected distance
            projectedDist =  distance.cdist(NewSamples, [candidate], 'chebyshev')
            minprojectedDist[i] = np.min(projectedDist)
                
            
        if mcCriterion == 'mc-intersite-proj': 
            weightEuclideanDist = ((nNewSamples+1)**(1/ndim) - 1) * 0.5
            weightProjectedDist = (nNewSamples+1) * 0.5
            totalDistScores= weightEuclideanDist * minIntersiteDist + weightProjectedDist * minprojectedDist
        
        elif mcCriterion == 'mc-intersite-proj-th':
            alpha = 0.5 # chosen (tradeoff)
            d_min = 2 * alpha / nNewSamples
            if any(minprojectedDist < d_min):
                allCandidates = np.delete(allCandidates, [minprojectedDist < d_min], axis=0)
                totalDistScores = np.delete(minIntersiteDist, [minprojectedDist < d_min], axis=0)
            else:
                totalDistScores= minIntersiteDist
                
        else:
            raise NameError('The MC-Criterion you requested is not available.')
        
            
        self.newSamples = allCandidates
        self.explorationScore = totalDistScores / np.nansum(totalDistScores)
        
        
        return self.newSamples, self.explorationScore 
    
    #--------------------------------------------------------------------------------------------------------
            
    def approximateVoronoi(self, w, constraints=[]):
        """
        An approximate (monte carlo) version of Matlab's voronoi command.  
        The samples are assumed to lie within the LB and UB bounds (=vectors, 
        one lower and upper bound per dimension).  
        
        If LB,UB are not given [-1 1] is assumed.
        
        Arguments
        ---------
        constraints : string
            A set of constraints that have to be satisfied.
            Voronoi cells which partly violate constraints are estimated at their
            size within the allowed area.
        
        Returns
        -------
        areas: numpy array
            An approximation of the voronoi cells' areas.
            
        allCandidates: list of numpy arrays
            A list of samples in each voronoi cell.
        """
        PCEModel = self.PCEModel
        # Get the Old ExpDesign #samples
        samples = self.OldExpDesign
        
        nSamples = samples.shape[0] 
        dim = samples.shape[1]
        
        # Get the bounds
        Bounds = self.Bounds
        
        
        # Compute the number of random points 
        # 100 random points in the domain for each sample
        nPoints = w * samples.shape[0]
        
        # Generate random points to estimate the voronoi decomposition
        # points = np.zeros((nPoints, dim))
        # for i in range(dim):
        #    points[:,i] = stats.uniform(loc=0, scale=1).rvs(size=nPoints)
        
        # # Scale each column to the correct range
        # for i in range(dim):
        #     	points[:,i] = self.scaleColumns(points[:,i],Bounds[i][0],Bounds[i][1])
        
        ExpDesign = ExpDesigns(PCEModel.Inputs)
        points = ExpDesign.generate_samples(nPoints, 'random')

        
        self.allCandidates = points
        
        # Calculate the nearest sample to each point
        self.areas = np.zeros((nSamples))
        self.closestPoints = [np.empty((0,dim)) for i in range(nSamples)] #cell(nSamples, 1)
        
        # Compute the minimum distance from all the samples of OldExpDesign for each test point
        for idx in range(nPoints):
            # calculate the minimum distance
            distances = self.buildDistanceMatrixPoint(samples, points[idx,:], doSqrt=True)
            closestSample = np.argmin(distances)
            
            #Add to the voronoi list of the closest sample
            #print('Point %s found to be closest to sample %s' %(points[idx], samples[closestSample]))
            self.areas[closestSample] = self.areas[closestSample] + 1
            prevclosestPoints = self.closestPoints[closestSample]
            self.closestPoints[closestSample] = np.vstack((prevclosestPoints, points[idx]))
            
        
        # divide by the amount of points to get the estimated volume of each
        # voronoi cell
        self.areas = self.areas / nPoints

        self.perc = np.max(self.areas * 100)

        self.errors = self.areas 

        
        return self.areas, self.allCandidates
    
    #--------------------------------------------------------------------------------------------------------
        
    def buildDistanceMatrixPoint(self, samples, point, doSqrt=False):
        """
        Calculates the intersite distance of all points in samples from point.
        
        """
        
        distances = distance.cdist(samples, np.array([point]), 'euclidean')
                
        # do square root?
        if doSqrt: return distances 
        else: 
            return distances**2
    
    #--------------------------------------------------------------------------------------------------------
    
    def scaleColumns(self, x,lowerLimit,upperLimit):
        """
        Scale all columns of X to [c,d], defaults to [-1,1]
        If mn and mx are given they are used as the original range of each column of x
        
        """

        n = x.shape[0]
        
        mn, mx = min(x), max(x)
        
        # repmat( mn,n,1 ) , repmat(mx-mn,n,1) 
        res = np.divide((x - np.tile(np.array(mn), n)) , np.tile(np.array(mx-mn), n)) * (upperLimit - lowerLimit) + lowerLimit
                
        
        return res

#if __name__ == "__main__":
#    import scipy.stats as stats
#    import matplotlib.pyplot as plt
#    import matplotlib as mpl
#    import matplotlib.cm as cm
#    plt.rc('font', family='sans-serif', serif='Arial')
#    plt.rc('figure', figsize = (12, 8))
#    
#    def plotter(OldExpDesign, allCandidates, explorationScore):
#        global Bounds
#        
#        from scipy.spatial import Voronoi, voronoi_plot_2d
#        vor = Voronoi(OldExpDesign)
#        
#        fig = voronoi_plot_2d(vor)
#        
#        # find min/max values for normalization
##        minima = min(explorationScore)
##        maxima = max(explorationScore)
##        
##        # normalize chosen colormap
##        norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
##        mapper = cm.ScalarMappable(norm=norm, cmap=cm.Blues_r)
##        
##        for r in range(len(vor.point_region)):
##            region = vor.regions[vor.point_region[r]]
##            if not -1 in region:
##                polygon = [vor.vertices[i] for i in region]
##                plt.fill(*zip(*polygon), color=mapper.to_rgba(explorationScore[r]))
#        
#        
#        ax1 = fig.add_subplot(111)
#        
#        ax1.scatter(OldExpDesign[:,0], OldExpDesign[:,1], s=10, c='r', marker="s", label='Old Design Points')
#        for i in range(OldExpDesign.shape[0]):
#            txt = 'p'+str(i+1)
#            ax1.annotate(txt, (OldExpDesign[i,0],OldExpDesign[i,1]))
#            
##        for i in range(NrofCandGroups):
##            Candidates = allCandidates['group_'+str(i+1)]
##            ax1.scatter(Candidates[:,0],Candidates[:,1], s=10, c='b', marker="o", label='Design candidates')
#        ax1.scatter(allCandidates[:,0],allCandidates[:,1], s=10, c='b', marker="o", label='Design candidates')
#        
#        ax1.set_xlim(Bounds[0][0], Bounds[0][1])
#        ax1.set_ylim(Bounds[1][0], Bounds[1][1])
#        
#        plt.legend(loc='best');
#        plt.show()
#        
#    def voronoi_volumes(points):
#        from scipy.spatial import Voronoi, ConvexHull
#        v = Voronoi(points)
#        vol = np.zeros(v.npoints)
#        
#        for i, reg_num in enumerate(v.point_region):
#            indices = v.regions[reg_num]
#            if -1 in indices: # some regions can be opened
#                vol[i] = np.inf
#            else:
#                
#                #print("reg_num={0: 3.3f} X1={1: 3.3f} X2={2: 3.3f}".format(reg_num, v.points[reg_num-1, 0], v.points[reg_num-1, 1]))
#                vol[i] = ConvexHull(v.vertices[indices]).volume
#        
#        print('-'*40)
#        for i in range(nrofSamples):
#            print("idx={0:d} X1={1: 3.3f} X2={2: 3.3f} Volume={3: 3.3f}".format(i+1, v.points[i, 0], v.points[i, 1], vol[i]))
#        
#        return vol    
#    
#    NofPa = 2
#    
#    Bounds = ((-5,10), (0,15))
#    
#    nrofSamples = 10
#    OldExpDesign = np.zeros((nrofSamples, NofPa))
#    for idx in range(NofPa):
#        Loc = Bounds[idx][0]
#        Scale = Bounds[idx][1] - Bounds[idx][0]
#        OldExpDesign[:,idx] = stats.uniform(loc=Loc, scale=Scale).rvs(size=nrofSamples)
#    
#    
#    nNewCandidate = 40
#    
#    # New Function
#    volumes = voronoi_volumes(OldExpDesign)
#    
#    
#    # SUMO
#    Exploration = Exploration(Bounds, OldExpDesign, nNewCandidate)
#    
#    #allCandidates, Score = Exploration.getVornoiSamples()
#    allCandidates, Score = Exploration.getMCSamples()
#    
#    print('-'*40)
##    for i in range(nrofSamples):
##        print("idx={0:d} X1={1: 3.3f} X2={2: 3.3f} Volume={3: 3.3f}".format(i+1, OldExpDesign[i,0], OldExpDesign[i,1], vornoi.areas[i]))
#        
#    plotter(OldExpDesign, allCandidates, volumes)
    
