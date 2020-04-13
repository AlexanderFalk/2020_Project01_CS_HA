#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 07:51:01 2020

@author: alexanderfalk
"""
import time
import solution
import sys

class FurhestCluster:


    def __init__(self, instance, time_limit=60):
        self.instance = instance
        self.time_limit = time_limit

    def construct(self, time_left):
        return self.algorithm(time_left)

    def algorithm(self, start_time):
        sol = solution.Solution(self.instance)
        route = [0] # Our route
        capacity = 0 # Our capacity for each vehicle
        unvisited_nodes = list(self.instance.nodes)
        current_node = self.instance.nodes[0] # Starting a depot 0
        unvisited_nodes.remove(current_node)
        furthest_distance = 0
        furthest_node = None
        closest_distance_from_furthest_node = 0
        closest_node_from_furthest_node = None
        
        furthest_node_closest_nodes = []
        
        # While there are still nodes to visit, continue
        while unvisited_nodes:
            # Find the node furthest away from the depot
            for index, p in enumerate(unvisited_nodes):
                dist = sol.instance.distance(current_node['pt'], p['pt'])

                if dist > furthest_distance or furthest_distance == 0:
                    furthest_distance = dist
                    furthest_node = p
                    
            unvisited_nodes.remove(furthest_node)
            furthest_node_closest_nodes += [furthest_node]
            capacity += furthest_node['rq']
            # As long as the capacity is not reached
            capacity_not_reached = True
            while capacity_not_reached and unvisited_nodes:

                # Loop through the nodes closest to the furthest node
                for index, p in enumerate(unvisited_nodes):
                    dist = sol.instance.distance(furthest_node['rq'], p['rq'])
                    if dist < closest_distance_from_furthest_node or closest_distance_from_furthest_node == 0:
                        closest_distance_from_furthest_node = dist
                        closest_node_from_furthest_node = p
                        
                    # If the closest node can fit the vehicle, then add it to its own list        
                    if capacity + closest_node_from_furthest_node['rq'] <= self.instance.capacity:
                        capacity += closest_node_from_furthest_node['rq']
                        furthest_node_closest_nodes += [closest_node_from_furthest_node]
                        unvisited_nodes.remove(closest_node_from_furthest_node)
                        closest_distance_from_furthest_node = 0
                    else:
                        capacity_not_reached = False
            
            # Find the shortest route in the furthest node list of closest nodes
            sub_current_node = furthest_node
            closest_distance = 0
            closest_node = None
            while furthest_node_closest_nodes:
                
                for node in furthest_node_closest_nodes:
                    dist = sol.instance.distance(sub_current_node['rq'], node['rq'])
                    
                    if dist < closest_distance or closest_distance == 0:
                        closest_distance = dist
                        closest_node = node
                        
                route += [self.instance.nodes.index(closest_node)]
                sub_current_node = closest_node
                furthest_node_closest_nodes.remove(closest_node)
                closest_distance = 0
    
            t1 = time.time() # End time
            if t1 - start_time > self.time_limit:
                sys.stdout.write("Time Expired\n")
                return sol

                            
            sol.routes += [route+[0]]
            route = [0]
            capacity = 0
            furthest_distance = 0
            furthest_node = None
            closest_distance_from_furthest_node = 0
            closest_node_from_furthest_node = None
            furthest_node_closest_nodes = []

        return sol