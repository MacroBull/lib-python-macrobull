# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 13:26:06 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

"""



from math import asin, sqrt


def intPoint(p):
	return (int(p[0]), int(p[1]))

'''
def crossAngle(p0, p1, p2, p3):
	x0, y0 = p0
	x1, y1 = p1
	x2, y2 = p2
	x3, y3 = p3

	x1 -= x0
	y1 -= y0
	x3 -= x2
	y3 -= y2

	cp13 = x1*y3 - x3*y1
	sp13 = ((x1**2 + y1**2) * (x3**2 + y3**2))**0.5

	return asin(cp13/sp13)
'''

def crossAngle(p0, p1, p2, p3):
	x1 = p1[0] - p0[0]
	y1 = p1[1] - p0[1]
	x2 = p2[0] - p3[0]
	y2 = p2[1] - p3[1]

	cp13 = float(x1*y2 - x2*y1)
	sp13 = ((x1**2 + y1**2) * (x2**2 + y2**2))**0.5

	return asin(cp13/sp13)

def projModelling(p0, p1, p2, p3):
	x0, y0 = p0
	x1, y1 = p1
	x2, y2 = p2
	x3, y3 = p3

	denom = float((y1 - y0) * (x3 - x2) - (y2 - y3) * (x0 - x1))
	if denom == 0:
		xs = ys = 0
	else:
		cp23 = x2*y3 - x3*y2
		cp10 = x1*y0 - x0*y1
		numx = cp23 * (x0 - x1) - cp10 * (x3 - x2)
		numy = cp23 * (y1 - y0) - cp10 * (y2 - y3)
		xs = numx / denom
		ys = numy / -denom

	denom = float((y3 - y0) * (x1 - x2) - (y2 - y1) * (x0 - x3))
	if denom == 0:
		xt = yt = 0
	else:
		cp21 = x2*y1 - x1*y2
		cp30 = x3*y0 - x0*y3
		numx = cp21 * (x0 - x3) - cp30 * (x1 - x2)
		numy = cp21 * (y3 - y0) - cp30 * (y2 - y1)
		xt = numx / denom
		yt = numy / -denom


	global proj_as, proj_at, proj_s, proj_t
	global proj_p0, proj_p1, proj_p2, proj_p3
	proj_p0, proj_p1, proj_p2, proj_p3 = p0, p1, p2, p3
	
	
	global proj_sx, proj_sy, proj_tx, proj_ty, proj_vx1, proj_vy1, proj_vx3, proj_vy3, proj_l12, proj_l32

	proj_vx1 = p1[0] - p0[0]
	proj_vy1 = p1[1] - p0[1]

	proj_vx3 = p3[0] - p0[0]
	proj_vy3 = p3[1] - p0[1]
	
	proj_sx = xs
	proj_sy = ys
	
	proj_tx = xt
	proj_ty = yt
	
	proj_l12 = proj_vx1*proj_vx1 + proj_vy1*proj_vy1
	proj_l32 = proj_vx3*proj_vx3 + proj_vy3*proj_vy3
	

	proj_as, proj_at, proj_s, proj_t =  crossAngle(p0, p1, p2, p3), crossAngle(p0, p3, p2, p1), (xs, ys), (xt, yt)
	return proj_as, proj_at, proj_s, proj_t



def rProj2(qx, qy):

	x2 = qx - proj_sx
	y2 = qy - proj_sy

	cp13 = float(proj_vx1*y2 - x2*proj_vy1)
	sp13 = sqrt(proj_l12 * (x2**2 + y2**2))

	qs = asin(cp13/sp13) / proj_as

	x2 = qx - proj_tx
	y2 = qy - proj_ty

	cp13 = float(proj_vx3*y2 - x2*proj_vy3)
	sp13 = sqrt(proj_l32 * (x2**2 + y2**2))

	qt = asin(cp13/sp13) / proj_at

	return abs(qs), abs(qt)



def rProj(q):

	global proj_as, proj_at, proj_s, proj_t

	if proj_as:
		qs = crossAngle(proj_p0, proj_p1, q, proj_s) / proj_as
	else:
		raise ValueError("parallel on S")

	if proj_at:
		qt = crossAngle(proj_p0, proj_p3, q, proj_t) / proj_at
	else:
		raise ValueError("parallel on T")

	return abs(qs), abs(qt)

