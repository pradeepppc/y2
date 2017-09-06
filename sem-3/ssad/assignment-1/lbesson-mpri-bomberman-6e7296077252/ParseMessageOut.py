#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This module implement a simple wrapper for output messages (send by clients or server).
It respect the semantics about the communications (this document is available here `specification_slides <../../specification_slides.pdf>`_).

Basically, it a collection of mini pretty-printer.

It also provides the function *try_pickling*, to save datas from binary files (load them with ParseMessageIn.try_unpickling).
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.7a'
__date__='mar. 19/02/2013 at 01h:03m:24s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#: This can be erased by the module Constants to modify the global verbosity of this module
PRINT_ALL_PARSEOUT	=	True

#1###############
# Usual Modules #
#import pprint	#: Use pprint to print the data which are pickling with pickle.
try:
	import cPickle as pickle
except:
	import pickle

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import *	# Constants.py : all the constants

# About Pickling
#################
def try_pickling(data, info="(no info about the pickling was given)", verb=True, fn=filename_pickling):
	 """ Save the datas *data* to the file *fn*.

 This file will be **erase** if present, so be cautious. The file *fn* can then be load with ParseMessageOut.try_pickling.

 The goal of *info* is to say what variables are picked (see the examples below).

 If *verb* is here, this function print a log saying from which file datas are being read.

 This function doesn't handle exception, so be prudent with it.

 Example:
  >>> from ParseMessageIn import try_unpickling
  >>> a, b, c = 0, 2.0, u"ok !"	# Make a tuple.
  >>> try_pickling((a,b,c)) # Save the tuple, in the default file (.datas_saved_by_picked_python.pkl).
  >>> aa, bb, cc = try_unpickling(info="aa, bb, cc") # Load the tuple from the default file, and save it to (aa, bb, cc).

 Warning:
.. warning::
   All datas cannot be picked and upicked.
   Fore more details, see directly the documentation of the **pickle** module.
	 """
	 if verb:
		  ANSIColors.printc('\t/pickle/ <blue>Saving<white> datas %s, to <u>%s<U>...' % (info, fn))
	 try:
	  output = open(fn, 'wb')
	  # Pickle dictionary using protocol -1.
	  pickle.dump(data, output, -1)
	  output.close()
	 except Exception as e:
	  if verb:
	   ANSIColors.printc('\t/pickle/ <red>failed<white> when saving to <u>%s<U>\n\t/pickle/ Cause : %s.' % (fn, e))
	  raise e
	  return False
	 if verb:
	  ANSIColors.printc('\t/pickle/ <green>succed<white> when saving to <u>%s<U>.' % fn)
	 return True

def str_of_state(state):
	 """ str_of_state(state) -> '0', '1', or '2'.
	  The simpliest conversion from a state (Board.State) to a string.

	 Returned values:
	  * '0' for an empty spot.
	  * '1' for a destructible wall.
	  * '2' for a undestructible wall."""
	 if state.wall:
	  if state.destr: return '1'
	  else: return '2'
	 else: return '0'

def str_of_players(board, pl):
	 """ str_of_players(board, pl) -> ";p.pseudo ,p.x,p.y" sequence
Simply return a string representing the list of Player.Player associated with their position.
 All found players *have to be* in the list [pl].

.. warning::

   Take care of the **space** between pseudo and the first *;*.
	 """
	 ANSIColors.printc("<warning> <neg><magenta> Generating the string to seng my list of players....<reset><white> ......")
	 res = ""
	 res_list = ["0"] * len(pl)
	 for i, j, spot in board:		#: ok.
	   if spot.players:
	    for p in spot.players:
	     if p in pl:
#:	      res += ";%s,%i,%i" % (p.pseudo, p.x, p.y)
	      res_list[ p.id ] = ";%s,%i,%i" % (p.pseudo, p.x, p.y)
	      ANSIColors.printc("<warning> <magenta> I have the player <white>[%s], with id=<u>%i<U>, and he/she will be sent as : <neg>%s<Neg>. " % (p, p.id, res_list[ p.id ] ) )
	 for s in res_list:
		res += s
	 # Now, we are sure that we are sending the players in a good order.
	 #
	 # And this is maybe simpler !
