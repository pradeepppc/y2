#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
 This program is the **server** for our *Bomberman multiplayer game*.

Example
-------
  This show how the **textual mode** *looks like during the game* :

.. image:: images/exempletextual_server.png
   :scale: 100 %
   :align: center

How to ?
========

 The program accept some *command line* options.

 The simpliest way to use it is::
  **$ ./BombermanServer.py --server bomberman.crans.org --port 12885**
 This will launch the *server* on **bomberman.crans.org** (assuming that your machine is *opened* on the Internet with this domain name), on the *port* **12885** (it **have** to be an open port, maybe you will have to change something in your *firewall*).
   On *Windows*, a window will surely pop to ask you confirmation for this (with a message like "Python is trying to use the port 12885, are you sure ?").

PyRlwrap
---------

 The client *have* to be launched from the **command line**, and during the game the *stdin* (*i.e.* the keyboard) is listened.
  So you can send messages yo your server, directly from the command line.
  The script `PyRlwrap.py <PyRlwrap.html>`_ provide a **readline wrapper** for this command line interface. It brings:
   * shortcut, "a la Nano" (^A: begin line, ^E: end line etc);
   * history (Up & Down show previous message).

 You can launch the client with *PyRlwrap.py* like this (-vv is to *increase* verbosity):
  **$ ./PyRlwrap.py ./BombermanServer.py --server 138.231.134.230 --port 9312 -vv**

Options for textual mod
-----------------------

 The following options can change how the *textual mod* looks like :
  * --noUTF : disabled *UTF* caracters for the board.
    And, **warning** for pseudos, if one begins with a *non-ascii* caracter, the *id* of the player is used (an integer, between 0 and the number of player -1).
  * --noANSI or --ANSI : force to disable or enable the colors.
    Normally, you don't have to use them, because the `ANSIColors module <ANSIColors.html>`_ can detect *cleverly* if colors are supported.
    (Note: this have been tested with **Linux**, **Cygwin**, but not with **Mac OS X**)

Saving and restoring
--------------------

 This is an experimental functionnality, but it should work.
  You can try to **launch again the server on his last state**, with the --load option.
  By default, the *loaded file* is *savegame.ess*, but you can specifify yourse with the --file option.

 And the save file can also be changed with the --save option.
  But this functionnality *have* to be enabled with changin USE_PICKLING to True in `ConfigServer.py <ConfigServer.html>`_.

About
=====

Getting some help
-----------------

 This program uses a *high-level* **command line** parser : `ParseCommandArgs <ParseCommandArgs.html>`_, based on *argparse* from the standard distribution.

 Therefore, the *help* for this program can be obtained simply with ::
  **$ ./BombermanClient.py --help**

 The *help* embed some colors, and it can be read through a pipe :
  **$ ./BombermanClient.py -h | less -r**

About:
======

Algorithm:
----------

 The server follows an algorithm in 3 main parts.

 1. First he **waits for clients**, and **register** them.
    Then, he create the game variables, **send the map** to the clients; and start his 2nb part.

 2. He **listen for order** from clients, **check** them, and if they are ok, **apply** them to his local version of the game.
    Then he make evolved his own game (blow the bomb *etc*).
    And he **send back order** to the clients, saying what have been *modified*.
    And the loop 2 begin again.

 3. And when only one player is on the game, he is declared as the winner.

Choices:
--------

 * For handling many clients (*i.e.* listening for many incoming orders), **select.select** is used.
    Both for the step 1 and 2.
 * The **syntax of messages** is :
    * explained in the `specification_slides.pdf <../../specification_slides.pdf>`_,
    * or in the module `ParseMessageIn <ParseMessageIn.html>`_,
    * or in the module `ParseMessageOut <ParseMessageOut.html>`_;
 * The **specification** of the game protocole is also detailed in the slides (and mainly it explains why **we use TCP**).

Saving and restoring:
=====================

 The server can **save and restore** his state.

How ?
-----

 It still very experimental, and quite limited : socket connections **cannot** be save to a file and restore later !
 But, by now, the board can be save during the game, and them restore after when launching a new server, to begin with this map.

 1. That mean, with the option *--load -f savegame.ess* you can try to **load** a previous map save in *savegame.ess*

 2. And with the option *--save savegame2.ess*, you can try to **save** the current map to *savegame2.ess* during the game.

 .. warning::
    This optionnal functionnality have to be **enabled**, by puting *USE_PICKLING* to 1 in `ConfigServer <ConfigServer.html>`_.

Example:
--------

 The server (left up corner) picked up the last map and will start the game with it and not a randomly generated one.

.. image:: images/exemple_saverestore.png
   :scale: 76 %
   :align: center

Warning
=======
.. warning::
   This script is not yet fully concluded.
   So, it might end badly on some untests behaviour.
   I ran many tests, but I can't ensure everything is all right...

TODOs ?:
=======
 * ? implement and describe the bonus system.
 * ? conclude the parser (add --bonus to activate bonus (not implemented yet)).
"""

__author__='Lilian BESSON'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__email__='lilian.besson[AT]normale.fr'
__version__='1.2a'	#: Version of this module
__date__='mar. 19/02/2013 at 22h:48m:15s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
try:
	import os, sys, time
	__date__ = time.strftime("%a %d/%m/%Y at %Hh:%Mm:%Ss", time.localtime(os.lstat(sys.argv[0]).st_mtime))
	del os, sys, time
finally:	pass
#1###############
# Usual Modules #
import socket, sys, select, os, copy, random, time
import thread

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import *	# Constants for the game
import Matrix		# Matrix.py : simple module to manipulate matrix, for the board.
import Player		# Player.py : implements the simple player system. (actions, representation etc)
import Board		# Board.py : two classes Board.Board and Board.State.
import ParseMessageOut	# ParseMessageOut.py : pretty printing of data types, for exchange on the net.
import ParseMessageIn	# ParseMessageIn.py : parsing of data types, for exchange on the net.
from AffichPygame import *	# Brings pygame ! Mainly for music, keyboard reaction and graphical window.

try:
	from ConfigServer import *
	if verb and verb2:
		print "The file %s have been loaded as a configuration file for the server." % 'ConfigServer.py'
		print "The server will use the profile named '%s'." % profile_name
	assert( CLOCK_FREQUENCY > 1.0 )
	assert( CLOCK_FREQUENCY < 80.0)
finally:
	if verb and verb2:
		print "[ERROR] I failed when I tried to load the file %s as a configuration file for the server." % 'ConfigServer.py'

###############################################################################
##### First net functions #####

def print_on_all(message = 'No message was gave', list_clients = [], origin = 'you (the server)', PRINT_ALL_MESSAGE = PRINT_ALL_MESSAGE):
	""" Print the *message* on **stdout** of each client (found in the list of client *list_clients*).
	*origin* permits to print some usefull informations for delivering the origin of the message the all connected clients.

	FIXED: doesn't fail any more.
	"""
	if PRINT_ALL_MESSAGE:
	 ANSIColors.printc("""
/print_on_all/ The message [<yellow>%s<white>], sent by %s, <green>is delivering<white> to all <u>%i other client%s<U>...
""" % ((message ), origin, len(list_clients), "s" if list_clients else ""))
	for socket_client in list_clients:
		try:
		 # FIXME: be sure of this.
		 if message[-1]!='\n':
		 	socket_client.send(message+'\n')
		 else:
		 	socket_client.send(message)
		except:
		 address_client = socket_client.getpeername()
		 ANSIColors.printc("""
