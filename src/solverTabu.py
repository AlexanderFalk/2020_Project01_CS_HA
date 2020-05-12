#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 08 08:15:31 2020

@author: alexanderfalk
"""

from copy import deepcopy
from itertools import permutations
from solverNN import NearestNeightbour
import time
import solution
import sys

class TabuSearch:

    def __init__(self, instance, time_limit=60):
        self.instance = instance
        self.time_limit = time_limit
        self.tabu_list_solutions = []
        self.tabu_list_solutions_max_size = 10
        self.tabu_list_edges = []
        self.tabu_list_edges_max_size = 5
        self.best_candidate_list = []

    def construct(self, start_time):
        return self.algorithm(start_time)

    def algorithm(self, start_time):
        """
        Tabu Search is an algorithm, which takes memory into consideration and tries to accomodate the problem of being stuck in local optimum.
        It is termed as a metaheuristic algorithm, meaning, it has a stopping criteria (such as time or epochs).
        The algoritm works as following:
            1. Create a solution by using a constructive algorithm (such as Nearest Neightbour) to establish a starting point
            2. Store the solution as the best solution
            3. Start making changes in the solution by swapping, deleting, adding or other modifications. 
            4. When a modification has been executed, the edge connecting two nodes are added to a Tabu List. The list contains edges which cannot be touched for n epochs. The length of the Tabu List is arbitrarily.
            5. Execute step 2-4 repeately until the stopping criteria is met. 
        """

        local_best = None

        ch = NearestNeightbour(self.instance)
        local_best = ch.construct(start_time)  # returns an object of type Solution

        # Stopping criteria: time
        while time.time() - start_time < self.time_limit:
            # Improving a Candidate Solution
            candidate = deepcopy(local_best)
            self.tabu_list_edges = []
            # Enumerate the candidate solution for swapping
            for index, route in enumerate(candidate.routes):
                segments = self.tour_segments(route)
                for i, j in segments:
                    candidate.routes[index] = self.improvement(route, i, j)
                    if len(self.tabu_list_edges) > self.tabu_list_edges_max_size:
                        self.tabu_list_edges.pop(0) # Remove entry which have been a tabu for n iterations
            
            if candidate.cost() < local_best.cost() and candidate not in self.tabu_list_solutions:
                local_best = candidate
                print(local_best.cost())
            
            self.tabu_list_solutions.append(candidate)
            if len(self.tabu_list_solutions) > self.tabu_list_solutions_max_size:
                self.tabu_list_solutions.pop(0)

        sys.stdout.write(f"Time Expired for {__name__}. Local Optima Returned\n")
        return local_best

    def distance(self, i, j):
        return self.instance.pre_distance(i, j)
    
    def tour_segments(self, route):
        indices = [index for index in range(len(route))]
        return list(permutations(indices, r = 2))

    def improvement(self, route, i, j):
        A, B, C, D = route[i-1], route[i], route[j-1], route[j % len(route)]
        if self.distance(A, B) + self.distance(C, D) > self.distance(A, C) + self.distance(B, D):
            if sum([self.instance.nodes[point]['rq'] for point in reversed(route[i:j])]) < self.instance.capacity:
                if (B, C) not in self.tabu_list_edges:
                    route[i:j] = reversed(route[i:j])
                    self.tabu_list_edges.append((B, C))

        return route