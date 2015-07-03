# -*- coding: utf-8 -*-
"""
Created on %(date)
Project	:Python-Project
Version	:0.0.1
@author	:Macrobull

Some utilities for oscilloscope data processing:
"""


import numpy as np
from scipy import signal
from scipy.optimize import leastsq
from pylab import *

#from __init__ import plotBlankRemains
plotBlankRemains = 0.1

from macrobull.linear import linear

def generator(waveType,t,z=0,a=1,w=1,p=0,d=0.5):
	'''
	a simple generator to generate waveform in waveType

	example:
		wave=generator('triangle',linspace(-10,10),z=2,a=3,w=0.5,d=0.8)
	'''
	if waveType=='sine':
		return z+a*sin(w*2*pi*t+p)
	elif waveType=='square':
		return z+a*(np.int32((p+t/w)%1<d))
	elif waveType=='triangle':
		c=(p+t/w)%1
		return (c<=d)*(z+a*c/d)+(c>d)*(z+a*(1-c)/(1-d))

def peakExtractor(s,l=None	,minDiff=None):
	'''
	find peaks in a waveform
	l to decide the exact length of data
	minDiff is the minimum of peak to peak value to be considered default value is 1/16 of the max difference

	-no exception handing, if theres no peak found may present a error-
	'''
	if	l==None: l=len(s)
	if	minDiff==None: minDiff=(s.max()-s.min())/16

	minInterval=l/200

	hPos,lPos=[],[]
	smax,smin=s.min()+minDiff,s.max()-minDiff
	maxPos,minPos=0,0
	#find peaks
	for i in range(l):
		if s[i]>smax:
			smax=s[i]
			maxPos=i

		if s[i]<smin:
			smin=s[i]
			minPos=i

		if (s[i]<smax-minDiff)and(maxPos-minPos>minInterval):
		#if (s[i]<smax-minDiff)and(i-maxPos>minInterval):
			hPos.append(maxPos)
			smin=s[i]
			minPos=i

		if (s[i]>smin+minDiff)and(minPos-maxPos>minInterval):
		#if (s[i]>smin+minDiff)and(i-minPos>minInterval):
			lPos.append(minPos)
			smax=s[i]
			maxPos=i

	#proccess the last and the first peak
	if (s[-1]>smax-minDiff)and(s[-1]>smin+minDiff):
		hPos.append(maxPos)
	if (s[-1]<smin+minDiff)and(s[-1]<smax-minDiff):
		lPos.append(minPos)
	if len(hPos)==0:
		if s[:lPos[0]].max()>s[lPos[0]]+minDiff:
			hPos=[s[:lPos[0]].argmax()]+hPos
	elif len(lPos)==0:
		if (s[:hPos[0]].min()<s[hPos[0]]-minDiff):
			lPos=[s[:hPos[0]].argmin()]+lPos
	elif ((lPos[0]<hPos[0]) and (s[:lPos[0]].max()>s[lPos[0]]+minDiff)):
			hPos=[s[:lPos[0]].argmax()]+hPos
	elif ((hPos[0]<lPos[0]) and (s[:hPos[0]].min()<s[hPos[0]]-minDiff)):
			lPos=[s[:hPos[0]].argmin()]+lPos

	return [hPos,lPos]

def ppv(s,l=None):
	'''
	return max peak-peak value
	'''
	hPos,lPos=peakExtractor(s,l=l,minDiff=(s.max()-s.min())*0.8)
	return average(s[hPos])-average(s[lPos])

def accp(s):
	'''
	AC component
	'''
	return s-average(s)