<warning> <red> I failed when I tried to send the message '<neg>%s<Neg>' to the client %s:%s...
<warning> <red> Exception = <neg>%s<Neg>.<white>
""" % ( message, str(address_client[0]), str(address_client[1]), str(sys.exc_info()[1]) ) )
	return True

def create_bind_socket(server = (SERVEUR_INIT, PORT_INIT)):
	"""create_bind_socket(server = (SERVEUR_INIT, PORT_INIT)) -> msocket
	 Create a **server** socket and bind it to the *port* and the addresse *host*.
	Make also this socket listening (with socket.listen).
	"""
	msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	msocket.bind(server)
	msocket.listen(64)
	return(msocket)

def create_data_socket(listen_socket, NB_CLIENT = 0, verb = True):
	"""create_data_socket(listen_socket, NB_CLIENT = 0) -> data_socket, data_address, NB_CLIENT
	 Create a **client** (data) socket from the **server** socket *listen_socket*.
	Update the integer [NB_CLIENT] by one.

	Print useful and colorful informations about this connection, and then return a 3-tuple :
	 * the created socket,
	 * the origin address of the listen_socket (addr. of the server (so, not very useful)),
	 * and the current number of clients.
	 """
	# This step can fail.
	data_socket, data_address = listen_socket.accept()
	NB_CLIENT += 1
	if verb:
		ANSIColors.printc("""
/new_socket/ A client connects to <green>addr:%s with port:%i<white>,
""" % data_address)
		ANSIColors.printc("""/new_socket/  This client is the <black>%ith<white> to connects.
""" % NB_CLIENT)
	return(data_socket, data_address, NB_CLIENT)

###############################################################################
##### Help for the User interface #####

# The help message, which can be printed to the user when invoking *'\\?'*
help_User = """
<green><u>Welcome in Bomberman server<U><white>, v%s.
	<blue>Wrote by %s, last version dated of %s.<white>
	Wrote in Python 2.7.3, using ANSIColors for colors in output messages.
	Reference page for this software is there : <u>https://bitbucket.org/vcohen/projet_reseau<U>.

<neg>You are a Bomberman server<Neg>, which accepts client using **TCP sockets**.
The server is mainly 3 steps :
 1. Create a map, then wait for users to connect to the server (and collect informations to them : their name and their favorite color). [1. is ok]
    When there is just enough player to begin the game, launch it !
 2. As an "infinite" loop, wait for actions from the players, then *check* them,
     then apply them to the local version of the game,
     then broadcast the action, using strings and the socket.send function. [2. is not yet ok]
 3. Conclude when a player wins the game, broadcast the name of the winner, and close. [3. is ok]
""" % (__version__, __author__, __date__)

# For the commands (with function *action_on_readstr*)
help_commands = """The following <green>commands are implemented<white> :
	<neg>\\h, \\help, \\?<Neg>	:	print a usefull help message,
	<neg>\\whoami<Neg>		:	print the informations about you (address, port),
	<neg>\\out<Neg>		:	logout (act like Ctrl+D),
	<neg>\\list<Neg>		:	list of all currently connected players,
	<neg>\\kill=NUM<Neg>	:	close manually the client number NUM (in order of connection, not by there port).<white>
"""

def print_list(player_clients):
	""" To print the list of current players.
	"""
	ANSIColors.printc("""
/list client/ %s.\n
/list client/ <green>The game is running with %i players<white>.
	""" % ( str(player_clients), len(player_clients) ))
	return(True)

def print_help(commands = True):
	""" To print the help for the second phasis 2.
	"""
	ANSIColors.printc("""\n
/phasis 2/ <u><green>You are running a Bomberman Server.<U><white>
/phasis 2/  This software is like a basic IRC server : it listen for the already registered clients.\n
/phasis 2/ Those clients have <neg>already received<Neg> the map you built.
/phasis 2/  So, they will send you orders,
	/message in/ <neg>MOVE_DOWN, MOVE_LEFT, MOVE_UP, MOVE_RIGHT<Neg>	-- for moves;
	/message in/ <neg>PLANT_BOMB<Neg>	-- for a new bomb.\n
/phasis 2/  And the server will : validate the order, apply it to his local game, then send back orders.
/phasis 2/  The clients use those orders to update their own game.\n
/phasis 2/ For example:
	/messages out/ <neg>MOVE_PLAYER(2,10,4)<Neg>	-- to move the 2nd player to 10,4;
	/messages out/ <neg>PLANT_BOMB(10,4)<Neg>	-- to put a new bomb in the spot 10,4;
	/messages out/ <neg>BLOW_BOMB(10,4,2)<Neg>	-- to make blow the bomb in the spot 10,4, with a radius of effect 2;
	/messages out/ <neg>GAME_OVER(2)<Neg>	-- to announce that the 2nd player losed.\n
/phasis 2/ You can also send manually messages to your clients, and they can send messages to you (if they are well designed).
/phasis 2/  <u>Just type here !<U>
	""")
	if commands:
		ANSIColors.printc(help_commands)
	return(True)

###############################################################################
#### Reaction to specials messages : commands ####

def action_on_readstr(readstr, list_clients, dict_clients, player_clients, server, lx, ly, nb):
	"""action_on_readstr(readstr, list_clients, dict_clients, player_clients, server, lx, ly, nb) -> <bool>
	 Reaction to special message readed from the keyboard !

	The goal is to allow the *administrator* of the server to act through the command line.

	Return *True* is the key did something, *False* if the *readstr* wasn't a command.
	"""
	if readstr in ['\\h\n', '\\help\n', '\\?\n']:
		ANSIColors.printc("/whoami/ You are a Bomberman Server, listening for player over the net interface : <neg>%s<Neg>." % str_of_InfoServer(server))
		ANSIColors.printc('/\\help/ <blue>Help : \\h or \\help or \\?<white>:')
		ANSIColors.printc(help_User)
		ANSIColors.printc(help_commands)
		return True
	if readstr in ['\\out\n']:
		for s in player_clients:
	 		s.close()
		ANSIColors.printc("""
