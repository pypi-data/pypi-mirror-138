'''
A python interface for accessing NetsBlox services
'''

from .editor import * # we import editor into global scope
from . import dev     # users can access dev explicitly if they want
from . import turtle  # our wraper around raw turtles
from . import snap

from .common import get_location

__version__ = '0.5.5'
__author__ = 'Devin Jean'
__credits__ = 'Institute for Software Integrated Systems, Vanderbilt University'
