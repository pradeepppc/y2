#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Store the file in ~/.pystartup, and set an environment variable to point
# to it:  "export PYTHONSTARTUP=~/.pystartup" in bash.

"""
Add auto-completion and a stored history file of commands to your Python
 interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
 bound to the Esc key by default (you can change it - see readline docs).

This module simple launch readline wrapper to help taping texts to python programs.
 Basically, it's less efficient than `PyRlwrap <PyRlwrap.html>`_, but quite simplier.

Warning:
========
.. warning::
   The readline history file is set locally (./.python.history.py).
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.2'
__date__='jeudi 07 02 2013, at 23h:17m:30s'	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules 
import atexit
import os
try:
	import readline
except ImportError:
	print("Module readline not available.")
else:
	import rlcompleter
	readline.parse_and_bind("tab: complete")
import rlcompleter

#: Set path of the history file. (Currently, it's **./.python.history.py**)
historyPath = os.path.expanduser(".python.history.py")

def save_history(historyPath=historyPath):
	''' The special function which will be called at exit,
	 to save the readline buffer to the history file.
	'''
	import readline
	readline.write_history_file(historyPath)

if os.path.exists(historyPath):
	readline.read_history_file(historyPath)

atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath
# Clean toplevels values
