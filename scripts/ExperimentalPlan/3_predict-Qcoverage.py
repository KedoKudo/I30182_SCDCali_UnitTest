'''
   Disclaimer: This code is written for the users' convenience and is provided to users by the CORELLI Team at SNS. We have tried our best to improve the code qualtiy. If you have found any bugs, please let us know. You can contact me for any comments and suggestions: Yaohua Liu, ynl@ornl.gov,  
         
   predcit_Qcoverage.py    V.03

   It performs a virtual experiment to check the detector coverage for a range of sample angles. One can use it to plan the experimental angles needed for a perfered Q coverage. 
   It can also combined with PredictPeaks and PredictFractionalPeaks to predict the location of a feature (such as a weak peak from a thin film sample.) on the detector. 

   One can use a virtual UB to predict the Q coverage without collecting any data. In this case, one needs the accurate structural information of the sample. 
 
Here is an example for a tetragonal system. Here the rotation axis is along the [1 0 0] direction. Note that the UB.mat file is very strict on the format. please copy and edit one previously generated from the 'SaveIsawUB' command. One can also use CreatUB.py (should be saved in the folder) to generate a UB file as needed.  

 0.00000000  0.23100000  0.00000000 
 0.00000000  0.00000000  0.23100000 
 0.10384900  0.00000000  0.00000000 
     4.3266      4.3266      9.6279     90.0000     90.0000     90.0000    180.2292 
     0.0000      0.0000      0.0000      0.0000      0.0000      0.0000      0.0000 

   Input:

   1. An accurate UB file (or a fake UB).
   2. A range of Omega angles.
   3. A detector maskfile. This is very important when using a magnet, e.g. SlimSam, where the SE will dramatically change the useful detector coverage. 

   Output:
   1. If the code is run from terminal, a nexus file will be saved in the shared folder. The file shows the Q space that will be covered, and the intensity reflects the relative flux. 


   V.01 Nov 17, 2016 @  Yaohua Liu. ynl@ornl.gov 
   V.02 Feb 29, 2017 @  YHL
            Add the opition of using a detector mask, update the script name.
   V.03 Apr 07, 2017 @  YHL
            Add an example of a virtual ub. A little tweak on the code to group the data to make it easy to use "PredictPeaks"
   V.04  Aug. 22, 2017@ YHL
            An external IDF file becomes an option rahter than required.  
	    	
	
   For more information, please contact one of the beamline staff. 
'''
 
import sys,os
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger
import numpy as np
np.seterr("ignore")


# Provide necessary information on the data here.
outputdir = '/SNS/CORELLI/IPTS-19055/shared/'
UBfile = "/SNS/CORELLI/shared/NXS/2019/ExperimentalPlan/testub.mat"
outputfile = outputdir + 'Predicted_QSpace.nxs'

# define the angles for virtual runs
Omegas = range(0, 30, 4)
totalrun = len(Omegas)
print "Total number of runs %d" %totalrun

#define the projected orientation in the HKL space
proj=['1,1,0', '1,-1,0', '0,0,1']

#define IDF file. Ask instrument scientists for the updated information
IDFfile = ''    # using default
#IDFfile = '/SNS/CORELLI/shared/Calibration/CORELLI_Definition_910.xml'  # newly calibrated. April, 2017 

#toggle the function to PredictPeaks. If turns on, need to update the Dmin and Dmax. This part is slow if dmin is smaller than 1. 
predictpeaks = 1 # 1 to turn on Predictpeaks. 
dRange = [1.5, 10.0]

# One Vandanium Run is used to load the flux and detector information. No need to change.  
filename='/SNS/CORELLI/shared/PythonScripts/ExpPlan/Vdata/COR_31663.nxs.h5'
Vdata = LoadEventNexus(Filename=filename, FilterByTimeStop=120)

#define the SE
SE = ""   # "CCR", "OC", "SlimSam"   
if SE in ["", "CCR"] :
    mask = LoadMask(Instrument='CORELLI', InputFile='/SNS/CORELLI/shared/PythonScripts/MaskFiles/CCR/maskfile_03262017.xml')
elif SE == "OC" :
    mask = LoadMask(Instrument='CORELLI', InputFile='/SNS/CORELLI/shared/PythonScripts/MaskFile_20170221.xml')
elif SE == "SlimSam" :
    mask = LoadMask(Instrument='CORELLI', InputFile='/SNS/CORELLI/shared/PythonScripts/MaskFiles/SlimSam/SlimSam.xml')
MaskDetectors(Workspace=Vdata,MaskedWorkspace=mask)


# Load the data and convert to Q space for mesh plot and peak finding. 
toMerge1=[]

for index, Omega in enumerate(Omegas):
    print "Run %d of %d, Processing converting MD for run : %s" %(index+1, totalrun, Omega)
    ows='COR_'+str(Omega)+'deg'
    toMerge1.append(ows)
    print 'Omega = %5.2f deg.' %(Omega)
    
    CloneWorkspace(InputWorkspace= Vdata, OutputWorkspace=ows)
    if len(IDFfile) > 0:
        LoadInstrument(Workspace= ows, Filename=IDFfile,RewriteSpectraMap=False)
    SetGoniometer(ows,Axis0=str(Omega)+',0,1,0,1') 
    

data = GroupWorkspaces(toMerge1)
LoadIsawUB(InputWorkspace=data,Filename=UBfile)
ConvertToMD(InputWorkspace=data,OutputWorkspace='md',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',Uproj= proj[0],Vproj=proj[1],Wproj=proj[2], 
    QConversionScales='HKL',LorentzCorrection='0', MinValues='-12.1,-12.1,-30.1',MaxValues='12.1,12.1,30.1')
mdmesh=MergeMD('md')

if predictpeaks == 1:
	PredictPeaks(InputWorkspace=data, WavelengthMin=0.8, WavelengthMax=2.9, MinDSpacing=dRange[0], MaxDSpacing=dRange[1], OutputWorkspace='peaks')

#SaveMD('mdmesh',Filename=outputfile)

