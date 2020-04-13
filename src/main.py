#!/usr/bin/python3

from algorithmconstructor import AlgorithmConstructor
import sys
import argparse
import time
import data
from furthestcluster import FurhestCluster
import solverLS
from solverNN import NearestNeightbour
from solverKNN import KNearestNeightbour
from twoopt import TwoOPT
from threeopt import ThreeOPT
from timeout import TimeOutException
import os
from pathlib import Path
# @my_logger
# @my_timer


def solve(instance, config):
    t0 = time.time()
    ch = FurhestCluster(instance)
    # ch = NearestNeightbour(instance)
    sol = ch.construct(t0)  # returns an object of type Solution

    # t0 = time.time()
    # ls = TwoOPT(sol)
    # ls = ThreeOPT(sol)
    # sol = ls.construct(t0)  # returns an object of type Solution
    return sol

def performance_testing(config):
    heuristics_algorithms = [NearestNeightbour]
    
    try:
        abs_path = os.path.abspath(os.path.dirname(__file__))
        results_path = os.path.join(abs_path, "../results/")
        data_path = os.path.join(abs_path, "../data/")
        
        for index, algorithm in enumerate(heuristics_algorithms):
            if os.path.isfile(results_path + algorithm.__name__ + '.csv'):
                os.remove(results_path + algorithm.__name__ + '.csv')
            Path(results_path).mkdir(parents=True, exist_ok=True)
            with open(results_path + algorithm.__name__ + '.csv', 'a') as filehandler:
                filehandler.write("{}, {}, {}, {}\n".format("Instance", "Cost", "Time", "Total Nodes"))
            
                for path, subdirs, files in os.walk(data_path):
                    for filename in files:
                        if '.xml' in filename:
                            print(filename)
                            t0 = time.time() # start time
                            instance = data.Data(os.path.join(path, filename))
                            canonical_solution = AlgorithmConstructor(instance, algorithm)
                            sol = canonical_solution.construct(t0)
                            assert sol.valid_solution()
                            ls = TwoOPT(sol)
                            # ls = ThreeOPT(sol)
                            sol = ls.construct(t0)  # returns an object of type Solution
                            assert sol.valid_solution()
                            time_elapsed = time.time() - t0
                            filehandler.write("{}, {}, {}, {}\n"
                                              .format(filename, sol.cost(), 
                                                      round(time_elapsed, 2), len(instance.nodes)))
                            
                        
    except TimeOutException:
        tb = sys.exc_info()[2]
        print(tb)


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', action='store',
                        dest='output_file',
                        help='The file where to save the solution and, in case, plots')

    parser.add_argument('-t', action='store',
                        dest='time_limit',
                        type=int,
                        required=True,
                        help='The time limit')

    parser.add_argument('instance_file', action='store',
                        help='The path to the file of the instance to solve')
    
    
    parser.add_argument('-p', 
                        action="store_true",
                        dest='performancetest',
                        default=False,
                        help='The file where to save the solution and, in case, plots')

    config = parser.parse_args()
    print('instance_file    = {!r}'.format(config.instance_file))
    print('output_file      = {!r}'.format(config.output_file))
    print('time_limit       = {!r}'.format(config.time_limit))
    if config.performancetest:
        
        performance_testing(config)
    else:    
        instance = data.Data(config.instance_file)
        instance.short_info()
        if config.output_file is not None:
            instance.plot_points(config.output_file+'.png');
        instance.show()
    
        sol = solve(instance, config)
    
        assert sol.valid_solution()
        if config.output_file is not None:
            if os.path.isfile(config.output_file):
                os.remove(config.output_file+'*')
            sol.plot_routes(config.output_file+'_sol'+'.png')
            sol.write_to_file(config.output_file+'.sol')
        print("{} routes with total cost {:.1f}"
              .format(len(sol.routes), sol.cost()))


if __name__ == "__main__":
    main(sys.argv[1:])