/\\out/ <warning> <red>Server is closing<white>, because <yellow>server wants to, with the \\out command !<white> (this is a very extrem way to quit : no cleaning and no message to your clients...)""")
		os._exit(1)
	if readstr[:5] in ['\\kill']:
		ANSIColors.printc("\\kill=NUM : close manually the client number NUM. Trying to determin NUM...")
	  	try:
		 indice_client = ParseMessageIn.number_of_kill(readstr)
		 assert( (indice_client > 0) and (indice_client < nb))
	 	 ANSIColors.printc("/\\kill=/ I understood this command with NUM=%i." % indice_client)
	 	 # Informing about this logging out
	 	 ANSIColors.printc('/\\kill=/ Client <green>%s:%i<white> <red><u>killed manually<U><white> !' % dict_clients[indice_client])
	 	 ANSIColors.printc('/\\kill=/  He was the player : %s (repr. = %s).\n' % (str(player_clients[indice_client]), repr(player_clients[indice_client]) ))
		 for client in list_clients:
		   client.send(ANSIColors.sprint('/\\kill=/ Client %s <red><u>killed manually<U><white> by the server !\n\t/K/  He was the player : %s (repr. = %s).\n' % ( dict_clients[indice_client], str(player_clients[indice_client]), repr(player_clients[indice_client]) ) ))
	 	 # Removing the client/player from the data lists
	 	 dict_clients.pop(indice_client)
	 	 list_clients.pop(indice_client)
	 	 player_clients.pop(indice_client)
	 	 # Done !
		except Exception as e:
		 ANSIColors.printc(" <red><u>Fail because %s<U><white>" % e)
	  	return True
	if readstr in ['\\whoami\n', '\\who am I\n']:
		ANSIColors.printc("/\\whoami/ You are a Bomberman Server, listening for player over the net interface : <neg>%s<Neg>." % str_of_InfoServer(server))
		ANSIColors.printc("/\\whoami/ You will wait for %i clients, then launch a game with a board of dim %ix%i." % (nb, lx, ly))
	  	return True
	  	###########
	if readstr in ['\\list\n', '\\clients\n']:
		ANSIColors.printc("/\\list/ There is currently <neg>%i connected clients<Neg>." % len(list_clients))
		for i in range(len(player_clients)):
		 ANSIColors.printc("This is the client number = <neg>%i<Neg>. He is connected from <u>%s<U>, and he his the player %s (repr. %s)" % (1+i, str(dict_clients[i]), player_clients[i], repr(player_clients[i])))
	  	return True
	return False

###############################################################################
#### First phasis for the game : initialization ####

def run_phasis1(lx = LX_CST, ly = LY_CST, nb = NB_PLAYER, server = (SERVEUR_INIT, PORT_INIT), board = None):
	"""run_phasis1(lx = LX_CST, ly = LY_CST, nb = NB_PLAYER, server = (SERVEUR_INIT, PORT_INIT)) -> (nbmax, lx, ly, pl, board, Mi, Mj)
 Creating all Game variables.
	The [server] variable refers to the address (and the port) of the server being builted.

	This is the 1st step of the server algorithm : creating the game, wait for client, register them, and when there are the correct number, go to step 2 (i.e. this function returns and new connection are no longer accepted).

	Returns (nbmax, lx, ly, pl, board, Mi, Mj) :
	 * nbmax: the max number of player for the map,
	 * lx, ly: the dimension of the map,
	 * pl: the list of all the player connected with the server,
	 * board: the map,
	 * Mi, Mj: two integer lists, long as pl, of players' initial positions."""
	# Initialing the server.
	ANSIColors.printc('/phasis 1/ <blue>Bomberman Server is initializing at <green><u>%s:%i<U><white>...' % server)
	try:
	 socket_server = create_bind_socket(server)	#: Now the server is open to listen from the network.
	except Exception as e:
	 ANSIColors.writec('\t<ERROR> <red>Bomberman Server <u>have failed<U> when trying to initialized to connection...<white>\n', file=sys.stderr)
	 ANSIColors.writec('\t<ERROR> Exception catched : <u>%s<U><white>\n' % str(e), file=sys.stderr)
	 os._exit(2)
	 # Hard quit : a server not connected to the network is nothing.
	ANSIColors.printc('/phasis 1/ <green>Bomberman Server <u>seems<U> to listen correctly on the network : <neg>%s:%i<Neg>...<white>' % server)
	ANSIColors.printc("/help/ Enter <blue>\\?<white> for <u>more help<U>.")
###############################################################################
	# Pseudos and colors for players
	pseudos, colors = pseudos_colors(nb)
	# Start position.
	if not board:
		Mi, Mj = start_position(TYPE_MAP, lx, ly, nb)
	else:
		Mi, Mj = [], []
		for tmp_pl in board.players():
		 Mi.append(tmp_pl.x)
		 Mj.append(tmp_pl.y)
		for i, j, tmpspot in board:
		 board[i, j].players = copy.copy([])
		 board[i, j].explosion = False
		 board[i, j].bomb = None
		ANSIColors.printc("""
/load/ Starts positions have been recover from the loaded map...
/load/Mi=<neg>%s<Neg>,\t Mj=<neg>%s<Neg>. """ % ( str(Mi), str(Mj) ))
		ANSIColors.printc("/load/ Now the current board is :\n%s" % str(board))
###############################################################################

	ANSIColors.printc("\n/initGame/ The board will be constructed with those parameters : TYPE_MAP=%s, lx=%i,ly=%i,nb=%i." % (str(TYPE_MAP), lx, ly, nb))
	# This one is always like this.
	nbmax = nb
	if nbmax>nbmax_Max or 0>nbmax:
	 ANSIColors.printc("<warning> <red>Nb of players ( = len(players)) have to be strictly in [|1;%i|] !<white>" % nbmax_Max)

	#: List of connected players
	player_clients = []
	#: List of associated sockets
	list_clients = []
	#: List of associated list of addresses
	dict_clients = []
	# The number of client that have been found (i.e. length of the last 3 lists)
	NB_CLIENT = 0

	if USE_DATABASE:
		#: GOAL: allow some user and block others.
		try:
		 import shelve
		 database = shelve.open(filename_database, writeback = True, flag = 'c')
		except Exception as e:
		 ANSIColors.printc("""/database/ <red>Error when opening the database<white> (<neg>%s<Neg>).\t/database/  Maybe the module isn't correctly installed or maybe the file is already there but with restrictive IO rights ?""" % filename_database)

	#: Logging this operations
	ANSIColors.printc("""
/waiting room/ <neg>Bomberman Server is launching step #1<Neg> : <u><magenta>waiting room.<white><U>
/waiting room/	* It act like a basic IRC server, waiting for new clients.
/waiting room/	* As soon as <green>%i clients<white> will be available, after they will all send their pseudos [and their colors], the game will begin.
/waiting room/	* You can send messages to your clients, and they can send messages to you (if they are well designed).
	""" % nbmax)
	# Informing that the database is well opened.
	if USE_DATABASE:
	 ANSIColors.printc("""/database/ <green>The database<white> (<neg>%s<Neg>) is well initialized !""" % filename_database)

	# Going in the main loop.
	keep = True
###############################################################################
	try:
	 while (len(player_clients) < nb) or keep:
	 	keep = True
		# Wait for new client ! As soon as the [nb]th client will be identified,
		#  and a pseudo/color will be stored for each of them, this will end.
		# And only do this !!
		list_listen = list_clients + [socket_server, sys.stdin]
		list_in, useless1, useless2 = select.select(list_listen, [], [])
		# Here is the trick with *select.select*.
		for socket_in in list_in:
		 # If the administrator is using the keyboard to send message to the clients,
		 #  for example to simplify communications
		 if(socket_in is sys.stdin):
		   readstr = sys.stdin.readline()
		   if action_on_readstr(readstr, list_clients, dict_clients, player_clients, server, lx, ly, nb):
		    continue
		   NB_CLIENT = len(dict_clients)	# update in case administrator used the command \\kill.
		   if len(readstr) == 0:
		   	ANSIColors.printc('/EOF ?/ Server sends <u>an EOF signal<U> : <red>server is closing<white> ...')
		   	raise KeyboardInterrupt
		   ANSIColors.printc('/out/ Server <blue>%s:%i <green>sends a message<white>.' % server)
		   origin = 'Server[%s:%i]' % (server)
		   print_on_all(readstr, list_clients, origin)
		 # If it's not from the administrator.
		 # /!\ in this context, that **don't** mean necessarily a new player (because it is **also** a chat room)
		 else:
		  file_in = socket_in.makefile()
