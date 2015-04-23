# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 08:57:49 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""



from numpy import *

def sigmoid(x):
	return 1./(1.+exp(-x))

def dsigmoidx(x):
	return exp(-x)/(1.0 + exp(-x))**2

def dsigmoidy(y):
	return y - y**2

class nn_simple():
	def __init__(self, ni, nh, no, bias = True, wRange = 0.3):
		self.epochs = 0
		self.ds_i = []
		self.ds_o = []
		self.nd = 0

		self.ni = ni + 1 if bias else 0
		self.nh = nh
		self.no = no

		self.ai = ones(self.ni)
		self.ah = ones(self.nh)
		self.ao = ones(self.no)

		self.wi = random.rand(self.ni, self.nh)*wRange
		self.wo = random.rand(self.nh, self.no)*wRange

		# last delta
		self.li = zeros((self.ni, self.nh))
		self.lo = zeros((self.nh, self.no))


	def act(self, inps):
		inps = array(inps, dtype=float)

		self.ai[:len(inps)] = inps

		for j in range(self.nh):
			s =  sum(self.ai * self.wi[:,j])
			self.ah[j] = sigmoid(s)

		for j in range(self.no):
			s =  sum(self.ah * self.wo[:,j])
			self.ao[j] = sigmoid(s)

		return self.ao

	def bp(self, tars, r, t):
		do = dsigmoidy(self.ao) * (tars - self.ao)

		err = zeros(self.nh)
		for i in range(self.nh):
			err[i] = sum(do*self.wo[i])
		dh = dsigmoidy(self.ah)*err

		#update weights
		for i in range(self.nh):
			delta = do * self.ah[i]
			self.wo[i] += r * delta + t * self.lo[i]
			self.lo[i] = delta

		for i in range(self.ni):
			delta = dh * self.ai[i]
			self.wi[i] += r * delta + t * self.li[i]
			self.li[i] = delta

		#return err
		return 0.5*sum((tars - self.ao)**2)

	def addSample(self, inps, tars):
		self.ds_i.append(inps)
		self.ds_o.append(tars)
		self.nd +=1

	def train(self, epoch = 1000, r = 0.5, t = 0.1):
		for i in range(epoch):
			err = 0
			for j in range(self.nd):
				self.act(self.ds_i[j])
				err += self.bp(self.ds_o[j], r, t)
		self.epochs += epoch
		return err

if __name__ == '__main__':
	net = nn_simple(2,5,1, 0.3)
	net.addSample([0,0], [0])
	net.addSample([1,1], [0])
	net.addSample([0,1], [1])
	net.addSample([1,0], [1])

	print net.act([0,0])
	print net.act([1,1])
	print net.act([0,1])
	print net.act([1,0])

	#net.weights()
	#print net.train(500, 1,0)
	#net.weights()
	#print net.train(500, 1,0)
	#net.weights()

	r = 0.5
	t = 0.1

	for i in range(10):
		print net.train(1000, r, t)

	print '-' * 10
	print net.act([0,0])
	print net.act([1,1])
	print net.act([0,1])
	print net.act([1,0])
