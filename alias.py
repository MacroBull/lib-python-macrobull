# -*- coding: utf-8 -*-
"""
Created on %(date)
Project	:Python-Project
Version	:0.0.1
@author	:MacroBull
alias for function 
example: sum=alias(lambda:a+b)
"""

class simAlias():
	'''simple alias, cover limited range, no exception handling'''

	def __init__(self,func):
		self.target=func


	def __call__(self,*args,**kw):
		return self.target()(*args,**kw)

	def __getattribute__(self, attr, oga=object.__getattribute__):
		subject = oga(self,'__subject__')
		if attr=='__subject__':
			return subject
		return getattr(subject,attr)

	def __nonzero__(self):
		return bool(self.target())

	def __getitem__(self,arg):
		return self.target()[arg]

	def __setitem__(self,arg,val):
		self.target()[arg] = val

	def __delitem__(self,arg):
		del self.target()[arg]

	def __getslice__(self,i,j):
		return self.target()[i:j]


	def __setslice__(self,i,j,val):
		self.target()[i:j] = val

	def __delslice__(self,i,j):
		del self.target()[i:j]

	def __contains__(self,ob):
		return ob in self.target()

	for name in 'repr str hash len abs complex int long float iter oct hex'.split():
		exec "def __%s__(self): return %s(self.target())" % (name,name)

	for name in 'cmp', 'coerce', 'divmod':
		exec "def __%s__(self,ob): return %s(self.target(),ob)" % (name,name)

	for name,op in [
		('lt','<'), ('gt','>'), ('le','<='), ('ge','>='),
		('eq','=='), ('ne','!=')
	]:
		exec "def __%s__(self,ob): return self.target() %s ob" % (name,op)

	for name,op in [('neg','-'), ('pos','+'), ('invert','~')]:
		exec "def __%s__(self): return %s self.target()" % (name,op)


	del name, op

	# Oddball signatures

	def __rdivmod__(self,ob):
		return divmod(ob, self.target())

	def __pow__(self,*args):
		return pow(self.target(),*args)


	def __rpow__(self,ob):
		return pow(ob, self.target())

from korepwx.proxies import CallbackProxy

def fulAlias(subject):
	'''use callback proxy alias, better but still no exception handling'''
	return CallbackProxy(subject)

alias=simAlias

