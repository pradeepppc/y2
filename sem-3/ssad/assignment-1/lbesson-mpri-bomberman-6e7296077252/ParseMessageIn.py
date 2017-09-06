#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
This module implement a simple analyser for input messages (read from clients or server).
It respect the semantics about the communications (this document is available here `specification_slides <../../specification_slides.pdf>`_).

Basically, it is a collection of mini parsers.

It also provides the function *try_unpickling*, to load datas from binary files (saved with ParseMessageOut.try_pickling).
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.7a'
__date__='mar. 19/02/2013 at 01h:04m:42s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#: This can be erased by the module Constants to modify the global verbosity of this module
PRINT_ALL_PARSEIN	=	True

#1###############
# Usual Modules #
import pprint	#: Use pprint to print the data which are pickling with pickle.
try:
	import cPickle as pickle
except:
	import pickle
# A try of pretty-printing / parsing
#  using printf and scanf
#  usefull to learn how to send datas using strings messages
import scanf

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import *	# Constants.py : all the constants

# About Pickling
#################
def try_unpickling(info="(no info about the unpickling was given)", verb=True,  verb2=False, fn=filename_pickling):
	 """ Load datas from the file *fn*.

 This file **have** to be present, and **have** to be created by ParseMessageOut.try_pickling.

 The goal of *info* is to say what variables will be set equal to the unpicked datas (see the examples below).

 If *verb* is here, this function print a log saying from which file datas are being read.

 If *verb2* is here, this function will also **print all unpicked datas** (using the pprint.pprint pretty-printer).
  Caution ! If the datas are quite huge (and you are allow to do so), the will print a huge message.

 This function doesn't handle exception, so be prudent with it (in particular, the file *fn* have to be there).

 Example:
  >>> from ParseMessageOut import try_pickling
  >>> a, b, c = 0, 2.0, u"ok !"	# Make a tuple.
  >>> try_pickling((a,b,c)) # Save the tuple, in the default file (.datas_saved_by_picked_python.pkl).
  >>> aa, bb, cc = try_unpickling(info="aa, bb, cc") # Load the tuple from the default file, and save it to (aa, bb, cc).

 Warning:
.. warning::
   All datas cannot be picked and upicked.
   Fore more details, see directly the documentation of the **pickle** module.
	 """
	 if verb:
		  ANSIColors.printc('\t/pickle/ <blue>reading<white> from <u>%s<U> to read datas,\n\t/pickle/ and load them into the variable(s) %s...' % (fn, info))
	 try:
	  pkl_file = open(fn, 'rb')
	  data = pickle.load(pkl_file)
	  if verb2:
		  pprint.pprint(data)
	  pkl_file.close()
	 except Exception as e:
	  if verb:
	   ANSIColors.printc('\t/pickle/ <red>failed<white> when reading <u>%s<U>\n\t/pickle/ Cause : %s.' % (fn, e))
	  raise e
	 if verb:
	   ANSIColors.printc('\t/pickle/ <green>succed<white> when reading <u>%s<U>.' % fn)
	 return data

def try_parse(message, pattern, verb=False):
	 """ A simple wrapping around scanf.sscanf.

	 This will try to parse the *message*, according to the scanf *pattern*.
	 If verb, print useful and colored log information."""
	 if PRINT_ALL_PARSEIN:
	  ANSIColors.printc("<magenta>/PRINT_ALL_PARSEIN/ message=<neg>'%s'<Neg>. pattern=<neg>'%s'<Neg>.<white>" % (message, pattern))
	 if verb:
	  ANSIColors.printc('\t/scanf/ <blue>Trying to parse<white> the message [%s] with the pattern [%s]...' % (message, pattern))
	 try:
	  result = scanf.sscanf(message, pattern)
	 except Exception as e:
	  if verb:
	   ANSIColors.printc('\t/scanf/  <red>Fail<white> ! scanf.sscanf raised the exception : %s.' % e)
	  raise e
	 if verb:
	  ANSIColors.printc('\t/scanf/  <green>Success<white> ! scanf.sscanf returned the value(s) : %s.' % str(result))
	 return result

def number_of_kill(s):
	 """ Sent message to manually kill a connected player.

	 For BombermanServer.py."""
	 result = try_parse(s, "\\kill=%i")
	 return result[0]

