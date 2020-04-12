#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 10:56:48 2020

@author: alexanderfalk
"""

import itertools
import time
import sys

class ThreeOPT:


    def __init__(self, computed_solution, time_limit=60):
        self.solution = computed_solution
        self.time_limit = time_limit

    def construct(self, time_left):
        return self.algorithm(time_left)

    def algorithm(self, start_time):
        for index, route in enumerate(self.solution.routes):
            segments = self.tour_segments(route)
            for i, j, k in segments:
                self.solution.routes[index] = self.improvement(route, i, j, k)
                
                t1 = time.time() # End time
                if t1 - start_time > self.time_limit:
                    sys.stdout.write("Time Expired\n")
                    return self.solution
        
        return self.solution

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)
    
    def tour_segments(self, route):
        indices = [index for index in range(len(route))]
        return list(itertools.combinations(indices, r = 3))

    def improvement(self, route, i, j, k):
        A, B, C, D, E, F = route[i-1], route[i], route[j-1], route[j], route[k-1], route[k % len(route)]
        dist0 = self.distance(A, B) + self.distance(C, D) + self.distance(E, F)
        dist1 = self.distance(A, C) + self.distance(B, D) + self.distance(E, F)
        dist2 = self.distance(A, B) + self.distance(C, E) + self.distance(D, F)
        dist3 = self.distance(A, D) + self.distance(E, B) + self.distance(C, F)
        dist4 = self.distance(F, B) + self.distance(C, D) + self.distance(E, A)
        
        if dist0 > dist1:
            route[i:j] = reversed(route[i:j])
            
        elif dist0 > dist2:
            route[j:k] = reversed(route[j:k])
            
        elif dist0 > dist4:
            route[i:k] = reversed(route[i:k])
            
        elif dist0 > dist3:
            route[i:k] = route[j:k] + route[i:j]
            
        return route