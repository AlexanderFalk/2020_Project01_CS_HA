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
        self.stuck = False
        self.threshold = 20
        self.threshold_counter = 0

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
        test = []
        total = 0
        for route in local_best.routes:
            total = 0
            for point in route:
                total += self.instance.nodes[point]['rq']
                
            test.append(total)
        print(test)
        # Stopping criteria: time
        while time.time() - start_time < self.time_limit:
            # Improving a Candidate Solution
            candidate = deepcopy(local_best)
            self.tabu_list_edges = []
            # Enumerate the candidate solution for swapping
            for i in range(len(candidate.routes)-1):
                for j in range(1, len(candidate.routes)):
                    if i != j:
                        candidate.routes[i], candidate.routes[j] = self.improvement(candidate.routes[i], candidate.routes[j])
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

    def improvement(self, route1, route2):
        
        for i in range(1, len(route1) - 1):
            A, B, C = route1[i-1], route1[i], route1[i+1] 
            for j in range(1, len(route2) - 1):
                D, E, F = route2[j-1], route2[j], route2[j+1]
                if self.distance(A, B) + self.distance(B, C) > self.distance(A, E) + self.distance(E, C) and self.distance(D, E) + self.distance(E, F) > self.distance(D, B) + self.distance(B, F):
                    if (E, C) not in self.tabu_list_edges and (B, F) not in self.tabu_list_edges:
                        self.tabu_list_edges.append((E, C))
                        self.tabu_list_edges.append((B, F))
                        print(f"{route1}, {route2}")           
                        print(f"bi: {route1[i]}, bk: {route2[j]}")
                        if sum([self.instance.nodes[point]['rq'] for point in route1]) < self.instance.capacity and sum([self.instance.nodes[point]['rq'] for point in route2]) < self.instance.capacity:
                            route1[i] = E
                            route2[j] = B
                            self.threshold_counter = 0
                            print("SWAP")
                    else:
                        self.threshold_counter += self.threshold_counter
                        if self.threshold_counter == self.threshold:
                            if sum([self.instance.nodes[point]['rq'] for point in route1]) < self.instance.capacity and sum([self.instance.nodes[point]['rq'] for point in route2]) < self.instance.capacity:
                                print("SWAP")
                                route1[i] = E
                                route2[j] = B
                                self.threshold_counter = 0
                        

                    
        return route1, route2