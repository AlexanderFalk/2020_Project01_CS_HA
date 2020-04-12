#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:11:01 2020

@author: alexanderfalk
"""

import itertools
import time
import solution
import sys
import random

class KNearestNeightbour:


    def __init__(self, instance, time_limit=60):
        self.instance = instance
        self.time_limt = time_limit

    def construct(self, start_time):
        return self.algorithm(start_time)

    def algorithm(self, start_time, k=3):
        sol = solution.Solution(self.instance)
        
        route = [0] # Our route
        capacity = 0 # Our capacity for each vehicle
        unvisited_nodes = list(self.instance.nodes[1:])
        current_node = self.instance.nodes[0] # Starting a depot 0
        distances = {}
        
        # While there are still nodes to visit, continue
        while unvisited_nodes:
            # Loop through the unvisited nodes
            for index, p in enumerate(unvisited_nodes):
                dist = sol.instance.distance(current_node['pt'], p['pt'])
                distances.update( { dist : p } )
                
            distances = {k : v for k, v in sorted(distances.items(), key=lambda item: item[0])}
            shortest_distances = dict(itertools.islice(distances.items(), k))
            
            randomly_picked_node = random.choice(list(shortest_distances.keys()))
            node = distances.get(randomly_picked_node)
            if capacity + node['rq'] <= self.instance.capacity:
                capacity += node['rq']
                route += [int(node['id']) - 1]
                current_node = node
                unvisited_nodes.remove(current_node)

            else:
                sol.routes += [route+[0]]
                route = [0]
                capacity = node['rq']
            
            t1 = time.time() # End time
            if t1 - start_time > self.time_limit:
                sys.stdout.write("Time Expired\n")
                return sol

            distances = {}
            node = None
            randomly_picked_node = None            
            
        sol.routes += [route+[0]]
        return sol

