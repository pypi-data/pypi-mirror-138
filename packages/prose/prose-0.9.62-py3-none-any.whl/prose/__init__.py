import warnings
from astropy.wcs import FITSFixedWarning

warnings.simplefilter("ignore", FITSFixedWarning)

from . import config

CONFIG = config.ConfigManager()


from . import visualization as viz

from .io.fitsmanager import FitsManager
from .fluxes import ApertureFluxes
from .telescope import Telescope
from prose.core import Block, Sequence, Image
from .observation import Observation


def load(photfile):
    return Observation(photfile)