###############################################################################
		  # It is a new client !
		  if(socket_in is socket_server):
		  	# The creation of the socket update NB_CLIENT automatically !
		 	new_client, address_client, NB_CLIENT = create_data_socket(socket_server, NB_CLIENT)
		 	# Make a new Player.PlayerServer to representing this client.
		 	new_player = Player.PlayerServer(pseudo = pseudos[NB_CLIENT-1], color = colors[NB_CLIENT-1])
		 	# Here is CREATED the Player.PlayerServer instance, but not well modified
		 	#  to have the good pseudo/color.
		 	# A good client *have* to send those informations, just after his connection.
		 	#######################
		 	new_player.id = NB_CLIENT-1
		 	# His pseudo and color are initialized with the default values.
		 	ANSIColors.printc('/new/ A new Player.PlayerServer have been created : <neg>%s<Neg>.' % new_player)
		 	if USE_DATABASE:
			 	if not database.has_key(address_client[0]):
			 	 ANSIColors.printc('/database/ This player is <yellow>unknown in the database<white> (<neg>%s<Neg>).' % filename_database)
				try:
				 database[address_client[0]] = (new_player.pseudo, new_player.color)
			 	 ANSIColors.printc('/database/ This player is <green>now stored<white> on the database (<neg>%s<Neg>), with the mapping <u>[%s] \\mapsto [%s]<U>.' % (filename_database, address_client[0], str(database[address_client[0]])))
			 	except Exception as e:
			 	 ANSIColors.printc("""/database/ <red>Error (%s) when registering<white> this new player on the database (<neg>%s<Neg>).""" % (e, filename_database))
		 	# If you want to inform all the already connected client that a new one have been found ?
		 	if INFORM_CLIENTS:
		 	 print_on_all(ANSIColors.sprint("""
/new_client/ A new client connects to <green>addr:%s with port:%i<white>,
/new_client/  This client is the <blue>%ith<white> to be connected to the <u>same<U> Bomberman Server as yourse,
/new_client/  This client is currently represented as the player %s (repr %s).
""" % (address_client[0], address_client[1], NB_CLIENT, str(new_player), repr(new_player))), list_clients, 'Server[%s:%i]' % (server))
			# Add the new client to the local datas.
		 	ANSIColors.printc('/adding/ This new player is added to list_clients; dict_clients; player_clients.')
		 	list_clients.append(new_client)
		 	dict_clients.append(address_client)
		 	player_clients.append(new_player)
			ANSIColors.printc('/repr./  This client is currently represented as the player %s (repr %s).\n' % (str(new_player), repr(new_player)))
###############################################################################
		  # One of the already connected client is sending a message
		  else:
		  	# Get the variable representing the player
		  	address_client = socket_in.getpeername()
		 	indice_client = dict_clients.index(address_client) # WARNING here.
		 	player = player_clients[indice_client]
		 	# Inform who is being listened
		 	ANSIColors.printc("""
<u>/listen/ <neg>Listening<Neg> to client <blue>%s<white>, number <red>%s<white> :<U>
""" % (str(address_client), str(1+indice_client)))
		 	ANSIColors.printc('/repr./  In the game, this client is the player : %s (repr. <neg>%s<Neg>)' % (str(player), repr(player)))
		 	# Read a message from one of the available client
		 	readstr = file_in.readline()
		 	if len(readstr)>0:
		 	 ANSIColors.printc('/reading/ Client <blue>%s:%i <green>sends a message<white> :' % address_client)
		 	 ANSIColors.printc('/reading/ This is his message : <blue>%s<green>...' % readstr)
		 	 if INFORM_CLIENTS:
			 	 list_clients.remove(socket_in)
			 	 origin = 'Client[%s:%i]' % address_client
			 	 print_on_all(readstr, list_clients, origin)
			 	 list_clients.append(socket_in)
			 	 ANSIColors.printc('/reading/  His message have been printed on <green>all %i other client\'s stdout<white>.' % (len(list_clients) - 1))
		 	 # Analyze the message from the client, and if it has the good form, change the attributes of the player.
		 	 try:
		 	  # message pseudo = %s
		 	  player.pseudo = ParseMessageIn.newplayer_of_str(readstr[:len(readstr)-1])[:32]
		 	  keep = False	# that mean : if it is the last client, then ok I can stop now.
		 	  		# and *color*s are just an add-on, so they are *not* mandatory.
			  ANSIColors.printc('/scanf/  <green>Success<white> ! The player <blue>%s<white> have changed his <u>pseudo<U> to %s (and now, he is %s).' % (origin, player.pseudo, player))
			  if USE_DATABASE:
				  database[address_client[0]] = (player.pseudo, player.color)
			 	  ANSIColors.printc('/database/ This player have changed <green>in the database<white> (<neg>%s<Neg>), with the mapping <u>[%s] ~~~~» [%s]<U>.' % (filename_database, address_client[0], str(database[address_client[0]])))

			 except Exception as e1:
#:			  try:
		 	   # message color = %s
#:		 	   player.color = ParseMessageIn.newcolor_of_str(readstr[:len(readstr)-1])[:32]
#:			   ANSIColors.printc('/scanf/  <green>Success<white> ! The player <blue>%s<white> have changed his <u>color<U> to %s (and now, he is %s).' % (origin, player.color, player))
#:			   if USE_DATABASE:
#:				   database[address_client[0]] = (player.pseudo, player.color)
#:			 	   ANSIColors.printc('/database/ This player have changed <green>in the database<white> (<neg>%s<Neg>), with the mapping <u>[%s] \\mapsto [%s]<U>.' % (filename_database, address_client[0], str(database[address_client[0]])))
#:		 	  except Exception as e2:
			    if verb2:
			     ANSIColors.printc('/scanf/  <red>Fail<white> : the message was not a command. (e1 = %s)') ##'; e2 = %s)' % (e1, e2))
		 	 # Maybe the value of the player have been changed.
			 ANSIColors.printc("""
/repr/  This client is currently represented as the player %s (repr %s).
""" % (str(player), repr(player)))
		        else: # nothing readed from the client : he logged out or exited
		 	 ANSIColors.printc('/logged out/ Client <green>%s:%i<white> <red><u>logged out<U><white> !' % address_client)
		 	 # Removing the client/player from the data lists
		 	 NB_CLIENT = NB_CLIENT - 1
		 	 dict_clients.remove(address_client)
		 	 list_clients.remove(socket_in)
		 	 player_clients.remove(player)
		 	 # Informing about this logging out
		 	 ANSIColors.printc("""
/client out/  He <red>was<white> the player : %s (repr. = <neg>%s<Neg>).
""" % (str(player), repr(player) ))
		 	 # If you want to inform all the already connected client that he quit ?
		 	 if INFORM_CLIENTS:
		 	  print_on_all('/client out/ Client %s logged out !\n\t/5/  He was the player : %s (repr. = %s).' % ( ("%s:%i" % address_client), str(player), repr(player) ), list_clients, origin = 'Server[%s:%i]' % (server) )
	except Exception as e:
		if USE_DATABASE:
			database.close()
			ANSIColors.writec('/database/ <blue>The database have been closed<white> !')
		ANSIColors.writec('\a\n\t/END Phase 1/ <red>Server is closing<white>, because <red>%s<white> !' % e)
