#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 02:48:22 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""

from macrobull.cc98 import *

import sys, time, os

c = CC98()
#c.setAccount('MidoriYakumo', '233233')

#pl = pull(lambda n:c.getPostList((100, n)), 1, 1, lambda p:u'抢楼' in p.title)

if len(sys.argv) == 1:
	while 1:
		try:
			pl = filter(lambda p:u'抢楼' in p.title, c.getPostList((100, 1)))
			if not(pl): raise Exception("Oh suck!")
			for p in pl:
				print(u"{} / {}\n{}\n{}\n".format(p.response, p.datetime, p.title, c.postUrl(p.url)))
				os.popen('notify-send -i twitter-logo 抢楼！ "{}"'.format(p.title.encode('utf-8')))
			break
		except:
			print("Idle.")

		time.sleep(60 * 1)

else:
	url = c.postUrl(sys.argv[1])
	target = int(sys.argv[2]) - 1
	if len(sys.argv)>3:
		comment = sys.argv[3]
	else:
		comment = u"抢！"

	p = c.getPost(url)
	cf = c.getPostViewCnt(p)
	while cf < target:
		p = c.getPost(url)
		cf = c.getPostViewCnt(p)
		print("Current floor:", cf)
		time.sleep(0.5)
	while cf == target:
		r = c.replyPost(p , comment)
		if r: print("Gotta!")
		p = c.getPost(url)
		cf = c.getPostViewCnt(p)
		print("Current floor:", cf)


#c.dumpResp()

