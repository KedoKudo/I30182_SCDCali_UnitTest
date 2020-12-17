'''
   Disclaimer: This code is written for the users' convenience and is provided to users by the CORELLI Team at SNS. We have tried our best to make sure the code qualtiy. If you have found any bugs, please let us know. You can contact me for any comments and suggestions: Yaohua Liu, liuyh@ornl.gov,

   CreateMask.py


   Input:

   1. BTP numbers for detector masking: Bank, Tube, Pixel.

   Output:
   1.A mask file will be saved in the shared folder.

   V.01 Feb. 27, 2017 @ Yaohua Liu. liuyh@ornl.gov

   For more information, please contact one of the beamline staff.
'''

import sys,os
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger
import numpy as np
np.seterr("ignore")

#outputdir = '/SNS/CORELLI/shared/Vanadium/2018B_SlimSAM/'
outputdir = '/SNS/CORELLI/IPTS-22353/shared/scripts/'
MaskFile = outputdir + "SlimSam.xml"

COR = LoadEmptyInstrument(InstrumentName='CORELLI')
# For SlimSam
MaskBTP(Workspace=COR,Bank="1-30,62-91")     #  out-of-range modules in the A and C rows
MaskBTP(Workspace=COR,Pixel="1-10,200-256")    #  detector edges
# -- DB
MaskBTP(Workspace=COR,Bank="58",Tube="11-16")   #DB
MaskBTP(Workspace=COR,Bank="59",Tube="1-5")       #DB

SaveMask(COR, outputFile = MaskFile)