###############################################################################
	# Here : the while loop is concluded, the except might not have been executed.
	# So, the first step is almost done :
	#  * we have the informations about the map,
	#  * we have the correct number of players, each corresponding to a client
	# == > we just have to create the map, and return all those datas.
	ANSIColors.printc('\n\t/./ <red>Phasis #1 is done<white>, now, the map is being constructed !')
	ANSIColors.printc('/./  <red> The current list of player is <white>:\n\t/./ %s\n' % (str(player_clients)) )

	# Build the *final* list of player.
	nb = len(player_clients)
	for i in range(nb):
		ANSIColors.printc("/n/ Add a player : his number #%i. He is %s (repr. %s)." % (i, player_clients[i], repr(player_clients[i])))
	# Convert players to state
	spl = list()
	for i in range(nb):
	 spl.append(Board.State(wall = False, players = [player_clients[i]]))
	if not board:
		# Initialize the board
		board = Board.Board(Board.empty, lx, ly)
		# Change how to print boxes of the board (|-+/\\ or nonANSI)
		board.mat.box = Matrix.boxnoASCII if Board.UTFSupported else Matrix.boxASCII

		for i, j, spot in board:		#: ok.
			newspot = copy.copy( Board.empty )
			if (i>0) and (j>0) and (i<lx-1) and (j<ly-1) and (PROBA_UMUR > random.random()):
			  # no umur over the walls.
			  newspot = copy.copy( Board.umur )
			else:
			  newspot = copy.copy( random.choice( [ copy.copy(Board.dmur), copy.copy(Board.empty), copy.copy(Board.empty)] ) )
			if ((i%2 == 1) and (j%2 == 1)) and (0.3*PROBA_UMUR <= random.random()):
			 # Idea from Lucas Hosseini.
			 newspot = copy.copy( Board.umur )
			newspot.players = copy.copy([])
			board[i,j] = copy.copy(newspot)
	else:
		ANSIColors.printc("/pickle/ <INFO> <neg><u><green>The board was already here !<reset><white>")
	for i in range(nb):
		player_clients[i].move(Mi[i], Mj[i])
		board[Mi[i], Mj[i]] = spl[i]	# do not use copy.copy here : spl[i] are pointers to player_clients[k]
		for deltax in [-1, 1]:
		 for deltay in [-1, 1]:
		   if (Mi[i]+deltax >= 0) and (Mj[i]+deltay >= 0) and (Mi[i]+deltax <= lx-1) and (Mj[i]+deltay <= ly-1):
		    board[Mi[i]+deltax, Mj[i]+deltay].destr = False
		    board[Mi[i]+deltax, Mj[i]+deltay].wall = False
	# Send everything to all the clients.
	msg = ParseMessageOut.str_of_board_and_player(board, player_clients)
	ANSIColors.printc("/send/ The map has been created, and I'll send it to all the players.\n\t/send/ %s" % msg)
	print_on_all(message = msg, list_clients = list_clients, origin = 'Server[%s:%i]' % (server))
	print_clear("\n" + str(board))
	# Return all those created values.
	# To continue the game -> direction Phasis#2.
	return (nb, lx, ly, player_clients, board, Mi, Mj, socket_server, list_clients, dict_clients)

###############################################################################
#### Using Pickle ####

def save_current_game(variables_to_save, info = "variables_to_save", fn=filename_pickling):
	""" Save all variables content the list *variables_to_save*, in a .pkl file.

	The game can be restored then, by setting all variables equals
	 to their previous values
	 (**of course** this only work if the .pkl file is still there)."""
	return ParseMessageOut.try_pickling(variables_to_save, info, fn=fn)

###############################################################################
#### Mail Loop for the game ####

def run_phasis2(nb, lx, ly, player_clients, board, Mi, Mj, socket_server, server, list_clients, dict_clients):
	""" run_phasis2(nb, lx, ly, player_clients, board, Mi, Mj, socket_server, server, list_clients, dict_clients) -> Player.PlayerServer instance, for the winner.
	Mail Loop for the game."""
	NB_CLIENT = len(player_clients)	# have to be ==nb
	assert(NB_CLIENT == nb)
	ANSIColors.printc("""\n\n
	/phasis 2/ <green>Bomberman Server <u>is still listening<U> correctly on the network : <neg>%s:%i<Neg>...<white>
	/phasis 2/ <neg><green>Bomberman Server is launching step #2 .<Neg><white>
	""" % server)

	print_help()

	# Initialization of the clock frequency.
	clock = pygame.time.Clock()
	ANSIColors.printc("/pygame/ <INFO> <green>The game will make %i loops each seconds<white> (this control is made with clock.tick())" % CLOCK_FREQUENCY)

	# Print the parameters for the game.
	ANSIColors.printc("""
	/parameters/ The game is launching with those parameters : nb, lx, ly, Mi, Mj = %s.
	/parameters/  List of players : %s.
	/parameters/  Constants for the game : BREAK_ON_WALL, NB_BOMB_MAX_ALLOW, force_default, pv_Init = %s.
	/parameters/  And then the board :
	""" % (str( (nb, lx, ly, Mi, Mj) ), str(player_clients), str( (BREAK_ON_WALL, NB_BOMB_MAX_ALLOW, force_default, pv_Init)) ) )
	# print_clear("\n" + str(board))  # FIXME do not print the board constantly ?
###############################################################################
	# To count the nb of turns, and the time.
	nb_turn = 1
	time_before = time.time()
	time_before2 = time.time()

###############################################################################
	#: Start parallelization
	NB_THREADS = 3
	thread.start_new_thread( toggle_explosion, (board, player_clients, clock), \
		{'MAKE_DESTROY':True, 'FORCE':True, \
		'print_on_all':print_on_all, \
		'list_clients':list_clients, 'origin':("[%s:%i]" % server), \
		'num_thread':NB_THREADS} )
###############################################################################
	if USE_PICKLING:
	 save_current_game((nb, lx, ly, board), "nb, lx, ly, board", fn=savegame)
	# Going in the main loop.
	keep = True
	try:
	 while keep and (len(player_clients)>1):
		#: To ensure that the printing is not too quick.
		clock.tick(CLOCK_FREQUENCY)
		time_now = time.time()
		if ((time_now - time_before2) > 1):	# (5.0/CLOCK_FREQUENCY) ):
			# FIXME do not print the board constantly ?
			print_clear("\n" + str(board) + "\n PVs for players :\n")
			print_pvs_player(player_clients)
			time_before2 = time_now
			if USE_PICKLING:
			 save_current_game((nb, lx, ly, board), "nb, lx, ly, board", fn=savegame)
	 	keep = True
	 	# To be sure we are not keeping an already dead player alive...
	 	###############################################################
	 	for tmp_pl in player_clients:
	 		if tmp_pl.pv <= 0:
		 	 	ANSIColors.printc('/dead/ Player <neg>%s:%i<white> <red><u>is dead : it is not right that I found him here...<U><white>' % ( str(tmp_pl), tmp_pl.id ))
		 	 	try:
		 	 		ANSIColors.printc('/dead/ Player <neg>%s:%i<white> <red><u>is dead : I\'m deleting him from my variables...., at index %i for the lists, and on the spot %i,%i for the matrix...<U><white>' % ( str(tmp_pl), tmp_pl.id, tmp_pl.id, tmp_pl.x, tmp_pl.y ))
			 		indice_client = player_clients.index(tmp_pl)
			 	 	dict_clients.remove( dict_clients[indice_client] )
			 		list_clients.remove( list_clients[indice_client] )
			 		player_clients.remove(tmp_pl)
			 		board[tmp_pl.x, tmp_pl.y].players.remove(tmp_pl)
			 	except:
			 		ANSIColors.printc("/dead/ <warning> <neg> I failed badly when I tried to remove this player <neg>%s<Neg>. Cause=%s !" % (str(tmp_pl), str(sys.exc_info()[1])))
	 	###############################################################
		if ((time_now - time_before) > TIME_EXPLOSION ):
			if verb2:	ANSIColors.printc("<white>/time/ Time lapse between now and the last tic : <neg>%f<Neg>." % (time_now - time_before))
			time_before = time_now
			nb_turn += 1
			if verb:	ANSIColors.printc("/t/ <blue>New turn !<white> Number of turn : <neg>%i<Neg>." % nb_turn)
	 	#: Listening...
		list_listen = list_clients + [socket_server, sys.stdin]
		list_in, useless1, useless2 = select.select(list_listen, [], [])
		# Here is the trick with *select.select*.
		for socket_in in list_in:
