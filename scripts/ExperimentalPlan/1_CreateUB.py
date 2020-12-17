'''
   Disclaimer: This code is written for the users' convenience and is provided to users by the CORELLI Team at SNS. We have tried our best to make sure the code qualtiy. If you have found any bugs, please let us know. You can contact me for any comments and suggestions: Yaohua Liu, liuyh@ornl.gov,  
         
   CreateUB.py    

    It generates a virtual UB from lattice parameters and named sample orientation. 
   
   Input:

   1. Accurate lattice parameter.
   2. A vector defining the incoming beam direction.
   3. A second vector one in the horizontal plane and perpendicular to the first vector.

   Output:
   1. A UB file will be saved in the output folder. 
   
   V.01 Feb. 27, 2017 @ Yaohua Liu. liuyh@ornl.gov
   V.02 May 8 2017 @YNL.   Add extra help information.   

   For more information, please contact one of the beamline staff. 
'''
 
import sys,os
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger
import numpy as np
np.seterr("ignore")


# Provide necessary information
#iptsfolder= "/SNS/CORELLI/IPTS-16633/"
#outputdir=iptsfolder+"shared/CMO_LSAO/"
#outputdir = '/SNS/CORELLI/shared/PythonScripts/ExpPlan/'
UBfile ="/SNS/CORELLI/shared/NXS/2019/ExperimentalPlan/testub.mat"

# create a workspace (or you can load one)
ws=CreateSingleValuedWorkspace(5)

#set a UB matrix using the vector along k_i as 1,1,0, and the 0,0,1 vector in the horizontal plane, and the rotation axis is 1, -1, 0
# u is the vector along K_i when goniometer is at 0; and v is in-plane vector perpendicular to k_i, when goniometer is at 0
SetUB(ws,a=5.978,b=5.978,c=17.17,alpha=90, beta=90, gamma=120, u="1,1,0", v="0,0,1")
UB = ws.sample().getOrientedLattice().getUB()
SaveIsawUB(InputWorkspace=ws, Filename=UBfile)


