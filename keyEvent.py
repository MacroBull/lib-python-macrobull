# -*- coding: utf-8 -*-
"""
Created on Mon May  5 19:25:59 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

example:
	from macrobull.keyEvent import *
	import time

	with keyCtlHelper():
		while 1:
			time.sleep(0.5)
			if keyPressed():
				print readkey()

"""


import termios, fcntl, sys, os
import select

def initControl(termFlags = None, fdFlags = None):

	global fd, oldterm, oldflags

	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	newattr = termios.tcgetattr(fd)


	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	if termFlags:
		newattr[3] = termFlags

	newFdFlags = oldflags | os.O_NONBLOCK
	if fdFlags:
		newFdFlags = fdFlags

	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	fcntl.fcntl(fd, fcntl.F_SETFL, newFdFlags)

def restoreControl():

	global fd, oldterm, oldflags

	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


def readkey(n = 1):
	return sys.stdin.read(n)

def keyPressed():
	return select.select([sys.stdin],[],[],0)[0] != []


class keyCtlHelper:
	def __enter__(self):
		initControl()
		return True

	def __exit__(self, *args):
		restoreControl()
		return True

