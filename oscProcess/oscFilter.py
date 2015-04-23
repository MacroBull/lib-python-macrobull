# -*- coding: utf-8 -*-
"""
Created on %(date)
Project	:Python-Project
Version	:0.0.1
@author	:MacroBull

decide to add some DSP/filters for waveforms

"""


import numpy as np
from scipy import signal

def avgFilter(s):
	r=np.zeros(len(s))
	r[-1]=s[-1]
	r[0]=s[0]
	for i in range(1,len(s)-1):
		r[i]=(s[i-1]+s[i+1]+2*s[i])/4
	return r

def iirFilter(s):

	b, a = signal.iirdesign([1e-6,0.25], [1e-8,0.6], 3, 50)
	r = signal.lfilter(b, a, s)
	return r