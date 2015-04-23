# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:10:14 2013

@author: macrobull

data import module for Tek oscilloscope

________________________________________
Details:

	device:	neoScope
	source format:	BIN
	addtional info:	None
	count of channels:	2
	count of samples:	2040
	resolution:	8bit

"""

import struct
import sys

from __init__ import *


SAMPLESIZE=2040
rSAMPLESIZE=repr(SAMPLESIZE)


def loadWaveFromFile(filename	,Sa=1e5,ch1Div=1,ch2Div=1	,tOff=0,ch1Off=0,ch2Off=0):
	'''
	record Sa,Channel Div,Channel from bitmap screenshot files!!!
	offset can be set if there is problem

	example:
		s=neo.loadWaveFromFile('RAW001.BIN',Sa=651.0e3,ch1Div=5,ch2Div=5)
	'''
	if not(filename.endswith('.BIN')): sys.stderr.write('[Warning]May not be a supported file format!\n')

	f=open(filename,'rb')
	s=oscWave(filename)
	s.SAMPLESIZE=2040
	s.rSAMPLESIZE=repr(SAMPLESIZE)
	s.chs=[array(struct.unpack(rSAMPLESIZE+'B'	,f.read(SAMPLESIZE)))	,array(struct.unpack(rSAMPLESIZE+'B'	,f.read(SAMPLESIZE)))]

	s.chCnt=2
	#r.l=SAMPLESIZE
	#s.t=linspace(tPos-5*tDiv,tPos+5*tDiv,SAMPLESIZE) #should be calc by Sa!
	s.t=linspace(tOff-1020/Sa,tOff+1020/Sa,SAMPLESIZE) #should be calc by Sa!
	s.chs[0]=(s.chs[0]-128)*ch1Div*0.040+ch1Off
	s.chs[1]=(s.chs[1]-128)*ch2Div*0.040+ch2Off
	s.tUnit='Second'
	s.chTitles=['ch1','ch2']
	s.chUnits=['Volt']*2

	return s