def newplayer_of_str(s):
	 """ Sent message by a new player when he wants to change his pseudo.
	  Contains the pseudo of the player.
	 """
	 s=s.replace('(','').replace(')','')
	 result = try_parse(s, "NEW_PLAYER%s")
	 return result[0]

def newcolor_of_str(s):
	 """ Sent message by a new player when he wants to change his color.
  Contains the color of the player.

.. warning::
   The color is checked to be correct, i.e. one of the simple color from `ANSIColors.simpleColorList <ANSIColors.html#simpleColorList>`_.
   This list is ['green', 'red', 'blue', 'black', 'cyan', 'magenta', 'yellow', 'white'].
	 """
	 result = try_parse(s, "color=%s")
	 if not(result[0] in ANSIColors.simpleColorList):
	  raise Exception("The color %s is not a valid one (from the list ['green', 'red', 'blue', 'black', 'cyan', 'magenta', 'yellow', 'white'])." % result[0])
	 return result[0]

def update_players(board, list_players, player, message, verb=True):
	 """ Move the players in the list *list_players* according to the order in *message*.

	 This is for the first communication (message GAME_START), and **only for this**.
	 The order was packed with ParseMessageOut.str_of_players.
	 """
	 if verb:	print "update_players: receiving : %s" % message
	 N = len(list_players)
	 if verb:	print "N players, N=%i. Players=%s." % (N, str(list_players))
	 move_done = 0	#: Number of expected moves.
#:	 result = try_parse(message, ";%s,%i,%i"*N, verb=verb)#FIXME
#:	 result = try_parse(message, ";%s,%i,%i"*N+"%s", verb=verb)
	 message = message.replace(',', ' #')
	 # WARNING: this is not like in our formal semantics,
	 # but it's ok anyway.
	 # A try:
	 if message[-1]!='\n':
	 	ANSIColors.printc("\n\n<warning>  I found <neg> no '\\n' caracter at the end<Neg> at message=%s. !!! Not fine ?" % message )
		result = try_parse(message, ";%s#%i#%i"*N, verb=True)
#:		result = try_parse(message+"XXX", ";%s,%i,%i"*N+"%s", verb=True)
	 else:
	 	ANSIColors.printc("\n\n<warning>  I found <neg> one (or more) '\\n' caracter at the end<Neg> at message=%s. !!! Not fine ?" % message )
		result = try_parse(message[0: -1], ";%s #%i #%i"*N, verb=True)
#:		result = try_parse(message[0: -1]+"XXX", ";%s,%i,%i"*N+"%s", verb=True)
	 #######################################################################
	 for l in range(N):
	    if verb:	ANSIColors.printc("\t/update_players/ For the player [%s], looking for an order about id=%i ..." % (list_players[l], list_players[l].id))
	    x, y = result[l*3 + 1], result[l*3 + 2]
	    board[list_players[l].x, list_players[l].y].players.remove(list_players[l])
	    # Update attributes.
	    list_players[l].id = l	# by increasing order.
	    list_players[l].pseudo = result[l*3]
	    if list_players[l].pseudo == player.pseudo:
	    	     ################  FIXME  ##################################
	    	     ANSIColors.printc("\n\n<INFO> <neg> <warning> I'm trying to set the <u>id<U><Neg><white> of you, client [%s], to %i." % ( str(player), l ))
	    	     ANSIColors.printc("<INFO> <warning> <red><u> This is a bug in our protocol <U><Neg><white> <magenta><neg>***maybe***<Neg><white> the parsed *id* wasn't yourse, if an other is using the *same* pseudo as yourse...\n")
	    	     ################  FIXME  ##################################
		     player.move(x,y)
		     player.id = l
		     list_players[l] = player	#FIXME
	    board[x, y].players.append(list_players[l])
	    list_players[l].move(x, y)
	    if verb:
			ANSIColors.printc("\t/update_players/  <green>Found ! <yellow>id=%i => x=%i,y=%i<white>. Moving the player !" % (list_players[l].id, x, y))
	    move_done += 1
	 if (move_done < N) and verb:
		ANSIColors.printc("\t/update_players/  <WARNING> the parser 'ParseMessageIn.update_players' found only %i moves (and %i was expected)..." % (move_done, N))
	 return (board, list_players, player)

