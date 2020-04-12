#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:26:39 2020

@author: alexanderfalk
"""


import time
import itertools
import sys

class TwoOPT:


    def __init__(self, computed_solution, time_limit=60):
        self.solution = computed_solution
        self.time_limit = time_limit

    def construct(self, time_left):
        return self.algorithm(time_left)

    def algorithm(self, start_time):
        for index, route in enumerate(self.solution.routes):
            segments = self.tour_segments(route)
            for i, j in segments:
                self.solution.routes[index] = self.improvement(route, i, j)
                
                t1 = time.time() # End time
                if t1 - start_time > self.time_limit:
                    sys.stdout.write("Time Expired\n")
                    return self.solution
        
        return self.solution

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)
    
    def tour_segments(self, route):
        indices = [index for index in range(len(route))]
        return list(itertools.permutations(indices, r = 2))

    def improvement(self, route, i, j):
        A, B, C, D = route[i-1], route[i], route[j-1], route[j % len(route)]
        if self.distance(A, B) + self.distance(C, D) > self.distance(A, C) + self.distance(B, D):
            route[i:j] = reversed(route[i:j])
        return route