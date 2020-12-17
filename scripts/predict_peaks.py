import sys,os
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger
import numpy as np
np.seterr("ignore")


# Provide necessary information on the data here.
outputdir = '/SNS/CORELLI/IPTS-23019/shared/'
UBfile = "/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_300K.mat"
outputfile = '/SNS/CORELLI/IPTS-23019/shared/Natrolite/Predicted.peaks'

# define the angles for virtual runs
Omegas = range(0, 180, 3)
totalrun = len(Omegas)
print("Total number of runs {:d}".format(totalrun))

dRange = [1.0, 10.0]

# One Vandanium Run is used to load the flux and detector information. No need to change.
filename='/SNS/CORELLI/shared/PythonScripts/ExpPlan/Vdata/COR_31663.nxs.h5'
Vdata = LoadEventNexus(Filename=filename, FilterByTimeStop=120)

mask = LoadMask(Instrument='CORELLI', InputFile='/SNS/CORELLI/shared/PythonScripts/MaskFiles/CCR/maskfile_03262017.xml')
MaskDetectors(Workspace=Vdata,MaskedWorkspace=mask)

combinedPeaks = CreatePeaksWorkspace()
for index, Omega in enumerate(Omegas):
    ows='COR_'+str(Omega)+'deg'
    CloneWorkspace(InputWorkspace=Vdata, OutputWorkspace=ows)
    SetGoniometer(ows,Axis0=str(Omega)+',0,1,0,1')
    LoadIsawUB(InputWorkspace=ows, Filename=UBfile)
    PredictPeaks(InputWorkspace=ows,
                 WavelengthMin=0.8,
                 WavelengthMax=2.9,
                 MinDSpacing=dRange[0],
                 MaxDSpacing=dRange[1],
                 ReflectionCondition='All-face centred',
                 OutputWorkspace='peaks')
    CombinePeaksWorkspaces(LHSWorkspace='peaks',
                           RHSWorkspace='combinedPeaks',
                           OutputWorkspace='combinedPeaks')

SaveIsawPeaks(InputWorkspace='combinedPeaks', Filename=outputfile)
