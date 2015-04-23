# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:10:14 2013

@author: macrobull
data import module for Tek oscilloscope

________________________________________
Details:

	device:Tektronix TDS-2000
	source format:CSV
	addtional info:	18 lines, stored in r.info
	count of channels:	1(per file)
	count of samples:	2482
	resolution:	8bit
	
"""

import csv
import sys
import numpy as np
#from pylab import *

from __init__ import *


#SAMPLESIZE=2500-18
#rSAMPLESIZE=repr(SAMPLESIZE)


def loadWaveFromFile(filename):
	if not(filename.endswith('.CSV')): sys.stderr.write('[Warning]May not be a supported file format!\n')
	f=csv.reader(open(filename,'r'))
	r=oscWave(filename)

	info=[]
	for i in range(18):
		info.append(next(f))
	#print(info[1][1])

	r.tTitle='Time'
	r.tUnit=info[10][1]
	r.chTitles=[info[6][1]]
	r.chUnits=[info[7][1]]

	info=info[:3]+info[6:]
	r.info={}
	for item in info: r.info[item[0]]=item[1:]

	r.chCnt=1
	#l=len(r.chTitles)
	r.chs=[None]
	r.t,r.chs[0]=[],[]
	for line in f:
		if len(line)>0:
			r.t.append(float(line[3]))
			r.chs[0].append(float(line[4]))

	r.t=np.array(r.t)
	r.chs[0]=np.array(r.chs[0])
	return r