###############################################################################
		 # If the administrator is using the keyboard to send message to the clients,
		 #  for example to simplify communications
		 if(socket_in is sys.stdin):
		   readstr = sys.stdin.readline()
		   if action_on_readstr(readstr, list_clients, dict_clients, player_clients, server, lx, ly, nb):
		    ANSIColors.printc(""" This is a list of new commands. You can test them !
 * <neg>GAME_OVER(id)<Neg>	-- To announce the <green><neg>winner<Neg> of the game<white> (id is between 0 and %i),
 * <neg>PLANT_BOMB(i,j)<Neg>	-- To plant a <green>new bomb at position (i,j)<white> (i is between 0 and %i, j is between 0 and %i),
 * <neg>BLOW_BOMB(i,j,radius)<Neg>	-- To make the bomb at positon (i,j) <green>blow<white> (radius is the New York distance of explosion, default is %i),
 * <neg>MOVE_PLAYER(id,i,j)<Neg>	-- To <green>move the player number=id to the position (i,j)<white>.
""" % (nb, lx, ly, force_default) )
		    continue
		   NB_CLIENT = len(dict_clients)	# update in case administrator used the command \\kill.
		   if len(readstr) == 0:
		   	ANSIColors.printc('/9/ Server sends <u>an EOF signal<U> : <red>server is closing<white> ...')
		   	raise KeyboardInterrupt
		   ANSIColors.printc('/1/ Server <blue>%s:%i <green>sends a message<white>.' % server)
		   origin = 'Server[%s:%i]' % (server)
		   print_on_all(readstr, list_clients, origin)
		 # If it's not from the administrator.
		 # In this context, that **don't** mean necessarily a new player (because it is **also** a chat room)
		 elif not(socket_in is socket_server):	# No new clients in second phasis.
###############################################################################
		  	file_in = socket_in.makefile()
		  	# One of the already connected client is sending a message
		  	# Get the variable representing the player
		  	try:
		  	 address_client = socket_in.getpeername()
		  	 indice_client = dict_clients.index(address_client) # WARNING here.
		  	 player = player_clients[indice_client]
		  	except socket.error as eee3:
		  	 ANSIColors.printc("""
<warning> <magenta><neg>  I'm reading an already closed connection : this is bad !<Neg> I'm closing now...
<warning> Maybe the last client is already disconnected !<white>
""")
		 	 list_clients.remove(socket_in)
		 	 if not list_clients:
		 	 	ANSIColors.printc("<warning> <red>I have no client connected : ciao !<white> Exit code=6...")
		 	 	os._exit(6)
		 	 continue	# FIXME ?
		  	# Inform who is being listened
		 	ANSIColors.printc('\n\t/=/ Listening to client <blue>%s<white>, number <red>%s<white> :' % (str(address_client), str(1+indice_client)))
		 	ANSIColors.printc('/=/  In the game, this client is the player : %s' % str(player))
		 	# Read a message from one of the available client
		 	readstr = file_in.readline()
		 	if (len(readstr)>0) or (player.pv <= 0):
		 	 ANSIColors.printc('/1/ Client <blue>%s:%i <green>sends a message<white> :' % address_client)
		 	 ANSIColors.printc("/in/ He send <neg>%s<Neg>. I am going to use it..." % readstr)
		 	 origin = 'Server[%s:%i]' % server
		 	 if INFORM_CLIENTS:	# FIXME just be sure.
			 	 list_clients.remove(socket_in) # WARNING here.
			 	 print_on_all(readstr, list_clients, origin)
			 	 list_clients.append(socket_in) # WARNING here.
			 	 ANSIColors.printc('/1/  His message have been printed on <green>all %i other client\'s stdout<white>.' % (len(list_clients) - 1))
		  # readstr is now a message from the server.
###############################################################################
			 # Update the current game with those orders.
			 # the unpack functions are gameover_of_str, posplantbomb_of_str, blowbomb_of_str, moveplayer_of_str
			 try:
				  i, j = player.x, player.y
				  Mi, Mj = i, j
#:				  keep_parsing = True
				  if verb2:	ANSIColors.printc("\n/in/<INFO> Beginning parsing '<neg>%s<Neg>'." % readstr)
#:				  while keep_parsing and readstr:
				  # FIXME in the semantics, we said *one message, one '\n'*.
				  if readstr:
				   if readstr[ -1 ] == '\n':
				    readstr = readstr[: len(readstr) - 1 ]	# Delete the last '\n'
				  #############################################################
				   if readstr[:10] == 'PLANT_BOMB':
				 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a PLANT_BOMB message." % readstr)
				 	if board[i, j].bomb:
					 if verb: ANSIColors.printc("/!/ <u><red>This is not allowed<U><black>, you cannot drop a second bomb <u>here<U>.<white>")
					elif player.nb_bomb >= NB_BOMB_MAX_ALLOW:
					 if verb: ANSIColors.printc("/!/ <u><red>This is not allowed<U><black>, you cannot drop a new bomb on the board (max allow : %i).<white>" % NB_BOMB_MAX_ALLOW)
					else:
					 board[i, j].bomb = player.drop() # default value.
					 print_on_all( ParseMessageOut.str_of_posplantbomb(i, j) , list_clients, origin)
					 if verb: ANSIColors.printc("/out/ <green> An order have been sent to <neg>plant<Neg> a new bomb (=%s) at the spot <neg>%i,%i<Neg>.<white>" % ( str(board[i,j].bomb), i, j ))
				  #############################################################
				   if readstr[:9] == 'MOVE_LEFT':
				 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a MOVE_LEFT message." % readstr)
				 	if (j>0) and board[i, j-1].is_free():	j = max(0,j-1)
				  #############################################################
				   if readstr[:10] == 'MOVE_RIGHT':
				 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a MOVE_RIGHT message." % readstr)
				 	if (j<ly-1) and board[i, j+1].is_free():	j = min(ly-1,j+1)
				  #############################################################
				   if readstr[:7] == 'MOVE_UP':
				 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a MOVE_UP message." % readstr)
				 	if (i>0) and board[i-1, j].is_free():	i = max(0,i-1)
				  #############################################################
				   if readstr[:9] == 'MOVE_DOWN':
				 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a MOVE_DOWN message." % readstr)
				 	if (i<lx-1) and board[i+1, j].is_free():	i = min(lx-1,i+1)
				  #############################################################
				   else:
