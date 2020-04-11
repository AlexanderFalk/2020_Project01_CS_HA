#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:26:39 2020

@author: alexanderfalk
"""


import time
import itertools
import copy

class TwoOPT:


    def __init__(self, computed_solution):
        self.solution = computed_solution

    def construct(self, time_left):
        return self.algorithm(time_left)

    def algorithm(self, time_left):
        
        for index, route in enumerate(self.solution.routes):
            for A, B, C in self.tour_segments(route[1:-1]):
                self.solution.routes[index] = self.improvement(route, A, B, C)
        
        return self.solution

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)
    
    def tour_segments(self, route):
        return list(itertools.permutations(route, r = 3))

    def improvement(self, route, *points):
        A, B, C = list(points)
        temp_route = copy.deepcopy(route)
        if self.distance(A, B) + self.distance(B, C) > self.distance(A, C) + self.distance(C, B):
            old_total_dist = sum(self.distance(route[i], route[i - 1]) for i in range(len(route)))
            index_B = temp_route.index(B)
            index_C = temp_route.index(C)
            temp_route[index_B], temp_route[index_C] = temp_route[index_C], temp_route[index_B]
            new_total_dist = sum(self.distance(temp_route[i], temp_route[i - 1]) for i in range(len(temp_route)))
            if new_total_dist < old_total_dist:
                route = copy.deepcopy(temp_route)

        return route
        