#:	      # Ok, this is like in our formal semantics.
#:	 for p in pl:
#:	     res += ";%s,%i,%i" % (p.pseudo, p.x, p.y)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_players<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_newplayer(player):
	 """ str_of_newplayer(player) -> "NEW_PLAYER(player.pseudo)"
	  Sent message by a new player when he try to connect to the server.
	  Contains the pseudo of the player.

	  Can be unpack with ParseMessageIn.newplayer_of_str.
	 """
	 res = "NEW_PLAYER(%s)" % (player.pseudo)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_newplayer<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_newcolor(player):
	 """ str_of_newcolor(player) -> "color=player.color"
	  Sent message by a new player to annouce his color.
	  Currently, not used by the server.

	  Can be unpack with ParseMessageIn.newplayer_of_str.
	 """
	 res = "color=%s" % (player.color)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_newcolor<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_move(move_to_send):
	""" Return a string representing an action (a move or dropping a bomb).
	The *move_to_send* string is one of 'BOMB', 'LEFT', 'RIGHT', 'UP', 'DOWN'.
	From the client to the server.

	Returned value :
	 * PLANT_BOMB.
	 * MOVE_LEFT.
	 * MOVE_RIGHT.
	 * MOVE_UP.
	 * MOVE_DOWN.
	"""
	if move_to_send=="BOMB":
		res = "PLANT_BOMB\n"
	else:
		res = "MOVE_%s\n" % move_to_send
	if PRINT_ALL_PARSEOUT:
	 ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_move<U>: returns <neg>'%s'<Neg>.<white>" % res)
	return res

def str_of_board_and_player(board, pl):
	""" Convert a game state (composed of a board [board], instance of Board.Board; and a list of players [pl], of Player.Player.).
	Of course, positions of players in [pl] have to be concording with states (State.State) of the board.

	FIXME:
	 if lx and ly are not sent, they are constants.
	 not very awesome isn't it ?
	"""
	res = "GAME_START("
	for i, j, spot in board:		#: ok.
	  res += "%s" % spot.to_send()	#: 1,2, or 3
	  if (i<board.lx-1)or(j<board.ly-1):
	   res += ","
	print res
	res += board.str_of_players(pl)
#:	res += ")\n"
	res += ")"	# FIXME?
	if PRINT_ALL_PARSEOUT:
	 ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_board_and_player<U>: returns <neg>'%s'<Neg>.<white>" % res)
	return res

def str_of_gameover(player):
	 """ str_of_gameover(player) -> "GAME_OVER(player.id)"
	 Sent message by the server to announce the winner of the game, by refering to his [id].
	  For the player who have the same id is the *winner*, and the other *lost*.

	  Can be unpack with ParseMessageIn.gameover_of_str.
	 """
	 res = "GAME_OVER(%i)" % (player.id)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_gameover<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_posplantbomb(i, j):
	 """ str_of_posplantbomb(i, j) -> "PLANT_BOMB(i,j)"
	  Sent message by the server to announce that a bomb have been planted in the spot (i,j).

	  Can be unpack with ParseMessageIn.posplantbomb_of_str.
	 """
	 res = "PLANT_BOMB(%i,%i)" % (i,j)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_posplantbomb<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_blowbomb(i, j, radius):
	 """ str_of_blowbomb(i, j, radius) -> "BLOW_BOMB(i,j,radius)"
	  Sent message by the server to announce that a bomb have blowed up
	  in the spot (i,j), with the radius [radius].

	  Can be unpack with ParseMessageIn.blowbomb_of_str.
	 """
	 res = "BLOW_BOMB(%i,%i,%i)" % (i, j, radius)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_blowbomb<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

def str_of_moveplayer(player):
	 """ str_of_moveplayer(player) -> "MOVE_PLAYER(player.id,player.x,player.y)"
	  Sent message by the server to announce that a player have moved.

	  Can be unpack with ParseMessageIn.moveplayer_of_str.
	 """
	 res = "MOVE_PLAYER(%i,%i,%i)" % (player.id, player.x, player.y)
	 if PRINT_ALL_PARSEOUT:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEOUT/ <u>str_of_moveplayer<U>: returns <neg>'%s'<Neg>.<white>" % res)
	 return res

#END
