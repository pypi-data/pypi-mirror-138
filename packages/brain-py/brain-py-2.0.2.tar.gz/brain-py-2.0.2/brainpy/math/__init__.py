# -*- coding: utf-8 -*-


"""
The ``math`` module for whole BrainPy ecosystem.
This module provides basic mathematical operations, including:

- numpy-like array operations
- linear algebra functions
- random sampling functions
- discrete fourier transform functions
- compilations of ``jit``, ``vmap``, ``pmap`` for class objects
- automatic differentiation of ``grad``, ``jacocian``, ``hessian``, etc. for class objects
- loss functions
- activation functions
- optimization classes

Details in the following.
"""


# necessity to wrap the jax.numpy.ndarray:
# 1. for parameters and variables which want to
#    modify in the JIT mode, this wrapper is necessary.
#    Because, directly change the value in the "self.xx"
#    cannot work.
# 2. In JAX, ndarray is immutable. This wrapper make
#    the index update is the same way with the numpy
#


# data structure
from .jaxarray import *

# functions/operations
from .numpy_ops import *
from .operators import *
from .activations import *
from . import fft
from . import linalg
from . import random
from . import losses
from . import optimizers
from . import activations

# transformations
from .autograd import *
from .controls import *
from .jit import *
from .parallels import *

# others
from . import profile
from . import setting
from .profile import *
from .setting import *
from .function import *
from . import numpy
