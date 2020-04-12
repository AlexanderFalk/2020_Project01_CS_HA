#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 07:31:15 2020

@author: alexanderfalk
"""


import time
import solution
import sys

class NearestNeightbour:


    def __init__(self, instance, time_limit=60):
        self.instance = instance
        self.time_limit = time_limit

    def construct(self, start_time):
        return self.algorithm(start_time)

    def algorithm(self, start_time):
        sol = solution.Solution(self.instance)
        route = [0] # Our route
        capacity = 0 # Our capacity for each vehicle
        unvisited_nodes = list(self.instance.nodes[1:])
        current_node = self.instance.nodes[0] # Starting a depot 0
        shortest_distance = 0
        closest_node = None
        
        # While there are still nodes to visit, continue
        while unvisited_nodes:
            # Loop through the unvisited nodes
            for index, p in enumerate(unvisited_nodes):
                dist = sol.instance.distance(current_node['pt'], p['pt'])

                if dist < shortest_distance or shortest_distance == 0:
                    shortest_distance = dist
                    closest_node = p

            if capacity + closest_node['rq'] <= self.instance.capacity:
                capacity += closest_node['rq']
                route += [int(closest_node['id']) - 1]
                current_node = closest_node
                unvisited_nodes.remove(current_node)

            else:
                sol.routes += [route+[0]]
                route = [0]
                capacity = closest_node['rq']
            
            t1 = time.time()
            if t1 - start_time > self.time_limit:
                sys.stdout.write("Time Expired\n")
                return sol

            shortest_distance = 0
            closest_node = None
            
        sol.routes += [route+[0]]
        return sol

