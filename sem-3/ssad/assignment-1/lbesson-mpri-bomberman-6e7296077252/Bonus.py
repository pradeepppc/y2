#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This module implement a simple bonus system for Bomberman game.
Currently, it's quite limited, and not yet used by the game.

Warning
=======
.. warning::
   By now, the *bonus system* is **not yet** ready.
   
List of Bonuses:
================
 * no		-- nothing,
 * apple	-- a poisoned apple, decrease the life of the player (and *can* kill him),
 * dice		-- change randomly the life of the player,
 * fire		-- increase the *force* of player's bomb (*i.e.* the distance of explosion),
 * ice		-- increase the *timer* of player's bomb,
 * life[1|2|3]	-- increase (by *2, by +1 or by +2) the player's life,
 * sword	-- increase the *power* of player's bomb (they hit more !)

About:
======
 This bonus use the method Bonus.affect to change the game, so some modifications can be unable to do.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.4a'
__date__='jeudi 07 02 2013, at 23h:17m:30s'	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules #
import random
import Constants

#: For now, there is no bonus system used in the server or in the client,
#: so this constant represent the default bonus (*i.e.* no bonus).
#: Those constants are different bonus type.
#: From `here <http://en.wikipedia.org/wiki/Miscellaneous_Symbols>`_.
BONUS_NOBONUS='no'
BONUS_APPLE='☠apple'	#: a poisoned apple, decrease the life of the player (and *can* kill him),
BONUS_DICE='⚄dice'	#: change randomly the life of the player,
BONUS_FIRE='♨fire'	#: increase the *force* of player's bomb (*i.e.* the distance of explosion),⚡
BONUS_ICE='☃ice'	#: increase the *timer* of player's bomb,
BONUS_LIFE1='⛂life1'	#: increase (by *2) the player's life,
BONUS_LIFE2='☺life2'	#: increase (by +1) the player's life,
BONUS_LIFE3='⛀life3'	#: increase (by +2) the player's life,
BONUS_SWORD='⚔sword'	#: increase the *power* of player's bomb (they hit more !)

List_available_bonuses = [ BONUS_DICE, BONUS_SWORD ]	#: List of all availables bonuses.

#: The class
class Bonus:
	""" A Class to define a Bomberman bonus.

	Attributes:
	 * kind	-- reference of the bonus (by now, integer).
	
	This class can be used both by the client and the server,
	 but reasonably, have just to be used from Player and Board.
	"""

	def __init__(self, kind=BONUS_NOBONUS):
		""" Simple constructor of a bomb."""
		self.kind = kind	#:  reference of the bonus (by now, integer).

	def strNoUtf(self):
		""" Simple conversion to string, with no UTF caracters."""
		if self.kind == BONUS_NOBONUS: return " "
		return "BONUS"
#:		return self.kind[1].capitalize()

	__str__ = strNoUtf

	def strUtf(self):
		""" Simple conversion to string, with UTF caracters.."""
		if self.kind == BONUS_NOBONUS: return " "
		return self.kind[0]

	def __repr__(self):
		""" Toplevel representation of [self]."""
#:		return ("kind=%s" % self.kind)
		return self.kind
	
	def affect(self, player, board):
		""" affect(self, player, board) -> (player, board)
		When the *player* get this bonus, run this effect.
		*board* is the current state of the game (the Board.Board instance),
		*args* can be anything (see later)."""
		if self.kind == BONUS_APPLE:
			player.hurt()
		# Decrease the life of the player.
		elif self.kind == BONUS_DICE:
			player.pv = random.randint(1, 1 + Constants.pv_Init)
		# Set the life to random, between the init life +1 and 1.
		elif self.kind == BONUS_FIRE:
			player.templatebomb.force += 1
		# Increase the force of player's bombs.
		elif self.kind == BONUS_ICE:
			player.templatebomb.timer *= 2
		# Make the bomb of the player stay longer on the board.
		elif self.kind == BONUS_LIFE1:
			player.pv = player.pv * 2
		# Double the life of the player.
		elif self.kind == BONUS_LIFE2:
			player.pv += 1
		# Increase the life of the player.
		elif self.kind == BONUS_LIFE3:
			player.pv += 2
		# Increase the life of the player by 2.
		elif self.kind == BONUS_SWORD:
			player.templatebomb.power += 1
		else:	#: Don't do anything !
			pass	#: FIXME delete this.
		return (player, board)

#END
