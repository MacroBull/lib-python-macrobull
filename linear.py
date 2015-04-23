# -*- coding: utf-8 -*-
"""
Created on %(date)
Project	:Python-Project
Version	:0.0.1
@author	:%(username)
"""


def linear(a,b,u):
	return a*u+b*(1-u)

def extend(a,b,u):
	return (a*(1+u)+b*-u,a*-u+b*(1+u))
