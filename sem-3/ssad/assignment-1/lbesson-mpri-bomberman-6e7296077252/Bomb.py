#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This module implement a simple bomb system for Bomberman game.

There is two classes for Bombs :
 * BombNoOwner	-- one without any information about the player which own it,
 * Bomb		-- an other with an additionnal attribute *owner*.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.2d'
__date__='mer. 13/02/2013 at 04h:00m:20s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import *

class BombNoOwner:
	""" A Class to define a Bomberman bomb.
	This bomb have no information about his owner, because it's aimed to be store in the Player.Player class.

	Attributes:
	 * force	-- the dimension of explosion.
	 * timer	-- the timer of the bomb.
	 * power	-- the power of the bomb (number of inguries infliged by the bomb).
	
	This class can be used both by the client and the server.
	"""
	
	def __init__(self, force=force_default, timer=timer_default, power=power_default, verb=False):
	 """ Simple constructor of a bomb."""
	 if verb:
	 	ANSIColors.printc("\t/B/ <blue>One new <neg>anonym<Neg> bomb<white> : with force=%i, timer=%i, power=%i." % (force, timer, power))
	 self.force = force	#: the dimension of explosion.
	 self.timer = timer	#: the timer of the bomb.
	 self.power = power	#: The power of the bomb
	
	def __repr__(self):
	 """ Toplevel representation of [self]."""
	 return ("force=%i; timer=%i; power=%i" % (self.force, self.timer, self.power))
	
	def __str__(self):
	 return self.__repr__()
	
	def tic(self, toc=toc_default):
	 """ Just decrease the timer of the bomb, [toc] is the time spent during ticking.
	 self.timer<=0 is returned.
	 Allow the following shortcut :
	 
	 Example:
	  >>> if board[i,j].bomb.tic:
	  >>>  print 'My bomb at place (%i,%i) is exploding !!' % (i,j)
	  >>>  game.make_explosion(board[i,j].bomb) # a toy example.
	  >>> else:
	  >>>  print 'Hourra, the bomb at place (%i,%i) is not exploding !!' % (i,j) """
	 self.timer -= toc
	 return self.timer<=0

###################################
#### Add the owner of the bomb ####

class Bomb(BombNoOwner):
	""" A Class to define a Bomberman bomb.
	It is just a BombNoOwner with an extra *owner* attribute.

	Attributes:
	 * owner	-- the indicator of the player which droped the bomb.
	 * force	-- the dimension of explosion.
	 * timer	-- the timer of the bomb.
	 * power	-- the power of the bomb (number of inguries infliged by the bomb).
	
	This class can be used both by the client and the server.
	"""
	
	def __init__(self, owner, force=force_default, timer=timer_default, power=power_default, verb=True):
	 """ Simple constructor of a bomb.
	 The [owner] have to be given, the others paramaters can be omitted.
	 [owner] is used to be a Player.Player instance, but formally coulb be anything."""
	 if verb:
	 	ANSIColors.printc("\t/B/ <blue>One new bomb<white> : dropped by %s, with force=%i, timer=%i, power=%i." % (owner, force, timer, power))
	 self.owner = owner	#: the indicator of the player which droped the bomb.
	 self.force = force	#: the dimension of explosion.
	 self.timer = timer	#: the timer of the bomb.
	 self.power = power	#: The power of the bomb
	
	def __str__(self):
	 """ Simple conversion to string."""
	 return ("O:%s;T:%i" % (self.owner, self.timer))

def add_owner(bomb, owner):
	"""add_owner(bomb, owner) -> Bomb.Bomb instance
	Transform a Bomb.BombNoOwner instance to a Bomb.Bomb instance,
	 by adding to it the *owner*.
	"""
	return  Bomb(owner, force=bomb.force, timer=bomb.timer, power=bomb.power)

#END