#:				  	keep_parsing = False
				 	if verb:	ANSIColors.printc("""<question>\t/in/<INFO> I can't interpret [<neg>%s<Neg>] as any messages I can understand...""" % readstr)
				   # Now log all this.
				   if board[i,j].wall:
					if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is a <u>wall<U> in the wanted spot." % (player, Mi, Mj, i, j))
					continue
				   elif board[i,j].bomb:
					if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is a <u>bomb<U> in the wanted spot." % (player, Mi, Mj, i, j))
					continue
				   elif (i == Mi) and (j == Mj):
					if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is the natural limitation of the board." % (player, Mi, Mj, i, j))
					continue
				   elif board[i,j].is_free():
					ANSIColors.printc("/!/ <green>Player %s<white> is moving from (%i,%i) to (%i,%i)." % (player, Mi, Mj, i, j))
					try:
						board[player.x, player.y].players.remove(player)
						player.move(i, j)
						board[player.x, player.y].players.append(player)
						print_on_all( ParseMessageOut.str_of_moveplayer(player) , list_clients, origin)
						if verb: ANSIColors.printc("/out/ <green> An order have been sent to <neg>plant<Neg> a new bomb (=%s) at the spot <neg>%i,%i<Neg>.<white>" % ( str(board[i,j].bomb), i, j ))
						continue
					except ValueError as useless1:
						ANSIColors.printc("""
<warning> <red>I just tried to remove the player %s (repr. %s) from the spot %i,%i.
<warning> <red>This spot is %s (and contains this list of player %s).
""" % ( str(player), repr(player), player.x, player.y, str(board[player.x, player.y]), str(board[player.x, player.y].players) ))
#:						keep_parsing = False
				   else:
					if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i)." % (player, Mi, Mj, i, j))
					continue
			 except:
			 	raise	#FIXME be sure ?
###############################################################################
		        else: # nothing readed from the client : he logged out or exited
		         if player.pv <= 0:
		 	 	ANSIColors.printc('/dead/ Player <neg>%s<white> <red><u>died<U><white> !' % str(player))
		         else:
		 	 	ANSIColors.printc('/5/ Client <green>%s:%i<white> <red><u>logged out<U><white> !' % address_client)
		 	 # Removing the client/player from the data lists
		 	 NB_CLIENT = NB_CLIENT - 1
			 ANSIColors.xtitle(".: Phasis #2 of Bomberman Server %s:%i; playing with %i players) :." % (server[0], server[1], NB_CLIENT))
		 	 dict_clients.remove(address_client)
		 	 list_clients.remove(socket_in)
		 	 player_clients.remove(player)
		 	 # Informing about this logging out
		 	 ANSIColors.printc('/logged out/  He <red>was<white> the player : %s (repr. = <neg>%s<Neg>).\n' % (str(player), repr(player) ))
		 	 # FIXME, to respect the formal semantics, it is better to delete it.
		 	 # If you want to inform all the still connected client that he quit ?
		 	 if INFORM_CLIENTS:
		 	  print_on_all('/client out/ Client %s logged out !\n\t/5/  He was the player : %s (repr. = %s).' % ( ("%s:%i" % address_client), str(player), repr(player) ), list_clients, origin = 'Server[%s:%i]' % (server) )
###############################################################################
	except:
		ANSIColors.writec("""
/END Phase 2/ <red>Server is closing<white>, because <red><neg>%s<Neg><white> !""" % str( sys.exc_info()[1] ))
		raise
	# Here : the while loop is concluded, the except might not have been executed.
	print "\n", board
	if not player_clients:
		ANSIColors.writec("""\n
/END Phase 2/ <red>Server is closing<white>, because <red><neg>he have no valid client<Neg> to propose as a winner....<white> !""")
		sys.stderr.flush()
		sys.stdout.flush()
		os._exit(9)
	return player_clients[0], list_clients	# Last player on top !

###############################################################################
##### Last stuff : used the command line to know what to do #####

if __name__ ==  '__main__':
	import ParseCommandArgs
	#: This variable is the preprocessor, given to description and epilog by ParseCommandArgs,
	#:  * erase: to print with no colors.
	#:  * sprint: to print with colors.
	preprocessor = ANSIColors.sprint if ANSIColors.ANSISupported else ANSIColors.erase
	#:preprocessor = __builtin__.str, if you want to *see* the balises.
	#: Generate the parser, with another module.
	parser = ParseCommandArgs.parser_default(\
		description = '<green>BombermanServer <red>module<reset> and <blue>script<reset>.',\
		epilog = """\n\
<yellow>About:
======<reset>
 This is the server for a <neg>multiplayer Bomberman Game<Neg> (MPRI 1-21 projet, 2013).
 This project is hosted here <u>https://bitbucket.org/vcohen/projet_reseau<U>.
 The doc for this project can be find here <u>http://perso.crans.org/~besson/publis/Bomberman/_build/html/<U>.""", \
		version = __version__, date = __date__, author = __author__, \
 		preprocessor = preprocessor)
	#: Description for the part with '--file' and '--generate' options.
	group = parser.add_argument_group('About network connection', preprocessor("""\
<b>This program <u>is a server<U>. So, it will listen on an *address* and on a *port* <reset>
"""))
	#: Remember that action can be used to many things.
	group.add_argument("-s","--server", help = preprocessor("""The address of the server.
<u>Examples<U>:
 * <yellow>'127.0.0.1'<reset> : to listen only on the local loop (usefull for test if you don't have a network connection),
 * <yellow>'0.0.0.0'<reset> : to listen on all interfaces (usefull to be an *open* server),
 * <yellow>'bomberman-server.crans.org'<reset> : to listen only on a fixed loop, if you have a fix DNS name.
     <green> This one is the best, to be a simple-to-remember server name !<reset>""")) #:, required = True)
	group.add_argument("-p","--port", type = int, help = "The port on which the server will listen for clients (ex. 9312, or 12882).\n\t This port *have* to be an open port on your machine.") #:, required = True)
	#: A group for handling save restore
	group = parser.add_argument_group('Saving and restoring previous sessions', preprocessor("""\
<b>This program <u>save his state<U> (the board, list of players etc) during the session<reset>,
 so if there is a problem, the last valid state of the game will be kept.
And this program can of course restore such a state, to restart from where it was !
"""))
	group.add_argument('-l', '--load', help = preprocessor(""" If present, the server will try to restart a previously close session. Default is not."""), action = "store_true")
	group.add_argument('-f', '--file', help = preprocessor(""" Try to load the savegame from the file FILE if possible, launch a <red>new one<reset> if not."""))
	group.add_argument('--save', help = preprocessor(""" If present, the server will try to save his current session to the file SAVE. Default is none. To enable this <red>experimental functionnality<white>, <neg>change USE_PICKLING to True in ConfigServer.py<Neg>."""))
	#: A group for parametrize the map -x -y -N for lx, ly, nbmax
