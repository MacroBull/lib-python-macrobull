# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:10:14 2013

@author: macrobull

data import module for Tek oscilloscope

________________________________________
Details:

	device:	rigol
	source format:	csv
	addtional info:	2 lines
	count of channels:	1 or 2
	count of samples:	2048
	resolution:	8bit


"""

import csv
import sys
import numpy as np
#from pylab import *

from .__init__ import *


#SAMPLESIZE=2048
#rSAMPLESIZE=repr(SAMPLESIZE)


def loadWaveFromFile(filename,withUnit=True, chSepFile = False):
	if not(filename.endswith('.csv')): sys.stderr.write('[Warning]May not be a supported file format!\n')
	f=csv.reader(open(filename,'r'))
	r=oscWave(filename)

	if chSepFile:

		titles=next(f)
		units=next(f)

		r.tTitle=titles[0]
		r.chTitles=titles[1:-1]

		if withUnit:
			r.tUnit=units[0]
			r.chUnits=units[1:-1]
		else:
			r.tUnit=None

		r.chCnt=len(r.chTitles)
		r.chs=[None,None]

		if r.chCnt==1:
			r.t,r.chs[0]=[],[]
			for line in f:
				if len(line)>0:
					r.t.append(float(line[0]))
					r.chs[0].append(float(line[1]))



		if r.chCnt==2:
			r.t,r.chs[0],r.chs[1]=[],[],[]
			for line in f:
				if len(line)>0:
					r.t.append(float(line[0]))
					r.chs[0].append(float(line[1]))
					r.chs[1].append(float(line[2]))
			r.chs[1]=np.array(r.chs[1])

		r.t=np.array(r.t)
		r.chs[0]=np.array(r.chs[0])
	else:

		titles=next(f)
		units=next(f)

		r.chTitles=titles[:-2]
#		r.tUnit = 's'
#		r.chUnits = units[:-2]
#		r.chCnt = len(units)-2

#		t = float(units[-2])
#		t_inc = float(units[-1])
#
#		r.t = []
#		r.chs = [[] for i in range(r.chCnt)]
#		for line in f:
#			r.t.append(t)
#			for i in range(r.chCnt):
#				r.chs[i].append(float(line[i]))
#			t += t_inc
#
#		r.t = np.array(r.t)
#		for i in range(r.chCnt): r.chs[i] = np.array(r.chs[i])

		r.tUnit = units[0]
		r.chUnits = units[1:]
		r.chCnt = len(units)-2

		r.chTitles=titles[1:-1]

		r.t = []
		r.chs = [[] for i in range(r.chCnt)]
		for line in f:
			r.t.append(float(line[0]))
			for i in range(r.chCnt):
				r.chs[i].append(float(line[1+i]))

		r.t = np.array(r.t)
		for i in range(r.chCnt): r.chs[i] = np.array(r.chs[i])

	return r
