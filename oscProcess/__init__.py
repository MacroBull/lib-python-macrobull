# -*- coding: utf-8 -*-
"""
Created on Tue May 07 12:05:00 2013

@author: MacroBull

a module to process oscilloscope data
____________________________________
Constant
	plotBlankRemains is the blank border ratio in plot
"""

from pylab import *
import numpy as np
from numpy.fft import fft

#from . import oscFilter
#from . import oscUtility

#import oscFilter
#import oscUtility
#from macrobull.alias import alias

try:
	reduce
except NameError:
	from functools import reduce


from macrobull.linear import extend
from macrobull.misc import tex
#import neoScope
#import rigol

plotBlankRemains=0.1
#fftSound=0.1
#orders='n  u  m     k  M  G'
#orderPos=9
eps=1e-6

class oscWave(object):
	'''class of waves from oscilloscopes
		t:time
		ch:channels
		with
		Title(s),Units(s)
	'''

	def __init__(self,filename='None'):
		'''data source=filename'''
		self.source=filename

		self.tTitle='Time'
		self.tUnit=None
		self.t=[]
		self.__timeOrder=0 #real t=t*10^order

		self.chCnt=0
		self.chTitles=[]
		self.chs=[]
		self.chUnits=[]

		'''advance caculation'''

		self.__chFFTs=[]
		self.__chFreqs=[]


		'''read only function alias

		Original Version:
		self.tSpan=alias(lambda:self.t[-1]-self.t[0])
		self.l=alias(lambda:len(self.t))
		self.ch1=alias(lambda:self.chs[0])
		self.ch2=alias(lambda:self.chs[1])
		'''

	@property
	def tSpan(self):
		return self.t[-1]-self.t[0]

	@property
	def l(self):
		return len(self.t)

	@property
	def ch1(self):
		return self.chs[0]
	@ch1.setter
	def ch1(self,ch):
		self.chs[0]=ch

	@property
	def ch2(self):
		return self.chs[1]
	@ch2.setter
	def ch2(self,ch):
		self.chs[1]=ch

	@property
	def timeOrder(self):
		return self.__timeOrder
	@timeOrder.setter
	def timeOrder(self,order):#=None):
		'''adjust timer unit order
		leave order=None set to auto: absolute value of time will be in [10,100]
		'''

		if order==None:
			order=round(self.__timeOrder-1.5+log10(self.tSpan))

		order=int(order)
		self.t*=10**(self.__timeOrder-order)
		self.__timeOrder=order



	def applyAvgFilter(self):
		'''slightly denoise by calculate average value...'''
		for ch in self.chs[:self.chCnt]:
			ch=oscFilter.avgFilter(ch)

	@property
	def chFFTs(self):
		if self.__chFFTs==[]:
			self.fullFFT()
		return self.__chFFTs
	def fullFFT(self):
		'''calcuate all channels fft, stores result in chFFTs'''
		self.__chFFTs=[]
		for i in range(self.chCnt):
			self.__chFFTs.append(fft(self.chs[i])[:(self.l+1)//2]/self.l)

	@property
	def chFreqs(self):
		if self.__chFreqs==[]:
			self.calcFreq()
		return self.__chFreqs

	def __calcFreqArgs(self):
		r = []
		for i in range(self.chCnt):
			pos=1+abs(self.chFFTs[i][1:]).argmax()
			if pos<=self.l//4:
				if abs(self.chFFTs[i][pos])>abs(self.chFFTs[i][pos*2])*2:  #clearly A(f)>2*A(2*f) =w=
						r.append(pos)

				else: r.append(-1) #return -1 when no convincing result
			else: r.append(-1) #return -1 when no convincing result
		return r

	def calcFreq(self):
		'''
		calcuate all channels' frequence, stores result in chFreqs
		return -1 when no convincing result
		remember to do fullFFT() again after data modified
		'''
		self.__chFreqs=[]
		for pos in self.__calcFreqArgs():
			if pos==-1:
				self.__chFreqs.append(-1)
			else:
				self.__chFreqs.append(float(pos)/self.tSpan*(10**-self.timeOrder))

	def timeShift(self, ch1, ch2):
		return oscUtility.timeShift(self.tSpan,self.chs[ch1],self.chs[ch2])

	def phaseShift(self, ch1, ch2, method = "pf"):
		if method == "pf":
			return oscUtility.phaseShift(self.chs[ch1],self.chs[ch2], vOff = 0)
		elif method == "fft":
			fArgs = self.__calcFreqArgs()
			if (fArgs[ch1]==-1)or(fArgs[ch2]==-1):
				sys.stderr.write('phaseShift: Invalid base frequency ')
				return None
			else:
				try:
					fVal = self.chFFTs[ch2][fArgs[ch2]]
					phase = arctan(imag(fVal)/real(fVal))
					fVal = self.chFFTs[ch1][fArgs[ch1]]
					phase -= arctan(imag(fVal)/real(fVal))
				except ValueError as e:
					sys.stderr.write('phaseShift: Invalid arctan result '+repr(e))
					return None
				return phase
	@property
	def chTHDs(self):
		baseFreqs = self.__calcFreqArgs()
		print(baseFreqs)
		r = []
		for i,pos in enumerate(baseFreqs):
			r.append(1- abs(self.chFFTs[i][pos])**2 / sum(abs(self.chFFTs[i][1:])**2))
		return r



	def plotLissajous(self, plotChs=[0,1]	, **kw):
		'''plot Lissajous figure of two channels appointed by plotChs, default ch1 and ch2'''
		if self.chCnt<2: return -1	#invalid condition

		plotKw=dict(alpha=0.7	,linewidth=1.5)	#default plot style
		plotKw.update(kw)

		plot(self.chs[plotChs[0]]	,self.chs[plotChs[1]]	,label=self.chTitles[plotChs[0]]+' X '+self.chTitles[plotChs[1]]	, **plotKw)

		xlim(*extend(self.chs[plotChs[0]].min(), self.chs[plotChs[0]].max(), plotBlankRemains))
		ylim(*extend(self.chs[plotChs[1]].min(), self.chs[plotChs[1]].max(), plotBlankRemains))

		xlabel(self.chTitles[plotChs[0]]	+'\\' +self.chUnits[plotChs[0]])
		ylabel(self.chTitles[plotChs[1]]	+'\\' +self.chUnits[plotChs[1]])

		legend()


	def plotWave(self, plotChs=None	, **kw):
		'''plot Y-T figure of channels appointed by plotChs, default all channels'''
		if plotChs is None:	plotChs=range(self.chCnt)
		plotKw=dict(alpha=0.7	,linewidth=1.5)#default plot style
		plotKw.update(kw)

		for i in plotChs:
			plot(self.t	,self.chs[i]	,label=self.chTitles[i]	, **plotKw)

		#xlim(*extend(self.t.min(), self.t.max(), plotBlankRemains))
		#xticks(linspace(self.t[0]*(1+plotBlankRemains)	+self.t[-1]*-plotBlankRemains	,self.t[-1]*(1+plotBlankRemains)	+self.t[0]*-plotBlankRemains,11))
	    #xlim(wave.t.min()*1.2,wave.t.max()*1.2)

		if self.tUnit!=None:
			if self.timeOrder==0:
				orderStr=''
			else:
				orderStr="10^{"+repr(self.timeOrder)+'} '
			xlabel(tex(self.tTitle	+':'+orderStr +self.tUnit))	#show label of time
		if reduce(lambda u,v:u and (v==self.chUnits[0])	,self.chUnits[:self.chCnt]):
			ylabel(tex('Channels:'	+self.chUnits[0]))	#show label of channel if units are same

		legend()

	def merge(self,wave,tOff=0,update='-'):
		'''
		merge another oscWave class 'wave' into this
		tOff is the time offset added to 'wave'
		update={'-','='} means remain original data or replace it with 'wave' if time is the same

		'''

		if (self.tUnit!=wave.tUnit)	or	(self.chUnits[0]!=wave.chUnits[0]): #=_,=
			return -1

		wave.t+=tOff
		wave.TimeOrder=self.timeOrder #align at the same time unit order

		if (self.t.min()>wave.t.max()): #concatenate
			self.t=np.append(wave.t,self.t)
			for i in range(self.chCnt):
				self.chs[i]=np.append(np.zeros(wave.l),self.chs[i])
			for i in range(wave.chCnt):
				self.chs.append(np.append(wave.chs[i],np.zeros(self.l)))
		elif	(self.t.max()<wave.t.min()):
			self.t=np.append(self.t,wave.t)
			for i in range(self.chCnt):
				self.chs[i]=np.append(self.chs[i],np.zeros(wave.l))
			for i in range(wave.chCnt):
				self.chs.append(np.append(np.zeros(self.l)),wave.chs[i])
		elif (self.l==wave.l)	and	(abs(self.tSpan-wave.tSpan)<eps*self.tSpan):

			for i in range(wave.chCnt):
				self.chs.append(wave.chs[i])
				self.chTitles.append(wave.chTitles[i])
				self.chUnits.append(wave.chUnits[i])
			self.chCnt+=wave.chCnt
		elif update=='-':	#remain self and add wave at the same time
			before	=np.where(wave.t<self.t[0])
			after	=np.where(wave.t>self.t[-1])
			self.t=np.append(	np.append(wave.t[before],self.t)	,wave.t[after])
			for i in range(min(self.chCnt,wave.chCnt)):
				self.chs[i]=np.append(	np.append(wave.chs[i][before],self.chs[i])	,wave.chs[i][after])
		elif update=='=':
			#replace by wave at the same time
			before	=np.where(self.t<wave.t[0])
			after	=np.where(self.t>wave.t[-1])
			self.t=np.append(	np.append(self.t[before],wave.t)	,self.t[after])
			for i in range(min(self.chCnt,wave.chCnt)):
				self.chs[i]=np.append(	np.append(self.chs[i][before],wave.chs[i])	,self.chs[i][after])

'''
		elif update=='+':	#calcuate average data not avliable yet
			before	=np.where(wave.t<self.t[0])
			after	=np.where(wave.t>self.t[-1])
			self.t=np.append(	np.append(wave.t[before],(self.t+wave.)	,wave.t[after])
			for i in range(min(self.chCnt,wave.chCnt)):
				self.chs[i]=np.append(	np.append(wave.chs[i][before],self.chs[i])	,wave.chs[i][after])
'''
