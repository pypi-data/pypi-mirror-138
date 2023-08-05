"""
This is a python package for plotting and data processing in stellarator optimization.

It contains several python functions on HDF5, Fourier surfaces, FOCUS, cois, 
magnetic dipoles, STELLOPT, VMEC, BOOZ_XFORM, etc.

The repository is available at https://github.com/zhucaoxiang/CoilPy.

For full documenation, please check https://zhucaoxiang.github.io/CoilPy/api/coilpy.html.
"""
__version__ = "0.3.24"

# local packages
from .misc import colorbar, get_figure, kwargs2dict, map_matrix
from .misc import print_progress, toroidal_period, vmecMN, xy2rp
from .misc import trigfft, fft_deriv, trig2real, vmec2focus
from .misc import real2trig_2d, booz2focus, read_focus_boundary, div0
from .misc import biot_savart, rotation_matrix, rotation_angle
from .misc import set_axes_equal
from .hdf5 import HDF5
from .surface import FourSurf
from .dipole import Dipole
from .focushdf5 import FOCUSHDF5
from .coils import Coil, SingleCoil
from .stellopt import STELLout
from .vmec import VMECout
from .booz_xform import BOOZ_XFORM
from .mgrid import Mgrid
from .pm4stell import blocks2vtk, blocks2ficus
from .magnet import Magnet, corner2magnet
from .magtense_interface import get_center, build_prism, blocks2tiles
from .magtense_interface import corner2tiles, magtense2vtk

# from coilpy_fortran import hanson_hirshman, biot_savart
