import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Solution:
    routes = []
    def __init__(self, instance):
        self.instance = instance
        self.routes = []

    def valid_solution(self):
        
        # Checking if any vehicle is visiting an already visited point
        duplicates = [point for route in self.routes 
                      for point, count in collections.Counter(route[1:-1]).items() 
                      if count > 1]

        if len(duplicates) > 0:
            print("A customer has been visited more than once. Try again!")
            return False
        
        # The depot can't be in any route
        if 0 in duplicates:
            print("Some fool visited the depot on his route before finishing. Try again!")
            return False
        
        # Checking capacity constraints
        capacities = [self.capacity_constraints(route) 
                      for route in self.routes]

        if [False for capacity in capacities if capacity > self.instance.capacity]:
            print("A vehicle has exceeded the capacity limit!")
            return False
        
        # Checking intersection issues
        intersections = [self.intersection(route1[1:-1], route2[1:-1]) 
                         for route1 in self.routes 
                         for route2 in self.routes[1:] 
                         if route1 != route2]
        if [False for item in intersections if len(item) > 0]:
            print("Intersections between two routes have been found!")
            return False
        
        # Constraint 1 - Amount of Leaving and Entering vehicles are equal
        if [False for route in self.routes if route[0] != 0 or route[-1] != 0]:
            print("The amount of entering and leaving vehicles are NOT equal!")
            return False

        return True
    
    def capacity_constraints(self, route):
        return sum([self.instance.nodes[point]['rq'] for point in route])
    
    def intersection(self, route1, route2):
        return [P for P in route1 if P in route2]

    def cost(self):
        return sum([self.instance.route_length(r) for r in self.routes])
    
    
    # def euclidean_distance(self, q, p):
    #     '''We are only working with one-dimension, so the equation is as follow: SQRT((Qx - Px)^2 + (Qy - Py)^2)'''
    #     return math.sqrt(pow(q.x - p.x, 2) + pow(q.y - p.y, 2))


    def write_to_file(self, filename):
        with open(filename, "w") as filehandle:
            for route in self.routes:
                filehandle.write(",".join(map(lambda x: self.instance.nodes[x]["id"],route))+"\n")

    def plot_lines(self, points, style='bo-'):
        "Plot lines to connect a series of points."
        plt.plot([self.instance.nodes[p]["pt"].x for p in points], [self.instance.nodes[p]["pt"].y for p in points], style)
        plt.axis('scaled'); plt.axis('off')

    def plot_routes(self, outputfile_name=None):
        "routes is a list of routes (alternatively it can be a grand route).  The depot is red square."
        color = ["b","g","r","c","m","k"]
        c=0
        for route in self.routes:
            start = route[0]
            self.plot_lines(list(route), style=color[c]+"o-")
            self.plot_lines([start], 'rs') # Mark the start city with a red square
            c=(c+1) % len(color)
        if outputfile_name is None:
            plt.show()
        else:
            plt.savefig(outputfile_name, dpi=300)
