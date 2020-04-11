import time
import solution
import sys

class NearestNeightbour:


    def __init__(self, instance):
        self.instance = instance

    def construct(self, time_left):
        return self.algorithm(time_left)

    def algorithm(self, time_left):
        sol = solution.Solution(self.instance)
        t0 = time.process_time() # Starting time
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

            if time.process_time() - t0 > time_left:
                sys.stdout.write("Time Expired")
                return sol

            shortest_distance = 0
            closest_node = None
            
        sol.routes += [route+[0]]
        return sol