#:	group = parser.add_argument_group('Parametrize the map (by now, **do not use it**) :', preprocessor("""\
#:<b>The game <u>run on a map<U> (also called the board)<reset>,
#: which is mainly parametrized by his length : lx,ly; and the max number of player in it.
#: Currently, the map is very simple, and LX,LY should be 6,6; 8,8 or 10,10.
#:"""))
#:	group.add_argument('-x', '--lx', type = int, help = preprocessor(""" Force the map to take length LX over x axis."""), default = LX_CST)
#:	group.add_argument('-y', '--ly', type = int, help = preprocessor(""" Force the map to take length LY over y axis."""), default = LY_CST)
#:	group.add_argument('-N', '--nbmax', type = int, help = preprocessor(""" Force the map to take less than NBMAX players."""), default = NB_PLAYER)
	#: The parser is done,
	#: Use it to extract the args from the command line.
	args = parser.parse_args()
###############################################################################
	ANSIColors.xtitle(".: Bomberman Server, v%s, made by %s :." % (__version__, __author__))
	print_clear(".: Welcome in the Bomberman Server, v%s, made by %s Last modification %s :." % (__version__, __author__, __date__))
	# Use those args.
	verb = (args.verbose > 1) or verb	# Default = True
	verb2 = (args.verbose > 2) and verb2	# Default = False
	if verb2:	print(" Processing command line args...")
	print("About verbosity: verb=%s, verb2=%s." % (verb, verb2))
	# Print with ANSI escape code for colors if possible
	ANSIColors.ANSISupported = (not(args.noANSI) and ANSIColors.ANSISupported) or args.ANSI
	# Disable all escape codes for color to be generated
	if not(ANSIColors.ANSISupported):
		ColorOff()
	else: ColorOn()	#: Defined in Constants.
	ANSIColors.printc("/!/ ANSI escape code for colors supports = <green>%s<white>." % ANSIColors.ANSISupported)
	# Print with non ASCII caracters for boxes if possible
	Board.UTFSupported = not(args.noUTF) and Board.UTFSupported
	ANSIColors.printc("/!/ UTF escape code for boxes supports = <green>%s<white>." % Board.UTFSupported)

	# Set the server and the port
	server = args.server if args.server else SERVEUR_INIT
	port = int(args.port) if args.port else PORT_INIT
	# Choose a file to save.
	if args.save:
		savegame = args.save
	else:
		savegame = filename_pickling
	# Set the parameter of the map
	try:
		lx = max(1, min(lx_Max, int(args.ly))) if args.lx else LX_CST
		ly = max(1, min(ly_Max, int(args.lx))) if args.ly else LY_CST
		nbmax = max(1, min(nbmax_Max, int(args.nbmax))) if args.nbmax else NB_PLAYER
	except Exception as e:
		lx, ly, nbmax = LX_CST, LY_CST, NB_PLAYER
	 	if verb2 and verb:
	 		ANSIColors.printc("/init/ <u><red>Failed to find the lx,ly,nbmax<reset><white> in command line args. Cause : <neg>%s<Neg>." % str(e))
###############################################################################
	board = None
	#: If a save game is available, load it !
	if args.load:
		 ANSIColors.printc("/load/ <yellow>Trying to load<reset><white> \tthe game from a save file<reset><white>...")
		 try:
			 if args.file:
			  nbmax, lx, ly, board = ParseMessageIn.try_unpickling("(nbmax, lx, ly, board)", fn = args.file)
			 else:	# use the default value !
			  nbmax, lx, ly, board = ParseMessageIn.try_unpickling("(nbmax, lx, ly, board)")
			 for i, j, spottmp in board:
			   board[i,j] = copy.copy(spottmp)
			   board[i,j].players = copy.copy(spottmp.players)
			 ANSIColors.printc("/load/ <green>Succeed to load<reset><white> \tthe game from a save file<reset><white>...")
			 ANSIColors.printc("""
		/load/ I picked up those parameters : <neg>lx=%i,ly=%i,nb=%i<Neg>
		/load/ And the following board:
		%s
		""" % ( lx, ly, nbmax, str(board) ))
		 except Exception as e:
			 ANSIColors.printc("/load/ <u><red>Failed to load<reset><white> \tthe game from a save file...\n\t/load/ Cause : %s" % e)
	else:
###############################################################################
	 #: Otherwise, new parameters will be recreated.
	 if verb2:
		 e = "<yellow>-l neither --load found if the argument.<reset>"
		 ANSIColors.printc("/load/ <u><red>Failed to load<reset><white> \tthe game from a save file...\n\t/load/ Cause : %s" % e)
###############################################################################
	try:
	 ANSIColors.printc("/init/ <yellow>The game will run on the server : (%s:%i)<reset><white>" % (server, port))
	 if USE_NOTIFY:	ANSIColors.notify("Phasis #1 of Bomberman Server is going to start (you are listening on %s:%i for %i clients)" % (server, port, nbmax), obj=".: Bomberman Server :.", icon="bomberman.gif" )
	 ANSIColors.xtitle(".: Phasis #1 of Bomberman Server %s:%i :." % (server, port))
	 nbmax, lx, ly, player_clients, board, Mi, Mj, socket_server, list_clients, dict_clients = run_phasis1(lx = lx, ly = ly, nb = nbmax, server = (server, port), board=board)
	 # The game is initialized
###############################################################################
	 #: Launch the game
	 if USE_NOTIFY:	ANSIColors.notify("Phasis #2 of Bomberman Server is going to start (you are still listening on %s:%i; playing with %i players)" % (server, port, nbmax), obj=".: Bomberman Server :.", icon="bomberman.gif")
	 ANSIColors.xtitle(".: Phasis #2 of Bomberman Server %s:%i; playing with %i players) :." % (server, port, nbmax))
	 player_winner, list_clients = run_phasis2(nbmax, lx, ly, player_clients, board, Mi, Mj, socket_server, (server, port), list_clients, dict_clients)
	 print_on_all( ParseMessageOut.str_of_gameover(player_winner), list_clients, origin = 'Server[%s:%i]' % (server, port))
	 ANSIColors.printc("""
/end of the game/ <INFO> I just sent the last message to all connected clients, to inform them that the winner is :
<neg>%s<Neg> (repr. as : %s)
""" % ( str(player_winner), repr(player_winner) ))
	 ANSIColors.printc("<neg> Going asleep for 1.0 seconds...<Neg>")
	 time.sleep(1.0)
###############################################################################
	except KeyboardInterrupt:
	 ANSIColors.printc("""<warning> <red> The game is done<default>.
<warning>  I <yellow>guess<default> you closed it, probably with an EOF (<black>Ctrl+D<default>) or a SIGTERM signal (<black>Ctrl+C<default>).
<warning>  <green>Feel free to send any comment, suggestion or bug : <white> <u><neg>%s<reset>.""" % (__email__))
	 sys.stdout.flush()
	 sys.stderr.flush()
	 os._exit(1)
	except:
	 ANSIColors.printc("<ERROR> <red> The game is done<default>. I received the last exception <neg>%s<Neg>." % str(sys.exc_info()[1]))
	 sys.stdout.flush()
	 sys.stderr.flush()
	 raise
###############################################################################
	ANSIColors.printc("""<green><neg> The game is done<white>, and I didn't receive any unhandled exceptions in the end<reset> (good job !)...
<neg>The second phasis seems to give me this player as a winner<neg> : %s.
I'm quiting nicely now... <green>Feel free to send any comment, suggestion or bug : <white> <u><neg>%s<reset>.""" % ( player_winner, __email__ ) )
	os._exit(0)

###############################################################################
# DONE.