def board_and_player_of_str(board, pl, player, message, verb=True):
	"""board_and_player_of_str(board, pl, player, message, verb=True)-> board, pl, player
	 Update the board and the list of players with the map sent in the string *message*.

	The order was packed with ParseMessageOut.str_of_board_and_player.
	"""
	# Now parse the message.
	message=message.replace(')','').replace('(','')
	if verb: print "board_and_player_of_str: receiving : %s" % message
	result = try_parse(message, "GAME_START%s", verb=verb)
	message = message[len("GAME_START"):]

	# Continue parsing.
	for i,j,spot in board:
	 s = message[0] #: 1,2,3
	 if (i<board.lx-1)or(j<board.ly-1):
	   message = message[2:]
	 else:
	   message = message[1:] # no final ','.
	 board[i,j].destr = (s == '1')
	 board[i,j].wall = (s in ['1', '2'])
#:	 if verb: print "i=%i, j=%i => s=%s. Now this spot is %s." % (i,j,s, str(board[i, j]))
	if verb: print board
	if verb: print "board_and_player_of_str: now i look at : %s. I'm starting......" % message
	board, pl, player = update_players(board, pl, player, message, verb=verb)
	return (board, pl, player)

class GameOver(Exception):
	""" Exception Class for handling the end of the game (win or lose).

.. warning::
   Even if his name seems to says otherwise, this exception give the **winner** of the game.
   In fact, the name was choose to fit with the message *GAME_OVER*, already fixer in the formal semantics.
   This message, sent by the server, imply the **end of the game**, and give the *id* of the player who is winning the game.

Attributes:
 * player	-- the player which is which has wan.
 * msg		-- the message in case of victory.
	"""
	def __init__(self, player, msg="This is the default message. The winner is "):
	 """ Construction of a GameOver exception.
	 """
	 self.player = player	#: the player which has wan.
	 self.msg = msg	#: the message annoucing the death, which have to be printed to the player.

	def __str__(self):
	 """__str__(self) -> str
	  A pretty string for the exception. (with colors if self.player supports color)."""
	 return "%s %s." % (self.msg, self.player)

def gameover_of_str(s):
	"""gameover_of_str(s) -> s2, id
	Received message from the server to announce the winner of the game, by refering to his [id].
	For the player who have the same id : he is the *winner*, and for the other : they have *lost*.

	[s2] refers to the end of the message [s] (untouched by the data's extraction).

	The order was packed with ParseMessageOut.str_of_gameover.
	"""
	s=s.replace(')','').replace('(','')
	result = try_parse(s, "GAME_OVER%i")
	s = s[ len( "GAME_OVER%i" % (result[0]) ) :]
	return s, result[0]

def posplantbomb_of_str(s):
	"""posplantbomb_of_str(s) -> s2, i, j
	Received message from the server to announce that a bomb have been planted in the spot ([i], [j]).

	[s2] refers to the end of the message [s] (untouched by the data's extraction).

	The order was packed with ParseMessageOut.str_of_posplantbomb.
	"""
	s=s.replace(')','').replace('(','')
	result = try_parse(s, "PLANT_BOMB%i,%i")
	s = s[ len( "PLANT_BOMB%i,%i" % (result[0], result[1]) ) :]
	return s, result[0], result[1]

def blowbomb_of_str(s):
	"""blowbomb_of_str(s) -> s2, i, j, radius
	Received message from the server to announce that a bomb have blowed up
	 in the spot (i,j), with the radius [radius].

	[s2] refers to the end of the message [s] (untouched by the data's extraction).

	The order was packed with ParseMessageOut.str_of_blowbomb.
	"""
	s=s.replace(')','').replace('(','')
	result = try_parse(s, "BLOW_BOMB%i,%i,%i")
	s = s[ len( "BLOW_BOMB%i,%i,%i" % (result[0], result[1], result[2]) ) :]
	return s, result[0], result[1], result[2]

def moveplayer_of_str(s):
	"""moveplayer_of_str(s) -> s2, id, i, j
	Received message from the server to announce that a player [id] have moved to [i], [j].

	[s2] refers to the end of the message [s] (untouched by the data's extraction).

	The order was packed with ParseMessageOut.str_of_moveplayer.
	"""
	s=s.replace(')','').replace('(','')
	result = try_parse(s, "MOVE_PLAYER%i,%i,%i")
	s = s[ len( "MOVE_PLAYER%i,%i,%i" % (result[0], result[1], result[2]) ) :]
	return s, result[0], result[1], result[2]

# END
