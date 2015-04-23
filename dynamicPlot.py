# -*- coding: utf-8 -*-
"""
Created on 2013.09.28
Project	:Python-Project
Version	:1.0
@author	:MacroBull

usage:


	from numpy import sin, cos
	from macrobull.dynamicPlot import dynamicFigure, average


	df=dynamicFigure(updateInterval=100,screenLen=30)

	def update(fs):
		df.appendData([sin(fs/5.)],'Sine',211,procFunc=[lambda x,y:average(5,x,y), lambda x,y:average(0,x,y) ])
		df.appendData([cos(fs/5.)],'Cosine',212)


	df.newData=update

	df.run()

"""

NaN=float('nan')

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from macrobull.misc import extend, defaultSubplotMargin, average


defaultProcFunc=[lambda x,y:average(60,x,y), lambda x,y:average(0,x,y) ]
defaultFlotLabels=['1 min avg','all avg']
defaultPlotArgs=dict(alpha=0.7, linewidth=1.2, marker='o', markersize=2.4)
defaultFlotArgs=dict(alpha=0.3, linewidth=2.4)


class datum():

	def __init__(self,x,y, label, subPos=111, procFunc=[], plotArgs=defaultPlotArgs, flotLabels= defaultFlotLabels, flotArgs=defaultFlotArgs):
		self.x=x
		self.y=y
		self.label=label
		self.subPos=subPos
		self.procFunc=procFunc
		self.plotArgs=plotArgs
		self.flotArgs=flotArgs
		self.flotLabels=flotLabels

def passFunc():
	pass

def timeDiv(start,end,l):
	return np.linspace(start,end,l+1)[1:]#.round(0)

class dynamicFigure():

	def __init__(self, updateInterval=1000, screenLen=300 ):
		self.updateInterval=updateInterval
		self.screenLen=screenLen
		self.fig = plt.figure()
		plt.subplots_adjust(**defaultSubplotMargin)
		self.fig.canvas.mpl_connect('button_press_event', self.buttonHandler)
		self.fig.canvas.mpl_connect('key_press_event', self.keyHandler)
		self.pause=False
		self.subplots={}
		self.plots={}
		self.flots={}
		self.data={}
		self.ylim={}
		self.newYLim=self.ylim_allInView
		self.lastTimestamp=time.time()
		self.ani = animation.FuncAnimation(self.fig, self.update, interval=self.updateInterval)

	def __null__(self, *args, **kwargs):
		pass

	def run(self):
		self.pause=False
		plt.show()
		self.__destory__()


	def update(self,fs):

		if self.pause:
			self.lastTimestamp=time.time()
			return 1

		now=time.time()
		self.scrollData(now-self.screenLen)
		self.newData(fs)
		self.lastTimestamp=time.time()

		for label in self.data.keys():
			d=self.data[label]
			self.check_subplot(d.subPos, label)

			if label in self.plots:
				self.plots[label].set_xdata( d.x  + self.screenLen -now)
				self.plots[label].set_ydata( d.y)

				for i,f in enumerate( d.procFunc):
					self.flots[label][i].set_xdata( d.x  + self.screenLen -now)
					self.flots[label][i].set_ydata(f( d.x, d.y))

			else:
				self.plots[label] = self.subplots[ d.subPos].plot( d.x  + self.screenLen -now, d.y, label=label, **d.plotArgs)[0]

				self.flots[label]=[]
				for i,f in  enumerate(d.procFunc):
					self.flots[label].append(self.subplots[ d.subPos].plot( d.x  + self.screenLen -now, f( d.x, d.y), label=d.flotLabels[i], **d.flotArgs)[0])

		for pos in self.subplots:
			self.subplots[pos].legend( loc='upper left',prop={'size':9})

		if self.newYLim():
			self.applyYLim()

	def check_subplot(self, pos, title):
		if not(pos in self.subplots):
			self.subplots[pos] = self.fig.add_subplot(pos,title=title)
			self.subplots[pos].set_xlim(0,self.screenLen)
			return None
		return self.subplots[pos]


	def scrollData(self,thresTime):
		for label in self.data.keys():
			p=-1
			for i in range(len( self.data[label].x)):
				if  self.data[label].x[i]>=thresTime:
					p=i
					break
			if  p>=0:
				self.data[label].x= self.data[label].x[i:]
				self.data[label].y= self.data[label].y[i:]
			else:
				self.data[label].x=np.array([])
				self.data[label].y=np.array([])

	def newData(self,fs):
		pass

	def ylim_allInView(self):
		#for pos in self.ylim: self.ylim[pos]=None
		for pos in self.subplots: self.ylim[pos] = None
		for label in self.data.keys():
			d=self.data[label]
			if len(d.y)==0:
				self.data.pop(label)
				continue

			ymin, ymax= d.y.min(), d.y.max()
			for i in range(len(d.procFunc)):
				ymin = min( ymin , np.array(self.flots[label][i].get_ydata()).min())
				ymax = max( ymax , np.array(self.flots[label][i].get_ydata()).max())
			if self.ylim[d.subPos]:
				ylmin, ylmax = self.ylim[d.subPos]
				self.ylim[d.subPos] = (min(ylmin,ymin) , max(ylmax,ymax) )
			else:
				self.ylim[d.subPos] = (ymin , ymax)
		return True

	def ylim_28InView(self):
		#for pos in self.ylim: self.ylim[pos]=None
		for pos in self.subplots: self.ylim[pos] = None
		for label in self.data.keys():
			d=self.data[label]
			if len(d.y)==0:
				self.data.pop(label)
				continue

			ymin, ymax= d.y.min(), d.y.max()
			for i in range(len(d.procFunc)):
				ymin = min( ymin , np.array(self.flots[label][i].get_ydata()).min())
				ymax = max( ymax , np.array(self.flots[label][i].get_ydata()).max())
			if self.ylim[d.subPos]:
				ylmin, ylmax = self.ylim[d.subPos]
				self.ylim[d.subPos] = (min(ylmin,ymin) , max(ylmax,ymax) )
			else:
				self.ylim[d.subPos] = (ymin , ymax)
		return True

	def applyYLim(self):
		for pos in self.ylim:
			if self.ylim[pos]:
				self.subplots[pos].set_ylim(*extend(self.ylim[pos][0],self.ylim[pos][1],0.1))


	def appendData(self, y, label, subPos=None, x=[], **kwargs):
		if y==[]: return
		#if NaN
		now=time.time()
		y=np.array(y)

		if label in self.data:
			if x==[] :
				x = timeDiv(self.lastTimestamp,now,len(y))
			else:
				x= np.array(x)
			self.data[label].x = np.concatenate( [ self.data[label].x, x ] )
			self.data[label].y = np.concatenate( [ self.data[label].y, y ] )

			if subPos: self.data[label].subPos=subPos
		else:

			self.data[label] = datum(timeDiv(self.lastTimestamp,now,len(y)), y, label, **kwargs)
			if subPos:
				self.data[label].subPos=subPos
			else:
				if self.plots == {}:
					self.data[label].subPos=111
				else:
					self.data[label].subPos=self.subplots.keys()[-1]
			sp=self.check_subplot(self.data[label].subPos, title=label)
			if sp:
				sp.set_title(sp.get_title() + ' & ' + label)



	def __destory__(self):
		pass


	def buttonHandler(self,event):
		pass

	def defaultKeyHandler(self,event):
		#print event.key
		if event.key=='i': self.pause=not(self.pause)

	def keyHandler(self,event):
		return self.defaultKeyHandler(event)
		pass
