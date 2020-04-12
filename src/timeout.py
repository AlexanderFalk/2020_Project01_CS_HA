#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 15:11:51 2020

@author: alexanderfalk
"""


class TimeOutException(Exception):
    
    
    def __init(self, solution):
        super(TimeOutException, self).__init__(
            "A timeout has occurred during execution of the heuristics algorithms!"
            )
        
        self.solution = solution

