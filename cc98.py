#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 23:22:24 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""

import requests
from bs4 import BeautifulSoup
from hashlib import md5
import os


URL_BASE = "http://www.cc98.org/"
URL_LOGIN = URL_BASE + "sign.asp"
COOKIE_DOMAIN = "www.cc98.org"
COOKIE_JAR = os.getenv('HOME')+'/.myjar/cookie/' + COOKIE_DOMAIN


def dict2obj(d):
	from collections import namedtuple
	objClass=namedtuple('ParsedDict',' '.join(d.keys()))
	return objClass(**d)

class CC98Exception(Exception):
	def __str__(self):
		r = ''
		if type(self.args[0]) is int:
			r += '[' + str(self.args[0]) + '] '
		r += self.args[-1]
		return r

class CC98():

	def setAccount(self, username, password):
		self._username = username
		self._password = password

	def boardUrl(self, url):
		if type(url) is str:
			if not(url.startswith('http://')):
				url = URL_BASE + url
		elif len(url) == 2:
			if type(url) is dict:
				url = (url['bid'], url['id'])
			url = URL_BASE + "list.asp?boardID={}&page={}".format(*url)
		return url

	def postUrl(self, url):
		if type(url) is str:
			if not(url.startswith('http://')):
				url = URL_BASE + url
		elif len(url) == 2:
			if type(url) is dict:
				url = (url['bid'], url['id'])
			url = URL_BASE + "dispbbs.asp?boardID={}&ID={}".format(*url)
		return url

	def checkPageStatus(self, page):
		if u"服务器维护中" in page.title.text:
			raise CC98Exception(u"服务器维护中")

	def login(self, hidden = 2):

		if not( "_username" in self.__dict__
			and "_password" in self.__dict__):
			raise CC98Exception("Account not setup.")

		url = URL_LOGIN
		params = dict(a = 'i'
			, u = self._username.encode()
			, p = md5(self._password.encode()).hexdigest()
			, userhidden = hidden
			)

		r = requests.post(url, params = params)

		return r

	@property
	def cookie(self):
		if "_cookie" not in self.__dict__:
			self._cookie = self.getCookie()
		return self._cookie

	def getCookie(self, force = False, hidden = 2):
		try:
			if force: raise Exception()
			cookies = eval(open(COOKIE_JAR, 'r').read())
		except BaseException:
			r = self.login(hidden = hidden)
			if r.text == '9898':
				cookies = r.cookies.get_dict()
				f = open(COOKIE_JAR, 'w')
				f.write(repr(cookies))
				f.close()
			else:
				raise CC98Exception("Login Error: response is " + r.text)
		return cookies

	def dumpResp(self):
		f = open('/tmp/cc98.html', 'w')
		f.write(self._r.text.encode('utf-8'))
		f.close()

	def getPost(self, url):
		url = self.postUrl(url)
		page = BeautifulSoup(requests.get(url, cookies = self.cookie).text)
		self.checkPageStatus(page)
		return page

	def getPostViewCnt(self, page):
		field = page.find(id='topicPagesNavigation')
		return int(field.b.text)

	def replyPost(self, page, comment, expression = 'face22.gif'):

		form = page.find(id='fastReplyForm')

		data = {}
		for tag in form.find_all('input'):#, recursive=False):
			if tag.has_attr('name') and tag.has_attr('value'):
				data[tag['name']] = tag['value']

		data['Expression'] = expression
		data.pop('Submit')
		data['Content'] = comment

		headers = dict(origin = URL_BASE
#			, referer = url
			, referer = URL_BASE
			)

		r = requests.post(self.postUrl(form['action'])
			, headers = headers
			, cookies = self.cookie
			, data = data
			)

		self._r = r

		return len(BeautifulSoup(r.text).find_all('meta'))>2

	def getPostList(self, url):

		url = self.boardUrl(url)
		page = BeautifulSoup(requests.get(url, cookies = self.cookie).text)
		self.checkPageStatus(page)
		tb = page.find('tbody')

		r = []
		for c in tb.find_all('tr', recursive=False)[2:]:
			tr = c.find_all('td', recursive=False)
			respView = tr[3].text.strip()
			dateRep = tr[4].text.strip()
			r.append(dict2obj(dict(type=tr[0].span['title']
				, url=tr[1].a['href']
				, title=tr[1].text.strip()
				, author=tr[2].text.strip()
				, response=int(respView.split('/')[0])
				, view=int(respView.split('/')[1])
				, datetime=dateRep.split('|')[0].strip()
				, reply=''.join(dateRep.split('|')[1:])
			)))

#		self._r = tr
		return r

def pull(gen, cnt, start = 1, filt = lambda p:True):
	r = []
	while len(r) < cnt:
		r += filter(filt, gen(start))
		start += 1
	return r[:cnt]





