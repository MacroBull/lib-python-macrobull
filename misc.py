

defaultPlotArgs=dict(alpha=0.6	,linewidth=1.5)
defaultPlotArgs_bold=dict(alpha=0.6	,linewidth=2.5)
defaultSubplotMargin=dict(left=0.07,bottom=0.09,
	right=0.94,top=0.96,
	wspace=0.18, hspace=0.20)

#defaultPlotArgs = defaultPlotLine

#using rc file now@$HOME/.config/matplotlib/matplotlibrc
'''
import matplotlib

matplotlib.rc('font', **defaultPlotFont)
matplotlib.rc('lines', **defaultPlotLine)
'''


initSympy = """
from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
"""


def mplTheme(s=None):
	global mpl
	if not('mpl' in globals()): import matplotlib as mpl
	import os
	rcpath = os.getenv("HOME") + '/.config/matplotlib/'
	rcfile = None
	try:
		if s:
			rcfile = rcpath+s
			mpl.rc_file(rcfile)
		else:
			import random
			rclist = os.listdir(rcpath)
			rcfile = rcpath+rclist[random.randint(0, len(rclist)-1)]
			mpl.rc_file(rcfile)
	except IOError:
		pass
	return rcfile

def exclusiveSplit(s, sList = [' ', '\t', ','], index = 0):
	if index<len(sList):
		r = []
		for t in s.split(sList[index]):
			if t != '':
				r += exclusiveSplit(t, sList, index + 1)
		return r
	else:
		return [s]


def tex(s):
	''' XD '''
	r = ''
	eng = False
	for c in s:
		if (c<'\x7f')^(eng):
			r += r'$' + c
			eng = not eng
		else:
			r += c
	if eng: r += r'$'
	return r
	#return r'$'+s+r'$'

#def linear(a,b,u):
	#return a*u+b*(1-u)

#def extend(a,b,u):
	#return (a*(1+u)+b*-u,a*-u+b*(1+u))


def average(t,x,y):
	import numpy as np
	l=len(x)
	if t==0:
		return np.average(y).repeat(l)

	t/=2
	res=[]
	for i in range(l):
		st=i
		while (st>0) and (x[st]>x[i]-t): st-=1
		en=i
		while (en<l-1) and (x[en]<x[i]+t): en+=1
		res.append(np.average(y[st:en+1]))

	return np.array(res)

def texArrayPrint(a):
	if len(a.shape)==2:
		print("\\begin{equation}\\left[\\begin{array}{"+"c"*a.shape[0]+'}')
		for i in range(a.shape[0]):
			print(repr(a[i]).replace('array([','').replace('])','\\\\').replace(',',' &'))
		print("\\end{array}\\right]\\end{equation}")

def arrayNormalize(f,rangeInByte=True):
	maxv,minv=f.max()-f.min(),f.min()
	sf=f.shape
	r=f.reshape(-1)-minv
	if rangeInByte:
		for i in range(len(r)): r[i]=int(round(r[i]*255/maxv))
	return r.reshape(sf)


def serialChecker(autoChoice=True, *devType): # autoChoice : find first accessible one
	import os
	DEV_PATH="/dev/"
	if devType==():
		devType=["ttyUSB", "ttyAMA", "ttyACM", "rfcomm"]
	else :
		devType = list(devType)
		for i in range(len(devType)):
			if devType[i].isupper():
				devType[i] = "tty" + devType[i]

	'''#order changes:
	devFilter=' '.join([DEV_PATH+t+'*' for t in devType])
	devs=os.popen('ls '+devFilter).read().split()
	'''
	devs=[]
	for t in devType:
		devs += os.popen('ls ' + DEV_PATH+t+'* 2> /dev/null').read().split()

	if devs==[]: raise IOError(2,"No avaliable device.")

	if autoChoice:
		for d in devs:
			if os.access(d,os.R_OK|os.W_OK):
				return d

	for d in devs:
		print("Permission for "+d+" ?")
		if os.access('/usr/bin/kdesudo',os.X_OK):
			os.popen('kdesudo chmod 666 '+d)
		elif os.access('/usr/bin/kdesu',os.X_OK):
			os.popen('kdesu chmod 666 '+d)
		elif os.access('/usr/bin/gksudo',os.X_OK):
			os.popen('gksudo chmod 666 '+d)

		if os.access(d,os.R_OK|os.W_OK):
			return d

	raise IOError(13,"All devices' permissions denied.")
	return None

def json_dict2obj(d):
	from collections import namedtuple
	objClass=namedtuple('ParsedJson',' '.join(d.keys()))
	return objClass(**d)