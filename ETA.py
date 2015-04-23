# -*- coding: utf-8 -*-
"""
Created on Sat May 11 00:34:25 2013

@author: macrobull
Record time elapse of progress, calculate ETA in a better way(-quadratic-?)
"""

import time


class estProc():
	'''class for process to be estimated'''
	
	def __init__(self,p=0):
		'''p=initial process'''
		self.step=[(p,time.time())]
		
	
	def setProgress0(self,p):
		'''record time at this progress'''
		nowTime=time.time()
		step=self.step
		
		if p<=0:
			'''invalid progress'''
			step=[(p,nowTime)]
			return -1
		else:
			pSum=0
			sSum=0
			
			'''if p is a rolling-back'''
			i=len(step)-1
			while step[i][0]>=p: i-=1
			step=step[:i+1]
			
			step.append((p,nowTime))
			for i in range(len(step)-1):
				pSum+=1/(p-step[i][0])
				sSum+=(step[i+1][1]-step[i][1])/(step[i+1][0]-step[i][0])/(p-step[i][0])
				
			return sSum*(1-p)/pSum
		
	
	def setProgress1(self,p):
		
		nowTime=time.time()
		step=self.step
		
		if p<=0:
			'''invalid progress'''
			step=[(p,nowTime)]
			return -1
		else:
			pSum=0
			sSum=0
			
			'''if p is a rolling-back'''
			i=len(step)-1
			while step[i][0]>=p: i-=1
			step=step[:i+1]
			
			step.append((p,nowTime))
			for i in range(len(step)-1):
				pSum+=1/(p-step[i][0])
				sSum+=(nowTime-step[i][1])/(p-step[i][0])/(p-step[i][0])
				
			return sSum*(1-p)/pSum
		
		
	setProgress=setProgress1
	'''makes setProgress1 default'''


defaultProc=estProc(0)
setProgress0=defaultProc.setProgress0
setProgress1=defaultProc.setProgress1
setProgress=defaultProc.setProgress

