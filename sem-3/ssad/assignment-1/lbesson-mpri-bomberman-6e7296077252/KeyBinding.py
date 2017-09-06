#!/usr/bin/env python -i
# -*- encoding: utf-8 -*-

"""
This module implement a simple way to store and represent key binding for Bomberman game.
The class KeyBinding can be used by any other modules.

Currently, the representation of keyboard caracter is the one used by PyGame (SDL python binding).

For example :
=============
 * K_a to K_z represent the letter *a* to *z*,
 * K_TAB, K_SPACE, K_SLASH etc,
 * a complete list is stored in the variable LIST_of_authorized_keys.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.0b'
__date__='ven. 15/02/2013 at 02h:10m:51s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

import sys
try:
	#2#################
	# Project Modules #
	import ANSIColors
	#####################
	# Pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write(ANSIColors.sprint("\t<warning> <ERROR> <red>Fail<white> to launch module %s." % (err)))
	sys.exit(2)

#: The list of all valid keys.
#: Can be simply created with :
#:  >>> a = []
#:  >>> for i in dir(pygame):
#:  >>>  if i[2:] == 'K_': a.append(i)
#:  >>> return a
LIST_of_authorized_keys = ['K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_AMPERSAND', 'K_ASTERISK', 'K_AT', 'K_BACKQUOTE', 'K_BACKSLASH', 'K_BACKSPACE', 'K_BREAK', 'K_CAPSLOCK', 'K_CARET', 'K_CLEAR', 'K_COLON', 'K_COMMA', 'K_DELETE', 'K_DOLLAR', 'K_DOWN', 'K_END', 'K_EQUALS', 'K_ESCAPE', 'K_EURO', 'K_EXCLAIM', 'K_F1', 'K_F10', 'K_F11', 'K_F12', 'K_F13', 'K_F14', 'K_F15', 'K_F2', 'K_F3', 'K_F4', 'K_F5', 'K_F6', 'K_F7', 'K_F8', 'K_F9', 'K_FIRST', 'K_GREATER', 'K_HASH', 'K_HELP', 'K_HOME', 'K_INSERT', 'K_KP0', 'K_KP1', 'K_KP2', 'K_KP3', 'K_KP4', 'K_KP5', 'K_KP6', 'K_KP7', 'K_KP8', 'K_KP9', 'K_KP_DIVIDE', 'K_KP_ENTER', 'K_KP_EQUALS', 'K_KP_MINUS', 'K_KP_MULTIPLY', 'K_KP_PERIOD', 'K_KP_PLUS', 'K_LALT', 'K_LAST', 'K_LCTRL', 'K_LEFT', 'K_LEFTBRACKET', 'K_LEFTPAREN', 'K_LESS', 'K_LMETA', 'K_LSHIFT', 'K_LSUPER', 'K_MENU', 'K_MINUS', 'K_MODE', 'K_NUMLOCK', 'K_PAGEDOWN', 'K_PAGEUP', 'K_PAUSE', 'K_PERIOD', 'K_PLUS', 'K_POWER', 'K_PRINT', 'K_QUESTION', 'K_QUOTE', 'K_QUOTEDBL', 'K_RALT', 'K_RCTRL', 'K_RETURN', 'K_RIGHT', 'K_RIGHTBRACKET', 'K_RIGHTPAREN', 'K_RMETA', 'K_RSHIFT', 'K_RSUPER', 'K_SCROLLOCK', 'K_SEMICOLON', 'K_SLASH', 'K_SPACE', 'K_SYSREQ', 'K_TAB', 'K_UNDERSCORE', 'K_UNKNOWN', 'K_UP', 'K_a', 'K_b', 'K_c', 'K_d', 'K_e', 'K_f', 'K_g', 'K_h', 'K_i', 'K_j', 'K_k', 'K_l', 'K_m', 'K_n', 'K_o', 'K_p', 'K_q', 'K_r', 'K_s', 'K_t', 'K_u', 'K_v', 'K_w', 'K_x', 'K_y', 'K_z']

#: A dict of values associated to valid keys.
#: Can be simply created with ::
#:	DICT_of_authorized_keys = {}
#:	tmp = 0
#:	for k in LIST_of_authorized_keys:
#:	 exec("tmp=%s" % k)
#:	 DICT_of_authorized_keys[k] = tmp
DICT_of_authorized_keys = {}
tmp = 0
for k in LIST_of_authorized_keys:
 exec("tmp=%s" % k)	# WARNING XXX FIXME
 DICT_of_authorized_keys[k] = tmp

def print_keynum_as_str(keynum):
	""" Trying to print the *keynum* as a key name.
	The list of valid pygame keynames are in *LIST_of_authorized_keys*."""
	for s in LIST_of_authorized_keys:
	 if keynum == eval(s):
	  return s
	raise ValueError("%i is not a valid key number." % keynum)

######################################
#### The main class of KeyBinding ####

class KeyBinding(object):
	""" A Class to store and represent key binding for Bomberman game.
Keys are represented as a list of a pygame representation of a keyboard touch

