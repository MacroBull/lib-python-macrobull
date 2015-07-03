#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:53:37 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""


import struct
from ctypes import  *

class StlinkVersion(Structure):
	_fields_ = [("stlink_v", c_uint)
		,("jtag_v", c_uint)
		,("swim_v", c_uint)
		,("st_vid", c_uint)
		,("stlink_pid", c_uint)
		]

class Stlink(Structure):
#	pass
	_fields_ = [("backend", c_ulonglong)
		,("backend_data", c_ulonglong)
#		,("c_buf", c_ubyte * 32)
		,("c_buf", c_char * 32)
#		,("q_buf", c_ubyte * (1024 * 100))
		,("q_buf", c_char * (1024 * 100))
		,("q_len", c_int)
		,("verbose", c_int)
		,("core_id", c_uint)
		,("chip_id", c_uint)
		,("core_stat", c_int)
		,("flash_base", c_uint)
		,("flash_size", c_size_t)
		,("flash_pgsz", c_size_t)
		,("sram_base", c_uint)
		,("sram_size", c_size_t)
		,("sys_base", c_uint)
		,("sys_size", c_size_t)
		,("version", StlinkVersion)
		]


stlink = cdll.LoadLibrary("libstlink.so")
stlink.stlink_open_usb.restype = POINTER(Stlink)

sl = stlink.stlink_open_usb(10, 0)

if not(sl):
	raise Exception("STLink not available.")

sl_t = sl.contents
print("STLink Device:", hex(sl_t.chip_id), hex(sl_t.core_id))

stlink.stlink_version(sl)
stlink.stlink_enter_swd_mode(sl)

#stlink.stlink_reset(sl)
stlink.stlink_force_debug(sl)
stlink.stlink_run(sl)
stlink.stlink_status(sl)

#s
#time.sleep(1)
#


STRUCT_FORMAT_DICT = {1:'B', -1:'b', 2:'H', -2:'h', 4:'L', -4:'l'
	, 8:'Q', -8:'q'}

class Source():
	def __init__(self):
		self.requests = []

	def addRequest(self, baseAddr, wordSize = 4, length = 1, spec = 1):
		self.requests.append([baseAddr, wordSize, length, spec])

	def poll(self):
		r = []
		for baseAddr, wordSize, length, spec in self.requests:
			reqSize = wordSize * length
			while reqSize & 3: reqSize += 1
			stlink.stlink_read_mem32(sl, baseAddr, reqSize)
			buf = sl_t.q_buf[:wordSize * length]
			buf += b'\0' * (wordSize * length - len(buf))
			if spec == 0:
				r.append(buf)
			else:
				if spec == -1: wordSize *= spec
				r.append(struct.unpack('<' + STRUCT_FORMAT_DICT[wordSize]*length, buf))
		return r
		# try yield ?


