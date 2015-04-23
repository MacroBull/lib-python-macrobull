# -*- coding: utf-8 -*-
"""
Created on %(date)
Project	:Python-Project
Version	:0.0.1
@author	:MacroBull
"""

#import sys

#from macrobull.oscProcess import *
import macrobull.oscProcess.rigol as rigol
import macrobull.oscProcess.neoScope as neo
import macrobull.oscProcess.tektronix as tek
from macrobull.oscProcess.oscUtility import *
import numpy

#sRigol=rigol.loadWaveFromFile(sys.argv[1])
#import neoScope need more arguments
#sNeo0=neo.loadWaveFromFile('/home/macrobull/workspace/Python/oscLibTest/neoscope/RAW037.BIN',Sa=651.0e3,ch1Div=5,ch2Div=5)
sNeo0=tek.loadWaveFromFile('F0001CH1.CSV')
sNeo1=tek.loadWaveFromFile('F0001CH2.CSV')
sNeo0.merge(sNeo1)
sTek0=tek.loadWaveFromFile('F0002CH1.CSV')
sTek1=tek.loadWaveFromFile('F0002CH2.CSV')
sRigol0=rigol.loadWaveFromFile('(13).csv')
sRigol1=rigol.loadWaveFromFile('(15).csv')

#overwrite rigol0 part with rigol1
sRigol0.merge(sRigol1,update='-')
#add a generated waveform into rigol0
#sRigol1.chs[0]=generator('triangle',sRigol0.t,z=2,a=3,w=0.005,d=0.8)
sRigol1.ch1=generator('triangle',sRigol0.t,z=2,a=3,w=0.005,d=0.8)
sRigol1.t=sRigol0.t
sRigol1.chCnt=1
sRigol0.merge(sRigol1)
#merge Tek0's ch1 and ch2
sTek0.merge(sTek1)


#tweak

sNeo0.applyAvgFilter()
sNeo0.timeOrder=None
sRigol0.applyAvgFilter()
sRigol0.timeOrder=None
sTek0.applyAvgFilter()
sTek0.applyAvgFilter()
sTek0.timeOrder=-6

#sNeo0.plotWave()
#sTek0.plotWave()
#show()


#calcutaion

#sNeo0.calcFreq()
#sRigol0.calcFreq()
print('frequence calculation:{},{}'.format(
	sNeo0.chFreqs,	sRigol0.chFreqs))
#print(abs(sRigol0.chFFTs[0][:15]),abs(sRigol0.chFFTs[0][1:15]).argmax()+1)
print('peak-peak value:{:.2f},{:.2f},{:.2f}'.format(
	ppv(sNeo0.ch1), ppv(sNeo0.ch2), ppv(sRigol0.ch1)))
normf=sNeo0.tSpan*10**sNeo0.timeOrder*sNeo0.chFreqs[0]
print('distortion of neo0: ch1 as sine= {}, ch1 as triangle={}'.format(distortion(sNeo0.ch1,f=normf),distortion(sNeo0.ch1,waveType='triangle',t=1./normf)))

figure()
subplot(221)
sNeo0.plotWave()
peakAnnotator(sNeo0.t,sNeo0.ch1,minDiff=1)
subplot(222)
#sNeo0.plotLissajous()
sRigol0.plotLissajous()
subplot(223)
sRigol0.plotWave(alpha=0.5,lw=3)
subplot(224)
sTek0.plotWave()

rt,ft,hth,lth=riseFallTime(sTek0.tSpan,sTek0.ch1,retTh=True)
plot(sTek0.t[where((sTek0.ch1>lth)& (sTek0.ch1<hth))], sTek0.ch1[where((sTek0.ch1>lth)&(sTek0.ch1<hth))], lw=2)
print('Tek''s ch1 rise/fall time={},{}, shown with red. '.format(rt,ft))

show()
