# Setup virutal diffraction workspace using existing infrastructure
# within Mantid

import numpy as np

from mantid.simpleapi import CreateSimulationWorkspace
from mantid.simpleapi import SetUB
from mantid.simpleapi import PredictPeaks
from mantid.simpleapi import MoveInstrumentComponent
from mantid.geometry import CrystalStructure

# lattice constant for natrolite
# M. Ross, M. Flohr, and D. Ross,
# Crystalline Solution Seriesand Order-Disorderwithin the Natrolite Mineral Group
# American Mineralogist 77, 685 (1992).
a = 18.29  # A
b = 18.64  # A
c = 6.56  # A
alpha = 90  # deg
beta = 90  # deg
gamma = 90  # deg
lc_natrolite = {
    "a": a,
    "b": b,
    "c": c,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
}

# Generate simulated workspace for CORELLI
CreateSimulationWorkspace(
    Instrument='CORELLI',
    BinParams='1,100,10000',
    UnitX='TOF',
    OutputWorkspace='cws',
)

# Set the UB matrix for the sample
# u, v is the critical part, we can start with the
# ideal position
SetUB(
    Workspace="cws",
    u='1,0,0',  # vector along k_i, when goniometer is at 0
    v='0,1,0',  # in-plane vector normal to k_i, when goniometer is at 0
    **lc_natrolite,
)

# Creat crystal structure
