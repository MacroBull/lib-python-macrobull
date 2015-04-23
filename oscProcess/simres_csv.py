# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:10:14 2013

@author: macrobull

data import module for simulation data by proteus etc.

________________________________________
Details:

"TIME","R2(1)","U1:B(OP)","U1:D(OP)"
3,0,-10.6877,-7.8911
3.00541978,0,-10.6877,-7.89109


"""

#import csv
import sys
import numpy as np
#from pylab import *

from __init__ import *


#SAMPLESIZE=2048
#rSAMPLESIZE=repr(SAMPLESIZE)


def loadWaveFromFile(filename,withUnit=True):
	if not(filename.endswith('.csv')): sys.stderr.write('[Warning]May not be a supported file format!\n')
	f=open(filename,'r')
	r=oscWave(filename)

	titles=f.readline().rstrip().split(',')
	buff = f.readline().rstrip()
	units = None
	while not(buff[0] in '1234567890'):
		units=next(buff)
		buff = f.readline().rstrip()

	r.tTitle=titles[0]
	r.chTitles=titles[1:]
	r.chCnt = len(r.chTitles)

	if units:
		r.tUnit=units[0]
		r.chUnits=units[1:]
	else:
		r.tUnit='s'
		r.chUnits=['V']*r.chCnt

	r.t = []
	r.chs=[[] for i in range(r.chCnt)]

	while buff.find(',')>0:
		r.t.append(float(buff[:buff.find(',')]))
		for i, s in enumerate(buff[buff.find(',')+1: ].split(',')):
			r.chs[i].append(float(s))
		buff = f.readline()

	r.t=np.array(r.t)
	r.chs=[np.array(i) for i in r.chs]
	#if r.chCnt == 1: r.chs.append(None)

	return r