def riseFallTime(tSpan	,s,l=None,retTh=False):
	'''
	return average rise time and fall time
	-return [-1,-1] if not valid-
	set retTh=True to return rise and fall progress' threshold append to result
	easy to indicate by using:
		plot( s.t[where((s.ch1>lth)& (s.ch1<hth))], s.ch1[where((s.ch1>lth)&(s.ch1<hth))])
	'''
	if	l==None: l=len(s)
	hPos,lPos=peakExtractor(s,l=l,minDiff=(s.max()-s.min())*0.8)

	hPeak=average(s[hPos])
	lPeak=average(s[lPos])
	thHigh	=hPeak*0.9+lPeak*0.1
	thLow	=hPeak*0.1+lPeak*0.9

	riseTimes=[]
	fallTimes=[]

	mids=(s>thHigh)+(s<thLow)
	st=0
	while (st<l)and not(mids[st]): st+=1
	en=l-1
	while (en>0)and not(mids[en]): en-=1
	pst=pen=0
	for i in range(st+1,en):
		if not(mids[i]):
			if mids[i-1]:	pst=i-1
			if mids[i+1]:
				pen=i+1
				if (s[pst]>thHigh)and(s[pen]<thLow):
					fallTimes.append(pen-pst-1)
				if (s[pst]<thLow)and(s[pen]>thHigh):
					riseTimes.append(pen-pst-1)
				#pst=i+1

	#print(riseTimes,fallTimes)
	if retTh:
		return (tSpan/l*	average(array(riseTimes))	,tSpan/l*	average(array(fallTimes)),thHigh,thLow)
	else:
		return (tSpan/l*	average(array(riseTimes))	,tSpan/l*	average(array(fallTimes)))



def peakAnnotator(t	,s,l=None	,minDiff=None	,arrowMinPos=None	,arrowMaxPos=None):
	'''
	annotate peaks in oscWave.plotWave
	arrowMaxPos and arrowMinPos to decide the height of the line
	'''
	hPos,lPos=peakExtractor(s,l,minDiff)

	if	arrowMinPos==None:
		arrowMinPos=s.min()*(1+plotBlankRemains)+s.max()*-plotBlankRemains
	if	arrowMaxPos==None:
		arrowMaxPos=s.max()*(1+plotBlankRemains)+s.min()*-plotBlankRemains

	textHight=(s.max()-s.min())/32 #half
	#print(arrowMinPos,arrowMaxPos)

	for i in range(len(hPos)):
		annotate('{:.2f}'.format(s[hPos[i]]),
					 xy=(t[hPos[i]],s[hPos[i]]),
					 xytext=(t[hPos[i]],arrowMaxPos+textHight),
					 va="center", ha="center",
					 arrowprops=dict(arrowstyle="->"	,color='red'	,alpha=0.7	,connectionstyle="arc3")
					 )
		#if hPos[i]!=hPos[i-1]:
		if i:
			annotate('',
					 xy=(t[hPos[i]],arrowMaxPos),
					 xytext=(t[hPos[i-1]],arrowMaxPos),
					 arrowprops=dict(arrowstyle="<->" ,color='red' ,alpha=0.7	,connectionstyle="arc3")
					 )
			text((t[hPos[i]]+t[hPos[i-1]])/2	,arrowMaxPos-textHight,
				 '{:.2f}'.format(t[hPos[i]]-t[hPos[i-1]]),
				 va="center", ha="center")

	for i in range(len(lPos)):
		annotate('{:.2f}'.format(s[lPos[i]]),
					 xy=(t[lPos[i]],s[lPos[i]]),
					 xytext=(t[lPos[i]],arrowMinPos-textHight),
					 va="center", ha="center",
						 arrowprops=dict(arrowstyle="->"	,color='blue'	,alpha=0.7	,connectionstyle="arc3")
					 )
		#if lPos[i]!=lPos[i-1]:
		if i:
			annotate('',
					 xy=(t[lPos[i]],arrowMinPos),
					 xytext=(t[lPos[i-1]],arrowMinPos),
					 arrowprops=dict(arrowstyle="<->",
									 color='blue'	,alpha=0.7	,connectionstyle="arc3")
					 )
			text((t[lPos[i]]+t[lPos[i-1]])/2	,arrowMinPos+textHight,
				 '{:.2f}'.format(t[lPos[i]]-t[lPos[i-1]]),
				 va="center", ha="center")

	#rearrange y limit
	ylim(arrowMinPos-textHight*2,arrowMaxPos+textHight*2)
	#yticks(np.linspace(arrowMinPos-textHight*2,arrowMaxPos+textHight*2,11))
	return


