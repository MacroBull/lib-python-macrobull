# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:48:26 2013
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

"""

import re
import time

def colorizePrint(s,color):
	#color=0,1,4,5,7,30~37,40~47
	return "\x1B[1;{}m{}\x1B[0m".format(color,s)

class debugPrint():
	#use with!!!
	def __init__(self,filename):
		if filename==None: filename=repr(time.ctime())
		self.fDeb=open(filename,'w')
		
	def dprint(s):
		color=0
		ss=repr(s)
		if ss.find('info')>0: color=32
		elif ss.find('sensor')>0: color=36
		elif ss.find('err')>0: color=31
		if color:
			print(colorizePrint(s,color))
		else:
			print(s)
		fDeb.write('[{}] {}\n'.format(time.asctime(),s))
		fDeb.flush()