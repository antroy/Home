""" The orb package is a collection of modules for automating web-testing using Python scripts.

The package has 3 key classes, Web, Action and Chain. Web objects are responsible for storing information on the testing environment, such as base urls, default parameter dictionary etc. Action objects are responsible for storing the details of an actual http call, for example request parameters, url etc. Actions can also store a number of functions which can be used to parse the output of the response from the server.
"""     

from orb import *

__all__ = ('Web', 'Chain', 'Action', 'DataManager', 'BatchRunner')