Attributes:
 * up	-- the keys to go up / north.
 * down	-- the keys to go down / south.
 * left	-- the keys to go left / east.
 * right	-- the keys to go right / west.
 * bomb	-- the keys to drop bombs. 
 * help	-- the keys to print help. 

This class can be used both by the client and the server.

Example:
 >>> kbl=KeyBinding()
 >>> kbl.help=['K_DELETE'] # Override the default value.
 >>> kbl.bomb.append('K_DOLLAR') # Add a new key to drop bombs !
 >>> # To print a simple explanation about the keys :
 >>> print kbl.help()
 >>> # To redefine the keys, one by one :
 >>> kbl.ask()
	"""

	def __init__(self, up=['K_UP'], down=['K_DOWN'], left=['K_LEFT'], right=['K_RIGHT'], bomb=['K_SPACE'], help=['K_h']):
		""" Simple constructor of a key binding."""
		self.up=up	#: the keys to go up / north.
		self.down=down	#: the keys to go down / south.
		self.left=left	#: the keys to go left / east.
		self.right=right	#: the keys to go right / west.
		self.bomb=bomb	#: the keys to drop bombs. 
		self.help=help	#: the keys to print help.
		# For values.
		self.value_up=[]	#: the values of keys to go up / north.
		self.value_down=[]	#: the values of keys to go down / south.
		self.value_left=[]	#: the values of keys to go left / east.
		self.value_right=[]	#: the values of keys to go right / west.
		self.value_bomb=[]	#: the values of keys to drop bombs. 
		self.value_help=[]	#: the values of keys to print help.
		self.values()	#: make values for those keys.

	def __str__(self):
		 """__str__(self) -> str
		 A pretty string for the key bindings.
		 """
		 return "North/Up:'%s'; South/Down:'%s'; East/Left:'%s'; West/Right:'%s'; Bomb:'%s'; Help:'%s'." % (self.up, self.down, self.left, self.right, self.bomb, self.help)

	__repr__=__str__

	def get_help(self):
		""" Just return a string explaining the key binding list."""
		res="\t/?/ The following keys are used : "
		res+="North/Up:'%s'; South/Down:'%s'; East/Left:'%s'; West/Right:'%s'; Bomb:'%s'." % (self.up, self.down, self.left, self.right, self.bomb)
		res+=" To get this help message : '%s'." % self.help
		return res
	
	def ask(self):
		""" A way to ask interactivly, in text mod in console, to redefine the key binding list."""
		print "Interactivily : redefine key binding list in text mod ..."
		list_inp=[]
		for m in ['up', 'down', 'left', 'right', 'bomb', 'help']:
		 print "Old value for attribute %s : %s" % (m, self.__dict__[m])
		 zut = True
		 self.__dict__[m] = [] #: Reset the dict.
		 while(zut):
		 	zut=False 
			inp=raw_input("New value for attribute %s ? (Remember: Just a pygame representation of a keyboard touch, like 'K_a' or 'K_ESCAPE'.)" % m)
			if (not inp in LIST_of_authorized_keys) or (inp in list_inp):
				zut=True
				print "Wrong %s: try again !" % inp
		 self.__dict__[m].append(inp)
		 list_inp.append(inp)
		print "New key mapping :\n %s" % self

	def ok(self, inp, action='up'):
		""" A shortcut to : inp in key.action.
		Allow to check if the key [inp] is valid for the move [action].
		
		action is one of : up, down, left, right, bomb, help."""
		if action=='up': return (inp in self.up)
		if action=='down': return (inp in self.down)
		if action=='left': return (inp in self.left)
		if action=='right': return (inp in self.right)
		if action=='bomb': return (inp in self.bomb)
		if action=='help': return (inp in self.help)
		return False

	def values(self):
		""" Make 6 attributes value_up,..,value_help."""
		for a in ['up', 'down', 'left', 'right', 'bomb', 'help']:
		 l = self.__getattribute__(a)
		 for k in l:
		  self.__getattribute__('value_'+a).append(DICT_of_authorized_keys[k])

	def event_key_is_ok(self, key, action='up'):
		""" To check if the Pygame event key is valid for the move [action].
		
		action is one of : up, down, left, right, bomb, help."""
		if action=='up': return (key in self.value_up)
		if action=='down': return (key in self.value_down)
		if action=='left': return (key in self.value_left)
		if action=='right': return (key in self.value_right)
		if action=='bomb': return (key in self.value_bomb)
		if action=='help': return (key in self.value_help)
		return False

#################################
#### Two basic keys bindings ####

def classic():
	""" Return a simple key binding, like the one used in WoW or Skyrim (classic with direction with Z up, Q left, S down, D right)."""
	return KeyBinding(up=['K_z'], down=['K_s'], left=['K_q'], right=['K_d'], bomb=['K_x'], help=['K_h'])

def arrows():
	""" Return a simple key binding, like the one used in Lionheart or Mario."""
	return KeyBinding(up=['K_UP'], down=['K_DOWN'], left=['K_LEFT'], right=['K_RIGHT'], bomb=['K_SPACE'], help=['K_DELETE', 'K_h'])

# END
