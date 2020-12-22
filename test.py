# Setup virutal diffraction workspace using existing infrastructure
# within Mantid

import numpy as np
from collections import namedtuple
from tqdm import tqdm

from mantid.simpleapi import mtd
from mantid.simpleapi import CombinePeaksWorkspaces
from mantid.simpleapi import CloneWorkspace
from mantid.simpleapi import CreateSimulationWorkspace
from mantid.simpleapi import CreatePeaksWorkspace
from mantid.simpleapi import LoadIsawDetCal
from mantid.simpleapi import SetGoniometer
from mantid.simpleapi import SetUB
from mantid.simpleapi import PredictPeaks
from mantid.simpleapi import MoveInstrumentComponent
from mantid.geometry import CrystalStructure

from mantid.simpleapi import SCDCalibratePanels


def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


# lattice constant for natrolite
# M. Ross, M. Flohr, and D. Ross,
# Crystalline Solution Seriesand Order-Disorderwithin the Natrolite Mineral Group
# American Mineralogist 77, 685 (1992).
lc_natrolite = {
    "a": 18.29,  # A
    "b": 18.64,  # A
    "c": 6.56,  # A
    "alpha": 90,  # deg
    "beta": 90,  # deg
    "gamma": 90,  # deg
}
natrolite = convert(lc_natrolite)
# we don't have a clear way to setup crystal for natrolite
# TODO:
# cs_natrolite = CrystalStructure(
#     f'{natrolite.a} {natrolite.b} {natrolite.c}',
#     'f d d 2',
#     '',  # what should we do with this one
# )

# lattice constant for Si
# data from Mantid web documentation
lc_silicon = {
    "a": 5.431,  # A 
    "b": 5.431,  # A 
    "c": 5.431,  # A
    "alpha": 90,  # deg
    "beta": 90,  # deg
    "gamma": 90,  # deg
}
silicon = convert(lc_silicon)
cs_silicon = CrystalStructure(
    f"{silicon.a} {silicon.b} {silicon.c}",
    "F d -3 m",
    "Si 0 0 0 1.0 0.05",
)

# Generate simulated workspace for CORELLI
CreateSimulationWorkspace(
    Instrument='CORELLI',
    BinParams='1,100,10000',
    UnitX='TOF',
    OutputWorkspace='cws',
)
cws = mtd['cws']

# Set the UB matrix for the sample
# u, v is the critical part, we can start with the
# ideal position
SetUB(
    Workspace="cws",
    u='1,0,0',  # vector along k_i, when goniometer is at 0
    v='0,1,0',  # in-plane vector normal to k_i, when goniometer is at 0
    **lc_silicon,
)

# set the crystal structure for virtual workspace
cws.sample().setCrystalStructure(cs_silicon)

# Generate predicted peak workspace
dspacings = convert({'min': 1.0, 'max': 10.0})
wavelengths = convert({'min': 0.8, 'max': 2.9})

# Collect peaks over a range of omegas
CreatePeaksWorkspace(OutputWorkspace='pws')
omegas = range(0, 180, 3)

for omega in tqdm(omegas):
    SetGoniometer(
        Workspace="cws",
        Axis0=f"{omega},0,1,0,1",
    )

    PredictPeaks(
        InputWorkspace='cws',
        WavelengthMin=wavelengths.min,
        wavelengthMax=wavelengths.max,
        MinDSpacing=dspacings.min,
        MaxDSpacing=dspacings.max,
        ReflectionCondition='All-face centred',
        OutputWorkspace='_pws',
    )

    CombinePeaksWorkspaces(
        LHSWorkspace="_pws",
        RHSWorkspace="pws",
        OutputWorkspace="pws",
    )

pws = mtd['pws']

# Test_1: null test
# no movement of any detector
SCDCalibratePanels(
    PeakWorkspace="pws",
    a=silicon.a,
    b=silicon.b,
    c=silicon.c,
    alpha=silicon.alpha,
    beta=silicon.beta,
    gamma=silicon.gamma,
    changeL1=True,
    changeT0=False,
    CalibrateBanks=True,
    DetCalFilename='null_case.DetCal',
)

CloneWorkspace(
    InputWorkspace='cws',
    OutputWorkspace='cws_nullcase',
)
LoadIsawDetCal(
    InputWorkspace='cws_nullcase',
    Filename='null_case.DetCal',
)