def distortion(s,waveType='sine',**kw):
	'''
	calculate the distortion of sine/triangle() wave by leastsq

	cause theres no time passed in, f,t should normalize to 1s, as:
		f=s.tSpan*10**s.timeOrder*s.chFreqs[0])
		t=1/f

	______________________________
	arguments:
		for sine wave:
			f:frequence,	p:initial phase
			return voltage distortion (sqrt(power))
		for triangle wave:
			t:period,	p:initial phase,	d:duty
			return max delta
	'''

	def dSine(p,x,y):
		z,a,w,p=p
		return y-(z+a*sin(w*x+p))
	def dSquare(p,x,y):
		z,a,t,p,d=p
		return y-(z+a*((p+x/t)%1<d))
	def dTriangle(p,x,y):
		z,a,t,p,d=p
		c=(p+x/t)%1
		return y-(c<=d)*(z+a*c/d)-(c>d)*(z+a*(1-c)/(1-d))


	x=linspace(0,1,len(s))
	if waveType=='sine':
		kws=dict(f=1,p=0)
		kws.update(kw)
		p0=[average(s),ppv(s)/2,kws['f']*(2*pi),kws['p']]
		q= leastsq(dSine, p0, args=(x,s))
		#plot(linspace(-25,25,len(s)),-dSine(q[0],x,s))
		return sqrt(np.add.reduce([dSine(q[0],x[i],s[i])**2 for i in range(len(s))])/sum(s**2))

	elif waveType=='triangle':
		kws=dict(t=1,p=0,d=0.5)
		kws.update(kw)
		p0=[average(s)-ppv(s)/2	,ppv(s),	kws['t']	,kws['p']	,kws['d']]
		q= leastsq(dTriangle, p0, args=(x,s))
		#print(q[0])
		#plot(x,dTriangle(q[0],x,s),color='pink',lw=2)
		return max([dTriangle(q[0],x[i],s[i]) for i in range(len(s))])/ppv(s)

		'''
	elif waveType=='square':
		kws=dict(t=1,p=0,d=0.5)
		kws.update(kw)
		p0=[average(s)-ppv(s)/2	,ppv(s),	kws['t']	,kws['p']	,kws['d']]
		q= leastsq(dSquare, p0, args=(x,s))
		#print(p0,q[0])
		return np.add.reduce([dSquare(q[0],x[i],s[i])**2 for i in range(len(s))])/sum(s**2)
	'''

def phaseShift(s1, s2, vOff = None):
	l = len(s1)
	if l != len(s2): return None
	if vOff:
		s1_ac = s1 - vOff
		s2_ac = s2 - vOff
	else:
		s1_ac = accp(s1)
		s2_ac = accp(s2)

	return arccos(sum([s1_ac[i]*s2_ac[i] for i in range(l)]) / sqrt(sum([a**2 for a in s1_ac]) * sum([a**2 for a in s2_ac]) ))

def timeShift(tSpan, s1, s2, bias = False):
	l = len(s1)
	if l != len(s2): return None
	conv = convolve(accp(s1),accp(s2)[::-1])
	if (bias) and (-conv.min()>conv.max()):
		if conv.argmin()>l:
			ts = conv[:l+1].argmax() - l
		else:
			ts = conv[l:].argmax()
	else:
		ts = conv.argmax() - l
	return tSpan*ts/float(l)

def phaseDetector(s1,s2):
	'''
	Sinusoidal phase detector
	'''
	return pi/2. - arcsin(8*average(accp(s1)*accp(s2))/(ppv(s1)*ppv(s2)))

def sineInfo(s, f = 3., report=True, debugPlot = False):
	'''
		f for repetition in s, input f = fft_f * tSpan
		return amp, freql, shift, THD
		real f = freql /tSpan
	'''
	l = len(s)
	t = array(range(l))
	a2 = ppv(s)

	from lmfit import minimize, Parameters, report_fit

	def err(params, t, s):
	    amp = params['amp'].value
	    shift = params['shift'].value
	    omega = params['freq'].value

	    model = amp * sin(t * omega * 2*pi + shift)
	    return model - s

	params = Parameters()
	params.add('amp',   value= a2,  min= a2 / 3)
	params.add('shift', value= 0.) #, min=-pi, max=pi)
	params.add('freq', value=f/l , min = 0.6*f/l, max = 1.4*f/l)

	resd = minimize(err, params, args=(t, s)).residual

	if report: report_fit(params)
	if debugPlot:
		figure()
		plot(s)
		plot(s+resd)

	return (params['amp'].value, params['freq'].value * l , params['shift'].value % (2*pi) - pi, sum(resd**2)/sum(s**2))


'''
def distortion_sine(s, f):
	l = len(s)
	t = array(range(l))
	ref = generator('sine', t, z = average(s), a =ppv(s)/2, w = f/l, p = 0)
	ref = generator('sine', t, z = average(s), a =ppv(s)/2, w = f/l, p = phaseShift(s, ref))
	#plot(s)
	#plot(ref)
	plot(s-ref)
'''