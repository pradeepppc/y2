#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This module implement all constants used by the game.
 **Do not directly edit this one.**

Configure your client
---------------------

 To configure the **client**, edit `this config file <../../ConfigClient.py>`_.
 His documentation can be found `here <ConfigClient.html>`_.

Configure your server
---------------------

 To configure the **server**, edit `this config file <../../ConfigServer.py>`_.
 His documentation can be found `here <ConfigServer.html>`_.

About specification:
====================
 In particular, the following constants are convention, fixed in the specification:
  * LX_CST=11	-- dimension of the board for x (horizontal),
  * LY_CST=11	-- dimension of the board for y (vertical),
  * NB_PLAYER=3	-- number of client for the game,
  * pv_Init=3	-- initial number of PV for a player (have to be the same both in client and server),
  * force_default=4	-- distance of explosion for a bomb (only fixed for the server),
  * NB_BOMB_MAX_ALLOW=1	-- max number of bomb allowed to be possessed by one player at any moment,
  * PORT_INIT=12882	-- default port for the client and the server.

About other conventions:
========================
 * a *spot* is free (*i.e.* a player can move there) if there is **no wall** (destructible or not), **and** if there is *no bomb*. It is better because that allows players to block each other with their bomb (and, *of course*, to be blocked by their own bomb).
 * that mean a spot is free even if *a player is already in it*.
 * when the explosion of a bomb reach an other bomb, it should trigger the explosion of the new one (*that allows chain reaction*, and it's more funny).
 * a bomb should hurt a player regardless of who initially plant it.
 * the server is the *oracle* for the game : from the point of view of the client, each order coming from the server is to take *au pied de la lettre*, *i.e.* as pure truth (that means, no verification of incoming order is required, even in a *good client*).

The constants are sorted by modules.
Some tool functions are also defined here, mainly for textual mod (TUI).
"""

NB_PLAYER	=	2	#: Number of player for the game.
LX_CST	=	14	#: Dimension of the board, over the x axis (horizontal)
LY_CST	=	14	#: Dimension of the board, over the y axis (vertical)
pv_Init	=	7	#: Have to be the same for all player

__author__='Lilian BESSON'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__email__='lilian.besson[AT]normale.fr'
__license__='GPLv3'
__version__='1.4a'
__date__='mer. 20/02/2013 at 19h:03m:07s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
try:
	import os, sys, time
	__date__ = time.strftime("%a %d/%m/%Y at %Hh:%Mm:%Ss", time.localtime(os.lstat(sys.argv[0]).st_mtime))
	del os, sys, time
except:	pass

#:[['__version__', '__warningregistry__', '__all__', '__credits__', '__test__', '__author__', '__email__', '__revision__', '__id__', '__copyright__', '__license__', '__date__']]
#: Other meta variables. List from `pychecker --help`

#1###############
# Usual Modules #
import os
import subprocess
from random import shuffle

#2################
# Project Module #
import KeyBinding	# KeyBinding.py : implements the key binding.
import ANSIColors	# ANSIColors.py : just some colors definition.

#################################
##### "Graphical" functions #####

clearScreen = ANSIColors.clearScreen	#: To erase the current screen.

#: For printing, erase the screen or not before print the map
#:  It is better *not to*, because that take a lot of unused space in your terminal emulator buffer.
PRINT_CLEAR_EACH_TIME	=  False

def print_clear(e=""):
	""" print_clear(e) -> unit
	Clear the screen if [PRINT_CLEAR_EACH_TIME], then print [e]."""
	if PRINT_CLEAR_EACH_TIME: clearScreen()
	print e

#############################################
##### Tool with ANSIColors and PyZenity #####

def ColorOff(verb=False):
	""" Turn off the support of ANSI Colors.
	Can be used other somewhere else, or on other modules, AFTER importing ANSIColors module !"""
	try:
		for n in ANSIColors.colorList:
		 exec('ANSIColors.%s=\"\"' % n)
		 if verb: print "/deleting colors/ ANSIColors.%s deleted." % n
		print "/deleting colors/ ANSIColors disabling..."
	except:
		print "/deleting colors/ I failed when I tried to disable ANSIColors..."

def ColorOn(verb=False):
	""" Turn on the support of ANSI Colors.
	Can be used other somewhere else, or on other modules, AFTER importing ANSIColors module !"""
	try:
		for n in ANSIColors.colorList:
		 exec('ANSIColors.%s=ANSIColors._%s' % (n, n))
		 if verb: print "/initializing colors/ ANSIColors.%s recreated." % n
		ANSIColors.printc("/initializing colors/ ANSIColors <green>enabling...<white>")
	except:
		print "/initializing colors/ I failed when I tried to enable ANSIColors..."

###############################################
#### A function to print the player's PVs  ####
def print_pvs_player(pl):
	""" print_pvs_player(pl) -> unit
	Print the PVs of all the players in *pl*.
	"""
 	tmp = ""
 	for kk in range(len(pl)): tmp += ("PV[%s]=%i.\t" % (pl[kk], pl[kk].pv))
 	ANSIColors.printc("<neg>Players' lifes<Neg> : <reset>%s.<reset><white>\n" % tmp)
 	return True

###############################################################################
# Lists of constants.

force_default	= 4 #: Distance of explosion.
timer_default	= 6 #: In seconds. For the server only.
power_default	= 1 #: Power of explosion.
owner_default	= None #: No player owner the empty default bomb.
toc_default	= 1 #: Number of tic with one tic() application.

#: They have to not be modified by some exterior stuffs
SIGNAL_WALL_BREAKE	= 2
#: They have to not be modified by some exterior stuffs
SIGNAL_WALL_NOT_BREAKE	= 4
#: Signal returned by the destroy method over a state, if it hurts a player
SIGNAL_PLAYER_HURT	= 3
#: Signal returned by the destroy method over a state, if it hits a bomb
SIGNAL_BOMB_HURT	= 5

#: To know if an explosion is stoped by a destructible wall when it is destroyed.
BREAK_ON_WALL	= True

# Lists of constants for building a board.
lx_Max	= 19	#: Max Length of the board over X axis
ly_Max	= 19	#: Max Length of the board over Y axis
nbmax_Max	= 8	#: Nb Max of player over the board

def str_of_InfoServer((HOST, PORT)):
	"""A very small function to change a tuple (HOST, PORT).
	 representing informations about a server, to a string.

.. warning::
   Delete it : useless.
	"""
	return ("%s:%i" % (HOST, PORT))

#: Lists of constants for building a player.
pseudo_Init	= "anonym"	#: The default pseudo is your UNIX login.
try:
	from os import getlogin, getpid
	#: The default pseudo is your UNIX login, appended with the *PID* of the current process.
	#: This is mainly to force the introduction of *differents* pseudos for testing.
	pseudo_Init = getlogin() + "_" + str(getpid())
	del getlogin, getpid
except:
	pseudo_Init = "YouCanSetYourPseudoWithCommand--pseudo"

color_Init	=  "white"	#: The default color

death_message_Init	= "You died :("	#: FIXME find a way to receive it from the server.
nb_bomb_Init	=  0	#: No bomb on the board initially
x_Init	=  0	#: Default position for x
y_Init	=  0	#: Default position for y

#: Signals for communications of result in Player.Player.move
SIGNAL_TYPE_WRONG	=  1 #: The type of i or j in Player.Player.move was not an integer
SIGNAL_I_NEGATIVE	=  2 #: i in Player.Player.move was not a valid integer
SIGNAL_J_NEGATIVE	=  3 #: j in Player.Player.move was not a valid integer

pseudos_CST	=  ['Aurelie', 'Bobby', 'Celia', 'Dalia', 'Emilie', 'Fhu', 'Gnome', 'Harry']	#: The default pseudos

pseudos_IA =  ['Anne', 'Bob', 'Clark', 'Dan', 'Emma', 'Fabian', 'George', 'Hermionne', 'Ian', 'John',
	'Karol', 'Laura', 'Manu', 'Natalie', 'Ophelie', 'Patrice', 'Quentin', 'Raoul', 'Susane',
	'Tiphaine', 'Ubuntu', 'Valentin', 'Walter', 'Xiu', 'Yoda', 'Zorro']	#: For the bots.

colors_CST	=  ['green', 'red', 'blue', 'black', 'cyan', 'magenta', 'yellow', 'white']	#: The default colors
# for the server : the color of the %i player is colors_CST[i].

#: For the server : choose where it is hosted. (simple values, used by server AND client for Bomberman)
SERVEUR_INIT	=  '0.0.0.0'

PORT_INIT	=  12882	#: The port of the listening connection for the server.

info_server_Init	=  (SERVEUR_INIT, PORT_INIT)	#: Default value, for testing

verb	=  False	#: To know what message have to be printed or not (better is True)

verb2	=  False	#: To know what message have to be printed or not (better is False)

PRINT_ALL_MESSAGE	=  1		#: 1 to print messages

TYPE_MAP	=  0	#: 0, or 1 or 2. 0 is **cool** (players are initially put in the corner).

NB_BOMB_MAX_ALLOW	=  2	#: Max number of bombs allowed to be droped by one player. Ok that works (can be changed).

keyBindingList	=  []
for i in range(NB_PLAYER):
	keyBindingList.append(KeyBinding.classic())


def start_position(type= TYPE_MAP, lx=LX_CST, ly=LY_CST, nb=NB_PLAYER):
	"""start_position(type=TYPE_MAP, lx=LX_CST, ly=LY_CST, nb=NB_PLAYER) -> [integer,.,.], [integer,.,.,.]
	Starting position, returned as a couple of a list of [nb] integer.
	Usefull to make the map : there is currently 3 different types of starting values :
	 * type = 0:
	  On the corner, and on the diagonal, near to the corner.
	 * type = 1:
	  Near to the center.
	 * type = 2:
	  Again nearer to the center.

	The map is supposed to be just of size 11x11.
	"""
	Mi, Mj = [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]
	if type==0:
		Mi, Mj = [0,lx-1,0,lx-1,1,lx-2,1,lx-2], [0,0,ly-1,ly-1,1,1,ly-2,ly-2]
	if type==1:
		Mi, Mj = [1,lx-2,1,lx-2,0,lx-1,0,lx-1], [1,1,ly-2,ly-2,0,0,ly-1,ly-1]
	if type==2:
		Mi, Mj = [3,lx-4,3,lx-4,0,lx-1,0,lx-1], [3,3,ly-4,ly-4,0,0,ly-1,ly-1]
	# FIXME experimental
	shuffle(Mi)
	shuffle(Mj)
	return Mi[:nb], Mj[:nb]

def pseudos_colors(nb=NB_PLAYER):
	""" 8 pseudos and different colors for **initializing the datas** only.
	The server **have to wait** for *real* connections to be able
	 to know the *real* colors and pseudos of the players."""
	return pseudos_CST[:nb], colors_CST[:nb]

#: For ParseMessageIn and ParseMessageOut
#: About pickling : to save and restart variables.
filename_pickling	=  'savegame.ess'

#: If true, use a pickling file to save current game state for the server
USE_PICKLING = False

filename_database	=  'database_clients.db'	#: For storing all incoming connections in BombermanServer.py.

#:If true, use somes tools with a database of all known clients.
#:And print a warning when a new client is detected.
#:
#:.. warning::
#:   This is still experimental and quite limited.
USE_DATABASE = False

###############################################################################
# Lists of constants that really change how the game runs.

USE_BONUS_SYSTEM	= False	#: Not yet implemented.

USE_MUSIC	= False	#: Try to know if music will be used.

USE_SOUND_EFFECT	= False	#: Try to know if sound effects. will be used.

USE_WINDOW	= True	#: Try to know if a graphical window will be used.

USE_NOTIFY	= True	#: Try to know if notifications (with *notify-send*) will be used.

#: Number of loop each seconds.
CLOCK_FREQUENCY	=  15.0	# 1.0, or 100.0 for tests.

#: To use the window in Full screen.
#:
#: .. warning::
#:    By now, fullscreen mod **is not supported**.
USE_FULLSCREEN	= False

TIME_FADEOUT	= 8	#: When the game is done, a final music is played during this period of time.

TIME_EXPLOSION	= 3.0	#: Time for the bombs ?

PROBA_UMUR	= 0.05	#: with probability PROBA_UMUR, a spot is undestructible.

PROBA_BONUS	= 0.05	#: with probability PROBA_BONUS, a spot contains a bonus. Unused right *now*.

INFORM_CLIENTS = False	#: If true, send messages to client when a new player is connecting or disconnecting.

#: An other *experimental functionnality* : use differents frames for displaying the player.
#: That means: one picture for all directions (up, down, left and right).
#: By now, it works, but all player look the same (so it less pretty to use it)
USE_DIRECTION_FOR_PLAYER	=	True

#: To be very verbous with all **outputed** messages (*i.e.* send to the network), produced with ParseMessageOut
PRINT_ALL_PARSEOUT	=	False

#: To be very verbous with all **parsed** messages, produced with ParseMessageIn
PRINT_ALL_PARSEIN	=	False

#: To check action on client side before sending them for validation.
#:  Still not well functional.
PLAYER_CHECK_ACTION	=	False

#END
