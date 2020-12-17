iptsfolder= "/SNS/CORELLI/IPTS-23019/"
nxdir=iptsfolder + "nexus/"
ccdir = iptsfolder + "shared/autoreduce/"
scriptdir = iptsfolder+"shared/scripts/"
UBfile=scriptdir+'KCP_2nd_230K.mat'

from mantid.simpleapi import *
from mantid.api import *

BinParm='0.3,-0.005,5'
temp = '300K'
outputdir = iptsfolder+"shared/"+temp+"/"

#if not mtd.doesExist('maskfile'):
    #maskfile = LoadMask(Instrument='CORELLI',
                    #InputFile=scriptdir+'CCR.xml')

#if not mtd.doesExist('calibration'):
#    calibration = LoadNexus('/SNS/users/rwp/corelli/cal_2018_05/0a/TubeCalib+DetCal.nxs')

#maskfile = mtd['maskfile']
#calibration = mtd ['calibration']

# T = 300 K
start = 133752
stop = 133871

runs = range(start, stop+1,3)

toMerge1=[]
toMerge2=[]

#if mtd.doesExist('data'):
#    DeleteWorkspace('data')

LoadCC = False
# maskfile = mtd['maskfile']
# calibration = mtd['calibration']

for r in runs:
    print('Processing run : %s' %r)
    ows='COR_'+str(r)
    omd=ows+'_md'
    toMerge1.append(ows)
    toMerge2.append(omd)

    if not mtd.doesExist(ows):
        if LoadCC :
            filename=ccdir+'CORELLI_'+str(r)+'_elastic.nxs'
            if not mtd.doesExist(ows):
                LoadNexus(Filename=filename, OutputWorkspace=ows)
                #CopyInstrumentParameters(calibration, OutputWorkspace=ows)
                #MaskDetectors(Workspace=ows,MaskedWorkspace=maskfile)
        else:
            filename=nxdir+'CORELLI_'+str(r)+'.nxs.h5'
            if not mtd.doesExist(ows):
                LoadEventNexus(Filename=filename, OutputWorkspace=ows,FilterByTimeStop=120)
                #CopyInstrumentParameters(calibration, OutputWorkspace=ows)
                #MaskDetectors(Workspace=ows,MaskedWorkspace=maskfile)

    #get total proton_charge from run log
    owshandle=mtd[ows]
    lrun=owshandle.getRun()
    pclog=lrun.getLogData('proton_charge')
    pc=sum(pclog.value)/1e12
    #owshandle /= pc
    print('the current proton charge :'+ str(pc))

    #ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
    #Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
    SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
    #LoadIsawUB(InputWorkspace=ows,Filename=UBfile)
    #if not mtd.doesExist(omd):
    #ConvertToMD(InputWorkspace=ows,
       #OutputWorkspace=omd,
       #QDimensions='Q3D',
       #dEAnalysisMode='Elastic',
       #Q3DFrames='HKL',
       #Uproj='1,0,0',
       #Vproj='0,0,1',
       #Wproj='0,1,0',
       #QConversionScales='HKL',
       #LorentzCorrection='1',
       #MinValues='-15.1,-15.1,-15.1',
       #MaxValues='15.1,15.1,15.1')
data=GroupWorkspaces(toMerge1)
#md=GroupWorkspaces(toMerge2)
#mergedMD2=MergeMD(toMerge2)

#generate sample space
data=mtd['data']
mdqsampparts=ConvertToMD(data,QDimensions="Q3D",
                      dEAnalysisMode="Elastic",
                      Q3DFrames="Q_sample",
                      LorentzCorrection=1,
                      MinValues="-15,-15,-15",
                      MaxValues="15,15,15",
                      Uproj='1,0,0',
                      Vproj='0,1,0',
                      Wproj='0,0,1')
mdqsamp=MergeMD(mdqsampparts)

#LoadIsawUB(InputWorkspace='data',Filename=scriptdir+"KCP_300K.mat")
#ConvertToMD(InputWorkspace='data',
#                  OutputWorkspace='md',
#                  QDimensions='Q3D',
#                  dEAnalysisMode='Elastic',
#                  Q3DFrames='HKL',
#                  Uproj='1,1,0',
#                  Vproj='1,-1,0',
#                  Wproj='0,0,1',
#                  QConversionScales='HKL',
#                  LorentzCorrection='1',
#                  MinValues='-15.1,-15.1,-15.1',
#                  MaxValues='15.1,15.1,15.1')
#mergedMD_HHL=MergeMD('md')

#mtd.clear()
