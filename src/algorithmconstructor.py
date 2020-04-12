#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:57:55 2020

@author: alexanderfalk
"""

import math
import solution
from signal import signal, alarm, SIGALRM
from timeout import TimeOutException


class AlgorithmConstructor:
    
    
    def __init__(self, instance=None, algorithm=None, time_limit=60):
        assert instance is not None
        assert algorithm is not None
        self.instance = instance
        self.algorithm = algorithm
        self.time_limit = time_limit
        self.solution = solution.Solution(self.instance)
        
        
    def timeout_handler(self, signum, frame):
        raise TimeOutException(self.solution)
        
        
    def construct(self, start_time):
        signal(SIGALRM, self.timeout_handler)
        alarm(math.ceil(self.time_limit))
        return self.canonical_solution(start_time)
    
    def canonical_solution(self, start_time):
        ch = self.algorithm(self.instance, self.time_limit)
        self.solution = ch.construct(start_time)
        return self.solution
    
    