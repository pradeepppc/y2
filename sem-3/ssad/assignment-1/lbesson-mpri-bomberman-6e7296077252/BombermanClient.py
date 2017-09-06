#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
 This program is the **client** for our *Bomberman multiplayer game*.

Example
-------
  This show how the **textual mode** *looks like during the game* :

.. image:: images/exempletextual_client.png
   :scale: 100 %
   :align: center

How to ?
========

 The program accept some *command line* options.

 The simpliest way to use it is:
  **$ ./BombermanClient.py --server bomberman.crans.org --port 12885**
 This will launch the client on the *server* **bomberman.crans.org** (assuming that a server is already launched there), on the *port* **12885** (idem, it **have** to be the listening port of the server).

Customization of the player
---------------------------

 You can also specify two parameters to your *player* :
  1. your **pseudo** : with the *option* --pseudo.
     A pseudo can be as long as you want (but it will be cut at 32 caracters), can contain *UTF* caracters, **but no spaces or specials caracters**.
     The pseudo is used for communication, to identify yourself easily; and for *textual mod* (the first letter will be displayed on the board)
  2. and your player's **color** : with the *option* --color.
     A valid color is one of black, red, green, yellow, blue, magenta, cyan or white.

 So, you can be *Luke Skywalker*:
  **$ ./BombermanClient.py --server bomberman.crans.org --port 12885 --pseudo Luke --color cyan**

PyRlwrap
---------

 The client *have* to be launched from the **command line**, and during the game the *stdin* (*i.e.* the keyboard) is listened.
  So you can send messages yo your server, directly from the command line.
  The script `PyRlwrap.py <PyRlwrap.html>`_ provide a **readline wrapper** for this command line interface. It brings:
   * shortcut, "a la Nano" (^A: begin line, ^E: end line etc);
   * history (Up & Down show previous message).

 You can launch the client with *PyRlwrap.py* like this (and be *Mario*) :
  **$ ./PyRlwrap.py ./BombermanClient.py --server 138.231.134.230 --port 9312 --pseudo Mario --color red**

Options for textual mod
-----------------------

 The following options can change how the *textual mod* looks like :
  * --noUTF : disabled *UTF* caracters for the board.
    And, **warning** for pseudos, if one begins with a *non-ascii* caracter, the *id* of the player is used (an integer, between 0 and the number of player -1).
  * --noANSI or --ANSI : force to disable or enable the colors.
    Normally, you don't have to use them, because the `ANSIColors module <ANSIColors.html>`_ can detect *cleverly* if colors are supported.
    (_Note:_ this have been tested with **Linux**, **Cygwin**, but not with **Mac OS X**)

Options for graphical mod
-------------------------

 The following option(s) can change how the *graphical mod* looks like :
  * --music or --nomusic : try to enable the music or force to not use it.
  * --soundeffect or --nosoundeffect : try to enable the music effects (when a bomb blow) or force to not use it.

 For more details about *graphical mod*, cf `the AffichPygame module <AffichPygame.html>`_.

About
=====

Getting some help
-----------------

 This program uses a *high-level* **command line** parser : `ParseCommandArgs <ParseCommandArgs.html>`_, based on *argparse* from the standard distribution.

 Therefore, the *help* for this program can be obtained simply with ::
  **$ ./BombermanClient.py --help**

 The *help* embed some colors, and it can be read through a pipe :
  **$ ./BombermanClient.py -h | less -r**

Choices
-------

 * For handling multi channels listening and sending in step 1 and 2, **thread.thread** is used.
    Both for the step 1 and 2.
 * The **syntax of messages** is :
    * explained in the `specification_slides.pdf <../../specification_slides.pdf>`_,
    * or in the module `ParseMessageIn <ParseMessageIn.html>`_,
    * or in the module `ParseMessageOut <ParseMessageOut.html>`_;
 * The **specification** of the game protocole is also detailed in the slides (and mainly it explains why **we use TCP**).


Warning
=======
.. warning::
   This script is not yet fully concluded.
   So, it might end badly on some untests behaviour.
   I ran many tests, but I can't ensure everything is all right...

TODOs:
======
 * Make the option '--nowindow' available (by now, it fails).
 * Make sure the winner player is well get from the last message.

TODOs ?:
=======
 * ? Conclude the parser (add --keys to parametrize the KeyBinding).
 * ? Implement the bonus system.
 * ? Make the music smoother.
 * ? Use a smart update for the sprites (and not recompute all each time).
"""

__author__='Lilian BESSON'	#: Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__email__='lilian.besson[AT]normale.fr'
__version__='1.3a'
__date__='mar. 19/02/2013 at 22h:48m:28s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
try:
	import os, sys, time
	__date__ = time.strftime("%a %d/%m/%Y at %Hh:%Mm:%Ss", time.localtime(os.lstat(sys.argv[0]).st_mtime))
	del os, sys, time
except:	pass

#1###############
# Usual Modules #
import socket, sys, thread, os, copy, time
#:import atexit, random

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import *	# Constants.py : default constants.
import Matrix		# Matrix.py : simple module to manipulate matrix, for the board.
import ParseMessageOut	# ParseMessageOut.py : pretty printing of data types, for exchange on the net.
import ParseMessageIn	# ParseMessageIn.py : parsing of data types, for exchange on the net.
import Player		# Player.py : implements the simple player system. (actions, representation etc)
import Board		# Board.py : two classes Board.Board and Board.State.
import Bomb		# Bomb.py : two classes Bomb.Bomb and Bomb.BombNoOwner.
import KeyBinding	# KeyBinding.py : implements the key binding.
from AffichPygame import *	# Brings pygame ! Mainly for music, keyboard reaction and graphical window.
del(main)	# Delete from AffichPygame

try:
	from ConfigClient import *
	if verb and verb2:
		print "The file %s have been loaded as a configuration file for the client." % 'ConfigClient.py'
		print "The client will use the profile named '%s'." % profile_name
	assert( CLOCK_FREQUENCY > 1.0 )
	assert( CLOCK_FREQUENCY < 60.0)
except:
	if verb and verb2:
		print "[ERROR] I failed when I tried to load the file %s as a configuration file for the server." % 'ConfigClient.py'

##############################
##### First net function #####

def create_socket_client(server = (SERVEUR_INIT, PORT_INIT)):
	""" Create a socket designed to be a client, and connect it to @server.
	Return a socket."""
	msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	msocket.connect(server)
	return(msocket)

##########################
##### User interface #####

# The help message, which can be printed to the user when invoking *'\\?'*
help_User = """
<green><u>Welcome in Bomberman client<U><white>, v%s.
	<blue>Wrote by %s, last version dated of %s.<white>
	Wrote in Python 2.7.3, using ANSIColors for colors in output messages.
	Reference page for this software is there : <u>https://bitbucket.org/vcohen/projet_reseau<U>.

<neg>You are connected to a Bomberman server,<Neg> using **TCP sockets**.
All messages enter from <green><u>here<U><white> will be broadcasted to all other connected clients,
 and <green><u>here<U><white> are broadcasted all messages from other clients (and from the master server).

The following <green>commands are implemented<white> :
	<neg>\\h, \\help, \\?<Neg>	:	print this help,
	<neg>\\whoami<Neg>		:	print the informations about you (address, port of server & client) and your player,
	<neg>\\out<Neg>		:	logout (act like Ctrl+D),
	<neg>\\list<Neg>		:	list of all messages (both sent and received.),
	<neg>NEW_PLAYER(%%s)<Neg>	:	change your pseudo.
	<neg>color=%%s<Neg>	:	change your color (to one of [<black>'black'<white>, <red>'red'<white>, <green>'green'<white>, <yellow>'yellow'<white>, <blue>'blue'<white>, <magenta>'magenta'<white>, <cyan>'cyan'<white>, 'white']).
""" % (__version__, __author__, __date__)

#######################################
#### Reaction to specials messages ####

def action_on_readstr(readstr, pl_client, List_ReceivedMessages=[], List_SentMessages=[], verb=False):
	""" Reaction to special message read from the keyboard !"""
	have_changed = False
	if readstr in ['\\h\n', '\\help\n', '\\?\n']:
		ANSIColors.printc("\n\t/whoami/ You are a Bomberman player (%s), represented as a Player.Player instance : <neg>%s<Neg>." % (str(pl_client), repr(pl_client)))
		ANSIColors.printc('/?/ <blue>Help : \\h or \\help or \\?<white>:')
		ANSIColors.printc(help_User)
		return True
	if readstr in ['\\whoami\n']:
		ANSIColors.printc("\n\t/whoami/ You are a Bomberman player (%s), represented as a Player.Player instance : <neg>%s<Neg>." % (str(pl_client), repr(pl_client)))
	  	return True
	if readstr in ['\\list\n', '\\messages\n']:
		 if 0<len(List_ReceivedMessages):
		   ANSIColors.printc("/list/ You received the following messages : %s." % str(List_ReceivedMessages))
		 else:
		   ANSIColors.printc("/list/ No messages have been received...")
		 if 0<len(List_SentMessages):
		   ANSIColors.printc("/list/ You sent the following messages : %s." % str(List_SentMessages))
		 else:
		   ANSIColors.printc("/list/ No messages have been sent...")
		 return True
	if readstr in ['\\out\n']:
		pl_client.close()
		ANSIColors.printc("""
/\\out/ <warning> <red>Client is closing<white>, because <yellow>client wants to, with the \\out command !<white> (this is a very extrem way to quit : no cleaning and no messages to your server...)""")
		os._exit(5)	# Hard exit ! XXX
	try:
 	  # message pseudo=%s
 	  pl_client.pseudo = ParseMessageIn.newplayer_of_str(readstr[:len(readstr)-1])[:32]
	  ANSIColors.printc('/scanf/  <green>Success<white> ! You, the player <blue>%s<white>, have changed your <u>pseudo<U> to %s (and now, he is %s).' % (pl_client.info_connection, pl_client.color, pl_client))
	  have_changed = True
	except Exception as e1:
	  try:
 	   # message color=%s
 	   pl_client.color = ParseMessageIn.newcolor_of_str(readstr[:len(readstr)-1])[:32]
	   ANSIColors.printc('/scanf/  <green>Success<white> ! You, the player <blue>%s<white>, have changed your <u>color<U> to %s (and now, he is %s).' % (pl_client.info_connection, pl_client.color, pl_client))
	   have_changed = True
 	  except Exception as e2:
	    if verb: ANSIColors.printc('/scanf/  <red>Fail<white> : the message was not a command. (e1 = %s; e2 = %s)' % (e1, e2))
 	# Maybe the value of the player have been changed.
 	if have_changed:
	 ANSIColors.printc('/3/  You are currently represented as the player %s (repr %s).\n' % (str(pl_client), repr(pl_client)))
	return False

######################################
##### Initialization for the game ####

def initGame(lx=LX_CST, ly=LY_CST, nb=NB_PLAYER):
	"""initGame(lx=LX_CST, ly=LY_CST, nb=NB_PLAYER) -> (nbmax, lx, ly, pl, board, Mi, Mj)
	 Creating all Game variables.
	 Here there is no random in the map yet."""
	# Pseudos and colors for players
	pseudos, colors = pseudos_colors(nb)
	# Start position
	Mi, Mj = start_position(2, lx, ly, nb)
	nbmax=len(pseudos)
	pl=list()
	for i in range(nbmax):
		pl.append(Player.PlayerServer(pseudo=pseudos[i], color=colors[i]))
	# Convert players to state
	spl=list()
	for i in range(nbmax):
	 spl.append(Board.State(wall=False, players=[pl[i]]))
	# Initialize the board
	board=Board.Board(Board.empty, lx, ly)
	for i, j, spottmp in board:
	  board[i, j]=copy.copy(spottmp)
	  board[i, j].players=copy.copy([])
	for i in range(nbmax):
		pl[i].move(Mi[i],Mj[i])
		board[Mi[i],Mj[i]] = spl[i]
	#: For Bonuses.
#:	for i, j, spottmp in board:
#:	  if not(spottmp.players) and (PROBA_BONUS > random.random()):
#:		 board[i, j].bonus = Bonus.Bonus( random.choice ( Bonus.List_available_bonuses ) )
#:		 print "New bonus : %s." % (repr(board[i,j].bonus))
	return (nbmax, lx, ly, pl, board, Mi, Mj)

###################################################
#### IRC client for the step 1 (wainting room) ####

def run_client(msocket, server, player, PRINT_ALL_MESSAGE = PRINT_ALL_MESSAGE, double_thread=False):
	"""run_client(msocket, server, player, PRINT_ALL_MESSAGE = PRINT_ALL_MESSAGE, double_thread=False) -> player, nbmax0, lx0, ly0, pl0, board0, Mi0, Mj0, List_ReceivedMessages, List_SentMessages

	An infinite loop over the @msocket, which have to be a client socket assumed te be connected with @server (just used to print some usefull informations).
	Concurrently, read from stdin on client and write on stdout on server, and read on stdin on server and write on stdout on client. Use thread.

	If *PRINT_ALL_MESSAGE*, the client print all messages with a pretty workaroung.

	Moreover, it begins the construction of the board, and wait for more informations about it from the server.
	 When this phasis is conclude, create the board (and the others variables) and returns it.

	*double_thread* is just an experiment about two additionnal threads for the listening part.
	"""
	ANSIColors.printc("/0/ <blue>Trying to initialize the game variables<white>, and the server is %s:%i..." % server)
	nbmax0, lx0, ly0, pl0, board0, Mi0, Mj0 = initGame() # lx,ly,nbmax use constants values.
	board0.mat.box = Matrix.boxnoASCII if Board.UTFSupported else Matrix.boxASCII
	ANSIColors.printc("/0/ <blue>Game variables :<white>, %s." % str((nbmax0, lx0, ly0, Mi0, Mj0)) )
	print "\n", board0
	# For the connection
	msocket_name = ("%s:%i" % msocket.getsockname())
	server_name = ("%s:%i" % server)
	mfile = msocket.makefile()

	# For the IRC session.
	NB_THREADS = 0
	List_ReceivedMessages = []	# List of received messages.
	List_SentMessages = []		# List of sent messages.

	# Definition of the function we want to parallelize
	def read_write_inverse(sin, sout, client_to_server, board0, pl0, player, nsin = "sin", nsout = "sout", num_thread = 0):
		 """ Read input message from @sin and print them to @sout.
		@nsin and @nsout are string descriptors to print usefull informations about exchanged messages.
		The Boolean @client_to_server is used to print >> in the beginning of client input lines, and << in output.
		 """
		 ANSIColors.printc("\n\t/read_write_inverse/ <neg>Thread number %i<Neg> : initialized. Reading from %s, writing to %s..." % ( num_thread, nsin, nsout ))
		 sys.stdout.flush()
		 try:
		   while 1:
			 readstr = sin.readline()
			 if client_to_server:
			 	 if len(readstr)>0: List_SentMessages.append(readstr)
				 result_action = action_on_readstr(readstr, player, List_ReceivedMessages, List_SentMessages)
				 if result_action:
					 ANSIColors.printc("/command phasis 1/ <INFO> well executed !<white>")
					 continue
			 else:
			 	 if len(readstr)>0: List_ReceivedMessages.append(readstr)
			 	 if readstr[:10]=='GAME_START':
			 	  ANSIColors.printc("/in run_client/ <magenta> Trying to update the board<white>, with the following message :\n<neg>%s<Neg>. I'm starting....." % readstr)
			 	  try:
#:			 	  	ParseMessageIn.board_and_player_of_str(board0, pl0, player, readstr[0:len(readstr)-1], verb=verb2)
			 	  	ParseMessageIn.board_and_player_of_str(board0, pl0, player, readstr)
			 	  	#, verb=verb2)
			 	  except:
			 	  	ANSIColors.printc("/in run_client/ <red> Failed to update the board<white>, with the following message :\n<neg>%s<Neg>. I'm starting.....\n<default> I received this exception : <neg>%s<Neg>." % (readstr, str(sys.exc_info()[1])) )
			 	  raise Exception("/end run_client/ A valid map have been received : now the phasis #1 is done.")
			 # Handle if server or client is closing
			 if not(readstr):
	 			ANSIColors.printc("/%s/<INFO> <yellow>I read an empty string (that means from a closed connection) <white>...." % "in" if client_to_server else "out")
	 			sys.stdout.flush()
	 			sys.stderr.write("Communication (%s) is closing... The game is done !" % ("in" if client_to_server else "out"))
	 			os._exit(5)
	 			# FIXME
#:			 	raise Exception("Communication (%s) is closing..." % ("in" if client_to_server else "out"))
			 if PRINT_ALL_MESSAGE and (readstr[0]!='\n' if len(readstr)>0 else True):
			  if client_to_server:
			   ANSIColors.printc('/out/ Message [<yellow>%s<white>] read from <blue>%s<white>, sent to the server...' % (readstr, nsin))
			  else:
			   ANSIColors.printc('/in/ Message [<yellow>%s<white>] read from <blue>%s<white>,' % (readstr, nsin))
			  #: We remove the last caracter to avoid printing the last \n
			  sys.stdout.flush()
			 if client_to_server:
			  sout.write(readstr)
			 sout.flush()
		 except:
		 	 e = sys.exc_info()[1]
			 if 1<len(List_ReceivedMessages):
			   ANSIColors.printc("/list/ You received the following last message : %s." % str(List_ReceivedMessages[len(List_ReceivedMessages) - 1]))
			 if 1<len(List_SentMessages):
			   ANSIColors.printc("/list/ You sent the following last message : %s." % str(List_SentMessages[len(List_SentMessages) - 1]))
		 	 ANSIColors.printc("/run_client/ Phasis #1 stoped, because I received the exception e=%s." % str(e))
			 if client_to_server:
				raise Exception('/run_client1/ Phasis #1 stoped, because server closed !')
			 else:
			 	try: len(readstr)
			 	except: raise Exception('/run_client1/ Phasis #1 stoped, because client wants to<white> (^C or process kill by another way) !')
				raise Exception('/run_client1/ Phasis #1 stoped.')
				# , because reads an EOF signal (maybe you type ^D, or the server could be dead, or he decide to kill the connection, for example with the \\kill command)!
		 	 raise
	## END of the function we want to parallelize.
	####################################################
	try:
	 ANSIColors.printc("/0/ <blue>Connection seems to be <green><u>well<U><blue> established<white> with the server <green><u>%s<U><white>," % server_name)
	 # Send the color.
#:	 if player.send(ParseMessageOut.str_of_newcolor(player), True):
#:	 	ANSIColors.printc("/out/ <blue>You correctly sent your color<reset> (<%s>%s<white>) to the server <green><u>%s<U><white>," % (player.color, player.color, server_name))
	 ANSIColors.printc("/0/ You are identified as the client <green><u>%s<U><white>." % msocket_name)
	 # Announce that I used threads.
	 ANSIColors.printc("/?/ Enter <blue>\\?<white> for <u>more help<U>. <neg>Start parallelization with %s other thread%s.<Neg>" % ( ("2" if double_thread else "1"), ("s" if double_thread else "") ))
	 #: Start parallelization
	 NB_THREADS += 1
	 mythread = thread.start_new_thread(read_write_inverse, (sys.stdin, mfile, True, board0, pl0, player, ("stdin ("+msocket_name+")"), server_name, NB_THREADS))
	 if verb2:	ANSIColors.printc("/thread:read_write_inverse/ Launching a thread, identified with %s." % str(mythread))
	 sys.stdout.flush()
	 NB_THREADS += 1
	 if double_thread:
	 	mythread = thread.start_new_thread(read_write_inverse, (mfile, sys.stdout, False, board0, pl0, player, server_name, ("stdout ("+msocket_name+")"), NB_THREADS))
	 	ANSIColors.printc("/thread:read_write_inverse/ Launching a thread, identified with %s." % str(mythread))
	 	sys.stdout.flush()
	 else:
	 	#: This one is not threaded.
	 	read_write_inverse(mfile, sys.stdout, False, board0, pl0, player, server_name, ("stdout ("+msocket_name+")"), NB_THREADS)
	except:
	 e = sys.exc_info()[1]
	 ANSIColors.printc("/end run_client/ <red>Failure<yellow> the phasis #1 died<white>. Error : %s." % str(e))
	 ######################
	 # Try *here* to rebuild the new map with the last message in List_ReceivedMessages.
	 try:
	   if List_ReceivedMessages:
	 	msg = List_ReceivedMessages[len(List_ReceivedMessages) - 1] # the last one.
	 	print pl0
	 	print "\n"
	 	print player
	 	print "\n"
	 	old_pseudo = player.pseudo # try ?
	 	print board0
	 	ANSIColors.printc("/end run_client/ <magenta> Trying to update the board<white>, with the following message :\n<neg>%s<Neg>" % msg)
	 	board0, pl0, player = ParseMessageIn.board_and_player_of_str(board0, pl0, player, msg, verb=verb2)
	 	print pl0
	 	print "\n"
	 	print board0
	 	print "\n"
	 	print player
	   else:
		 ANSIColors.printc("<warning>\t/end run_client/ <red>No received messages have been used to try to recover the new map<white>.")
	 except:
	   eee = sys.exc_info()[1]
	   ANSIColors.printc("<warning>\t/end run_client/ <red>Failure<yellow> when trying to recover the new map<white>. Error : %s." % str(eee))
	   eee = sys.exc_info()
	   print eee[0]
	   print eee[1]
	   print eee[2]
	   ANSIColors.printc("\n<warning>\t/end run_client/ <red>Failure<yellow> when trying to recover the new map<white>. Error : %s." % str(eee))
	   raise
	   # FIXME ?
	 # Now it is ok.
	 ANSIColors.printc("/end run_client/ <blue>Game variables :<white>.")
	 print (nbmax0, lx0, ly0, pl0, Mi0, Mj0)
	 print "\n"
	 print board0
	 #######################################################################
	 # FIXME
	 ANSIColors.printc("/run_client/ <neg><magenta> Check for pseudos <u>%s<U><reset> I'm starting.......<white>" % old_pseudo)
	 has_the_good_pseudo = 0
	 for tmp_pl in pl0:
	 	has_the_good_pseudo += 1 if (tmp_pl.pseudo == old_pseudo) else 0
	 ANSIColors.printc("/run_client/ <neg><magenta> Check for pseudos (to be sure I received and understood the good ones, my old player's pseudo *have* to be the pseudo of one of my picked up players)<reset> I have %s...<white>" % str(has_the_good_pseudo))
#:	 assert ( has_the_good_pseudo > 1 )
#:	 assert ( has_the_good_pseudo == 1 )
	 # FIXME
	 #######################################################################
	 return player, nbmax0, lx0, ly0, pl0, board0, Mi0, Mj0, List_ReceivedMessages, List_SentMessages
	 # Exit !
	# if launched with double_thread
	return player, nbmax0, lx0, ly0, pl0, board0, Mi0, Mj0, List_ReceivedMessages, List_SentMessages

###################################
#### First step : Waiting room ####

def waiting_room(server = (SERVEUR_INIT, PORT_INIT), pseudo = "Luke", color = "cyan", lx = LX_CST, ly = LY_CST): #, nb = NB_PLAYER):
	""" Create a socket on the server *server*, and run a client on it.

	Here the client will enter in a **wainting room**, connect to a server,
	 then initialize all game variables (the map, the players etc),
	 and when all players will be ok, this function return all those variables,
	 to start the game.

	FIXME: this function is quite long, make sure it is ok.
	"""
	PRINT_ALL_MESSAGE = True
	# Display parameters, just to check they are right affect by the command line args.
	ANSIColors.printc("/params/ Currently, music is <neg>%s<Neg>, X window is <neg>%s<Neg>, and sound effects are <neg>%s<Neg>." % ( ("enabled" if USE_MUSIC else "disabled"), ("enabled" if USE_WINDOW else "disabled"), ("enabled" if USE_SOUND_EFFECT else "disabled") ))
	ANSIColors.printc("/n/ You will be <green>a player for a Bomberman game<white>, with pseudo %s and color %s.... trying connection" % (pseudo, color) )
	try:
	 player = Player.Player(info_server = server, pseudo = pseudo, color = color)
	 # Here is created the socket for the client, in player.socket_player
	 # He *already* sent his pseudo ! (and his color)
	 ANSIColors.printc("/n/ You are <green>now a player for a Bomberman game<white>. And you are identified as %s (and represented as %s)." % (player, repr(player)) )
	 ANSIColors.printc("/./ <blue>Connection is establishing<white> with the server <green><u>%s:%i<U><white>," % server)
	 # The class Player.Player already handle the socket.
	except socket.error:
	 if sys.stderr.isatty():
	 	ANSIColors.writec("\n<warning> <red><u>Connection refused<U><white> This program is a <blue>client<white> which <u>needs a server<U>.\n", file=sys.stderr)
	 	ANSIColors.writec("<warning> <red><u>Connection refused<U><white> ... the server %s:%i seems to be not responding (check if there is no typos in the server's name or if the port is correct).\n" % server, file=sys.stderr)
	 else:
	 	sys.stderr.write("\n\t/!/ This program is a client which needs a server.\n")
	  	sys.stderr.write("/!/ ...  the server %s:%i seems to be not responding (check if there is not type in the server's name or the port).\n" % server)
	 sys.stderr.write('\n/!\\ Connection refused because server was not responding ! /!\\\n')
	 sys.stderr.flush()
	 os._exit(3)
	# If connexion couldn't properly initialized
	except:
	 sys.stderr.write('\n/!\\ Connection refused badly /!\\ Reason : %s.\n' % ( str(sys.exc_info()[1]) ) )
	 sys.stderr.flush()
	 os._exit(4)
	# now the connection is good.
	try:
	 # The 1st phasis.
	 player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages = run_client(player.socket_player, server, player, PRINT_ALL_MESSAGE)
	except:
	 ANSIColors.printc("<warning>\t/E/ <red>Exception returned by run_client<white> : %s" % (str(sys.exc_info()[1])) )
	 raise
	ANSIColors.printc("/!/ Step #1 is done. You are the player %s (repr. %s).\n\t/?/ Now, the map is being constructed..." % (player, repr(player)))
	# Now, the game is beginning
	ANSIColors.printc("/./ <red>Initial exchange is <u>done<U><white> with the server <green><u>%s:%i<U><white>.\n\t/./ The game is starting..." % server)
	return (player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages)

##########################################################
#### A function (to be threaded) displaying the board ####

def affich_loop(background, screen, clock, board, pl, player, keyBinding, num_thread=0, USE_MUSIC=False):
 """ Launch an infinite loop to display the game.

 This function will be launched with an additionnal thread.

 The parameters *background*, *screen* and *clock* are PyGame objetcs.
 And *board*,*pl* represents the board and the list of players.
 """
 ANSIColors.printc("""
/help/ <blue>Tap one of <neg>%s<Neg> to get the list of all availables keys...<white>
""" % ( str(keyBinding.help) ))
 try:
  ANSIColors.printc("""
/affich_loop/ <neg>Thread number %i<Neg> : initialized. Infinite loop (freq=%i) to display the board :
%s
""" % ( num_thread, CLOCK_FREQUENCY, str(board) ))
  oldmat = copy.copy(board.mat) # clever !
  lx = board.lx
  ly = board.ly
  time_after = time.time()
  # Loop start !
  while True:
   clock.tick(CLOCK_FREQUENCY)
   time_before = time_after
   time_now = time.time()
   if (time_now - time_before) > (0.5 / CLOCK_FREQUENCY):
	time_after = time_now
	if USE_WINDOW:
		# PYGAME stuff.
		spotsSprites = listsprite_of_board(board)
		screen.blit(background, (0, 0))
		spotsSprites.draw(screen)
		pygame.display.flip()
	inp = ""
	for event in pygame.event.get():
		if event.type == QUIT:
			if USE_MUSIC or USE_SOUND_EFFECT:
			 ANSIColors.printc("/pygame/ <INFO> The Pygame music mixer is now playing datas/sound/%s.<white>" % (MUSIC_world_clear))
			 play_music(MUSIC_world_clear, number=1, volume=0.40)
			 pygame.mixer.music.fadeout(TIME_FADEOUT * 1000)
			thread.interrupt_main()
			os._exit(0)
		elif event.type == KEYDOWN:
			if verb2:	ANSIColors.printc("/pygame/ <warning> A key have been pressed : %i => %s.<white>" % (event.key, KeyBinding.print_keynum_as_str(event.key)))
			if event.key == K_ESCAPE:
				if USE_MUSIC or USE_SOUND_EFFECT:
				 ANSIColors.printc("/pygame/ <INFO> The Pygame music mixer is now playing datas/sound/%s.<white>" % (MUSIC_world_clear))
				 play_music(MUSIC_world_clear, number=1, volume=0.40)
				 pygame.mixer.music.fadeout(TIME_FADEOUT * 1000)
				thread.interrupt_main()
				os._exit(0)
			elif event.key == K_m:
				USE_MUSIC = True
				# Launching here music.
				play_music(MUSIC_loop(), volume=0.80)
				ANSIColors.printc("/pygame/ <INFO> The Pygame music mixer is initialized, playing datas/sound/%s.<white>" % (MUSIC_loop()))
			elif event.key == K_DOLLAR:
				ANSIColors.printc(help_User)
			for t in ['help', 'right', 'left', 'up', 'down', 'bomb']:
			    if keyBinding.event_key_is_ok(event.key, t):
				 ANSIColors.printc("/pygame/ <INFO> Catching action <neg>%s<Neg>.<white>" % t)
				 inp = t
	if inp and (verb or verb2):
		oldmat = copy.copy(board.mat)
###############################################################################
	if inp in ["!", "$", "stop"]:
#:		thread.exit()	# FIXME
		raise KeyboardInterrupt
	if inp == "":
		continue
	if inp == 'help':
		ANSIColors.printc("""
/help/ <blue>Tap one of <neg>%s<Neg> to get the list of all availables keys...<white>
%s
""" % ( str(keyBinding.help), keyBinding.get_help() ))
		ANSIColors.printc(help_User)
		continue
###############################################################################
	i, j	= player.x, player.y
	Mi, Mj	= i, j	# old pos.
	if verb:	ANSIColors.printc("/player pos/ I'm looking at your spot : %i,%i..." % (i, j))
	move_to_send	= ""
	bool_action	= False
	#: Analyse moves, validate them, update the new position
	#: but this new position (i,j) will be checked later.
	if inp == 'up':
		move_to_send = "UP"
		if verb: ANSIColors.printc("/u/ <blue>You <white>[%s]<white> want to go <green>up<white>." % player)
		i = max(0,i-1)
	if inp == 'down':
		move_to_send = "DOWN"
		if verb: ANSIColors.printc("/d/ <blue>You <white>[%s]<white> want to go <green>down<white>." % player)
		i = min(lx-1,i+1)
	if inp == 'left':
		move_to_send = "LEFT"
		if verb: ANSIColors.printc("/l/ <blue>You <white>[%s]<white> want to go <green>left<white>." % player)
		j = max(0,j-1)
	if inp == 'right':
		move_to_send = "RIGHT"
		if verb: ANSIColors.printc("/r/ <blue>You <white>[%s]<white> want to go <green>right<white>." % player)
		j = min(ly-1,j+1)
	if inp == 'bomb':
		if board[i, j].bomb:
		 ANSIColors.printc("/!/ <u><red>This is not allowed<U><black>, you cannot drop a second bomb <u>here<U>.<white>")
		elif player.nb_bomb >= NB_BOMB_MAX_ALLOW:
		 ANSIColors.printc("/!/ <u><red>This is not allowed<U><black>, you cannot drop a new bomb on the board (max allow : %i).<white>" % NB_BOMB_MAX_ALLOW)
		else:
		 move_to_send = "BOMB"
		 bool_action = True
	###############################################################################
	if not(move_to_send): continue
	ANSIColors.printc("/move_to_send/ I determined that you are concerned about the move '<neg>%s<Neg>'..." % move_to_send)
	# If the new place is new, and is not a wall, move the player to it
	if move_to_send and (move_to_send != "BOMB"):
		bool_action = True
		if (board[i, j].is_free()) and ((i != Mi) or (j != Mj)):
			if verb: ANSIColors.printc("/w/ <green>Player %s<white> wants to move from (%i,%i) to (%i,%i)." % (player, Mi, Mj, i, j))
		elif board[i,j].wall:
			if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is a <u>wall<U> in the wanted spot." % (player, Mi, Mj, i, j))
			if PLAYER_CHECK_ACTION:	continue
		elif board[i,j].bomb:
			if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is a <u>bomb<U> in the wanted spot." % (player, Mi, Mj, i, j))
			if PLAYER_CHECK_ACTION:	continue
		elif (i == Mi) and (j == Mj):
			if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i) because there is the natural limitation of the board." % (player, Mi, Mj, i, j))
			if PLAYER_CHECK_ACTION:	continue
		else:
			if verb: ANSIColors.printc("/!/ <green>Player %s<white> can not move from (%i,%i) to (%i,%i)." % (player, Mi, Mj, i, j))
			if PLAYER_CHECK_ACTION:	continue
	if move_to_send and bool_action:
		ANSIColors.printc("/str_of_move/ I'm transforming the move '<neg>%s<Neg>' into a valid message." % move_to_send)
		move_to_send = ParseMessageOut.str_of_move(move_to_send)
		ANSIColors.printc("/#/ <green>Player %s<white> try to send a message (<neg>%s<Neg>) to his server %s." % (player, move_to_send, str(player.info_server)))
	try:
		# Here is sent the move.
		player.send(move_to_send, verb or verb2)
	except Exception as useless3:
		ANSIColors.printc("<warning> <red>Failure<default>, when you (%s) try to send the message (<neg>%s<Neg>) (I received the exception %s)." % (str(player), move_to_send, str(useless3)))
###############################################################################
# End of the main loop (shall not happen).
 except:
  sys.stderr.write(ANSIColors.sprint("""
<warning>	/affich_loop/ <neg>Thread number %i<Neg> : failed with exception <neg>%s<Neg>.
	/affich_loop/ Now it will try to kill the caller (with <red>thread.interrupt_main()<white>).
""" % ( num_thread, str(sys.exc_info()[1]) )) )
  sys.stderr.flush()
  thread.interrupt_main()
#:  raise
 os._exit(1)

##################################
##### Main loop for the game #####

def main(player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages, keyBinding=KeyBinding.arrows(), verb2=True):
	""" main(player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages, keyBinding=KeyBinding.arrows(), verb2=True) -> Exception (no values returned, only an exception)

	Initialize Pygame and the music, and then launch the game.
	The display is done with a *threaded* function.

	Parameters:
	 * [player]		The player representing the client,
	 * [nbmax]		Is max number of players,
	 * [lx], [ly]		Are lenght of the board,
	 * [pl]			Is the list of player (represented as Player.Player instances),
	 * [board]		Is the board (represented as Board.Board instance !),
	 * [Mi], [Mj]		Are list of players' position to initiate the game,
	 * [List_ReceivedMessages], [List_SentMessages] To continue logging all inputs and outputs.
	 * [keyBinding]		Is a KeyBinding.KeyBinding to map key to moves.
	"""
###############################################################################
	# Just to be sure.
	sys.stderr.flush()
	sys.stdout.flush()
	# Print parameters.
	print (player, nbmax, lx, ly, Mi, Mj)
	k_of_player = -1
	for l in range(len(pl)):
	 Mi[l], Mj[l] = pl[l].x, pl[l].y	# Rebuilt the correction Mi Mj (initial positions).
	 if pl[l].id == player.id:
	  k_of_player = l			# Try to find the good index for the player.
	print "For the player, he have the index %i." % k_of_player
	print (Mi, Mj)
	print keyBinding
	print "\n", board
###############################################################################
	# Initialization of the pygame window.
	pygame.init()
	# Resolution of the screen.
	resY, resX = RESOLUTION_X*lx, RESOLUTION_Y*ly
	if USE_WINDOW:	# FIXME: still not working.
		if USE_FULLSCREEN:	# FIXME: still not working.
			screen = pygame.display.set_mode((resX, resY), pygame.FULLSCREEN)
		else:
			screen = pygame.display.set_mode((resX, resY))
		pygame.display.set_caption('.: Bomberman %ix%i (Res %ix%i) | Player %s, Color %s :.' % (lx, ly, resX, resY, player.pseudo, player.color))
		try:
		 pygame.display.set_icon( load_png( PICTURE_player % ( 1+(player.id % 8) ) ) )
		 #FIXED
		except Exception as e1:
		 try:
		  pygame.display.set_icon( load_png("player.gif")[0] )
		 except Exception as e2:
		  if verb2 or verb:
		   ANSIColors.printc("<INFO> <red> I failed when I tried to change the *window icon*. Cause = %s,%s." %  (str(e1), str(e2)) )
		# Background.
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((14, 0, 0))	#: A dark brown.
		# Make the window.
		screen.blit(background, (0, 0))
		pygame.display.flip()
		ANSIColors.printc("/pygame/ <INFO> The game window is initializing with resolution (%i,%i) (in pixels: %i,%i).<white>" % (lx, ly, resX, resY))
	# Initialization of the clock frequency.
	clock = pygame.time.Clock()
	ANSIColors.printc("/pygame/ <INFO> The game will make %i loop each seconds (this control is made with clock.tick())" % CLOCK_FREQUENCY)
	# Initialization of music mixer.
	pygame.mixer.init()
	if USE_MUSIC:
		# Launching the music.
		play_music(MUSIC_loop(), volume=0.80)
		ANSIColors.printc("/pygame/ <INFO> The Pygame music mixer is initialized, playing datas/sound/%s.<white>" % (MUSIC_loop()))
	# Change how to print boxes of the board (|-+/\\ or nonANSI)
	board.mat.box = Matrix.boxnoASCII if Board.UTFSupported else Matrix.boxASCII
	ANSIColors.writec("\a\n\t/s/ <green>Bomberman game is going to start ... <white>\n")
###############################################################################
	#: Start parallelization
	NB_THREADS = 1
	thread.start_new_thread( affich_loop, (background, screen, clock, board, pl, player, keyBinding, NB_THREADS, USE_MUSIC) )
	NB_THREADS = 70
	thread.start_new_thread( toggle_explosion, (board, pl, clock), {'MAKE_DESTROY':False, 'FORCE':False, 'num_thread':NB_THREADS, 'player':player})
###############################################################################
	nsin = ("%s:%i" % player.socket_player.getsockname())
	sin = player.socket_player.makefile()
	sout = sys.stdout
	client_to_server = False
	# To count the nb of turns, and the time.
	nb_turn = 1
	time_before = time.time()
	time_after = time.time()
	# Go !
###############################################################################
	try:
		while player.pv > 0:
		 #: To ensure that the printing is not too quick.
		 clock.tick(CLOCK_FREQUENCY)
###############################################################################
		 # Tring to get infos about temporalisation (for printing etc)
		 time_before = time_after
		 time_now = time.time()
#:		 if verb2:	ANSIColors.printc("<white>/time/ New loop ! Now=%s, before=%s, diff=%s.\n" % ( str(time_now), str(time_before), str(time_now - time_before) ))
		 if ((time_now - time_before) > TIME_EXPLOSION ):
		  # print_clear(board)  # FIXME do not print the board constantly ?
		  # print_pvs_player(pl)
		  # MAKE update which depends on TIME.
		  for itmp ,jtmp, spottmp in board:
			  board[itmp, jtmp].explosion = False
		  if verb2:	ANSIColors.printc("<white>/time/ Time lapse between now and the last tic : <neg>%f<Neg>." % (time_now - time_before))
		  time_after = time_now
#:		  board.tic(1, MAKE_DESTROY=False)
		  # Handle all bombs : now timer is not used for trigger explosion (but for textual mode display)
		  nb_turn += 1
		  if verb:	ANSIColors.printc("/t/ <blue>New turn !<white> Number of turn : <neg>%i<Neg>." % nb_turn)
###############################################################################
	 	 # Receive all actions, and apply them *textually* withouh any verification.
		 # Tring to get infos from the server.
		 if verb2:	print "Waiting for a message from the server...."
		 readstr = sin.readline()
		 # Handle if server is closing
		 if not(readstr):
			ANSIColors.printc("/%s/<INFO> <yellow>I read an empty string (that means from a closed connection) <white>...." % "in" if client_to_server else "out")
		 	raise Exception("Communication (%s) is closing..." % ("in" if client_to_server else "out"))
		 else:
		  List_ReceivedMessages.append( readstr )
		  if PRINT_ALL_MESSAGE and (readstr[0]!='\n' if len(readstr)>0 else True):
		 	ANSIColors.writec('/in/ Message [<yellow>%s<white>] readed from <blue>%s<white>,' % ((readstr[:(len(readstr) - 1)] ), nsin), file=sout)
		  # readstr is now a message from the server.
###############################################################################
		  # Update the current game with those orders.
		  # the unpack functions are gameover_of_str, posplantbomb_of_str, blowbomb_of_str, moveplayer_of_str
		  try:
			  keep_parsing = True
			  if verb2:	ANSIColors.printc("/in/<INFO> Beginning parsing '<neg>%s<Neg>'." % readstr)
			  readstr = readstr[: len(readstr) - 1 ]	# Delete the last '\n'
			  while keep_parsing and readstr:
			  #############################################################
			   if readstr[:1] == 'G':
			 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a GAME_OVER message." % readstr)
			 	readstr, unparsed_id = ParseMessageIn.gameover_of_str(readstr)
			 	ANSIColors.printc("/in/<INFO> I received a GAME_OVER message, for the player with id = %i." % unparsed_id)
			 	for tmp_pl in pl:
			 	 print tmp_pl
			 	 if tmp_pl.id == unparsed_id:
			 	  raise ParseMessageIn.GameOver(tmp_pl)
			  #############################################################
			   elif readstr[:1] == 'P':
			 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a PLANT_BOMB message." % readstr)
			 	readstr, unparsed_i, unparsed_j = ParseMessageIn.posplantbomb_of_str(readstr)
			 	if not(board[unparsed_i, unparsed_j].players):
			 		ANSIColors.printc("<red>/in/<warning> There is no player able to plant a bomb in spot %i:%i...<white>" % (unparsed_i, unparsed_j))
			 	ANSIColors.printc("/in/<INFO> Considering the spot <neg>%i,%i<Neg>..." % (unparsed_i, unparsed_j))
			 	newbomb = Bomb.BombNoOwner()
			 	board[unparsed_i, unparsed_j].bomb = newbomb
			 	ANSIColors.printc("/in/<INFO> Now there is a new bomb (<neg>%s<Neg>) <neg>at spot %i,%i<Neg>..." % (newbomb, unparsed_i, unparsed_j))
			 	update_print = True
			  #############################################################
			   elif readstr[:1] == 'B':
			 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a BOMB_BLOW message." % readstr)
			 	readstr, unparsed_i, unparsed_j, unparsed_radius = ParseMessageIn.blowbomb_of_str(readstr)
			 	if not(board[unparsed_i, unparsed_j].bomb):
			 		ANSIColors.printc("<red>/in/<warning> There is no bomb to blow in spot %i:%i...<white>" % (unparsed_i, unparsed_j))
			 		board[unparsed_i, unparsed_j].bomb = Bomb.BombNoOwner()
			 		ANSIColors.printc("<tellow>/in/<warning> I create the bomb <neg>%s<Neg><white>" % (board[unparsed_i, unparsed_j].bomb))
			 	ANSIColors.printc("/in/<INFO> Considering the bomb %s, <neg>at spot %i,%i<Neg>..." % (board[unparsed_i, unparsed_j].bomb, unparsed_i, unparsed_j))
			 	if USE_SOUND_EFFECT:	# play the sound of an explosion.
					pygame.mixer.music.pause()
					play_music(MUSIC_explosion, number=1, volume=0.80)
					if USE_MUSIC:
						pygame.mixer.music.queue('datas/sound/' + MUSIC_loop())
			 	board.destroy_bomb(unparsed_i, unparsed_j, radius=unparsed_radius, FORCE=True)
			 	#, verb=verb2) FIXED.
			 	ANSIColors.printc("/in/<INFO> The bomb %s, <neg>at spot %i,%i<Neg> <yellow>had exploded<white> !" % (board[unparsed_i, unparsed_j].bomb, unparsed_i, unparsed_j))
			 	# A try ?
			 	for tmp_pl in pl:
			 		if tmp_pl.pv <= 0:

			 			pl.remove(tmp_pl)
			 			ANSIColors.printc("/in/ <warning> I <neg>removed the player %s<Neg> from my current list of alive players (because he seemed to have less than 1 PVs) PV=%i...." % (str(tmp_pl), tmp_pl.pv))
						board[ tmp_pl.x, tmp_pl.y ].players.remove(tmp_pl)
			 			ANSIColors.printc("/in/ <warning> I <neg>removed the player %s<Neg> from the spot %i,%i (because he seemed to have less than 1 PVs) PV=%i...." % (str(tmp_pl), tmp_pl.x, tmp_pl.y, tmp_pl.pv))
			 	for itmp, jtmp, spottmp in board:
			 		for tmp_pl in board[itmp, jtmp].players:
				 		if tmp_pl.pv <= 0:
				 			board[itmp, jtmp].players.remove(tmp_pl)
			 				ANSIColors.printc("/in/ <warning> I <neg>removed the player %s<Neg> from the spot %i,%i (because he seemed to have less than 1 PVs) PV=%i...." % (str(tmp_pl), itmp, jtmp, tmp_pl.pv))
			 	# FIXME ?
			 	update_print = True
			  #############################################################
			   elif readstr[:1] == 'M':
			 	ANSIColors.printc("/in/<INFO> Trying to interpret [<neg>%s<Neg>] as a MOVE_PLAYER message." % readstr)
			 	readstr, unparsed_id, unparsed_i, unparsed_j = ParseMessageIn.moveplayer_of_str(readstr)
			 	for tmp_pl in pl:
			 	 if board[unparsed_i, unparsed_j].players:
			 	 	ANSIColors.printc("/in/<INFO> Considering the player %s, <neg>at spot %i,%i<Neg>..." % (board[unparsed_i, unparsed_j].players[0], unparsed_i, unparsed_j))
			 	 print tmp_pl
			 	 if (tmp_pl.id == unparsed_id):
			 	  if not( board[unparsed_i, unparsed_j].is_free() ):
			 	  	  ANSIColors.printc("<red>/in/<warning> For MOVE_PLAYER (about player <neg>%s<Neg> with id=%i) : the new spot is not empty !<white>" % ( str(tmp_pl), unparsed_id ))
			 	  board[tmp_pl.x, tmp_pl.y].players.remove(tmp_pl)
			 	  tmp_pl.move(unparsed_i, unparsed_j)
			 	  board[tmp_pl.x, tmp_pl.y].players.append(tmp_pl)
			 	  ANSIColors.printc("/in/<INFO> The player %s is now here : %i:%i." % (tmp_pl, tmp_pl.x, tmp_pl.y))
			  #############################################################
			   else:
			  	keep_parsing = False
			 	if verb:	ANSIColors.printc("""
<question>\t/in/<INFO> I can't interpret [<neg>%s<Neg>] as any messages I can understand...
""" % readstr)
###############################################################################
		  # End of the game (GameOver).
		  except ParseMessageIn.GameOver as e:
			player2, msg = e.player, e.msg
		  	ANSIColors.printc("/GameOver/ I received the exception GameOver : player=%s, msg=%s." % (str(player2), msg))
			if player2.id == player.id:
				ANSIColors.printc("""
/end of the game/ <green> <neg>You win !!<Neg><white> You received the message '%s'.""" % msg)
				ANSIColors.printc("""/end of the game/ <green> The game is closing now.<white>""")
				os._exit(0)
			else:
				ANSIColors.printc("""
<warning>\t/end of the game/ <magenta> The player <neg>%s<Neg> wan ! (he was represented as : %s).
""" % (player2, str(player2)))
				ANSIColors.printc("""
<INFO>\t/end of the game/ <red> You lost...<white> Try again ! You received the message '%s'.
""" % msg)
				ANSIColors.printc("""
<warning>\t/end of the game/ <red> The game is closing now.<white>""")
				os._exit(1)
###############################################################################
		  # Death of players.
		  except Player.PlayerDeath as e:
			player2, ingury, msg = e.player, e.ingury, e.msg
		  	ANSIColors.printc("/PlayerDeath/ I received the exception PlayerDeath : player=%s, msg=%s, ingury=%s." % (str(player2), msg, str(ingury)))
			if player2.id == player.id:
				ANSIColors.printc("""
<warning>\t/your death/ <red> You are dying !!<white> You received %i ingur%s, and the message '%s'.""" % (ingury, "y" if ingury<2 else "ies", msg))
				ANSIColors.printc("""
<warning>\t/your death/ <red> The game is closing now.<white>""")
				os._exit(2)
			else:
				ANSIColors.printc("""
<INFO>\t/other death/ <yellow> One of your opponent is dying !!<white> He received %i ingur%s, and the message '%s'.\n\t/other death/ Good job !
""" % (ingury, "y" if ingury<2 else "ies", msg))
				try:
				 pl.remove(player2)
				 board[ player2.x, player2.y ].players.remove(player2)
				except:
				 ANSIColors.printc("<warning> When I tried to remove this died player from the game variables...")
		  except Exception as e:
		   if verb:	ANSIColors.printc("""
/in/ <INFO> <red>Parsing failed !<white> Maybe the message %s was not a good one !. Exception : <neg>%s<Neg>.<white>
""" % (readstr, str(e)))
		  if verb2:	ANSIColors.printc("""
/in/<INFO> Concluding parsing ...<white>
""")
###############################################################################
	# Handling of all uncaugth exception (this is phasis 3).
	except socket.error:
		try:
		 player.close()
		except:
		 ANSIColors.printc("""
	<ERROR> <magenta> I failed when I tried to close the player <neg>%s<Neg>. Cause nb2 = <neg>%s<Neg>...
	""" % (player, str(sys.exc_info()[1])) )
		 raise	#FIXME ?
		ANSIColors.printc("""
<warning> <red>Phasis #2 closed !<default> Connection closed (<neg>%s<Neg>).
""" % str(sys.exc_info()[1]) )
		os._exit(3)
	except:
		try:
		 player.close()
		except:
		 ANSIColors.printc("""
	<ERROR> <magenta> I failed when I tried to close the player <neg>%s<Neg>. Cause nb2 = <neg>%s<Neg>...
	""" % (player, str(sys.exc_info()[1])) )
		 raise	#FIXME ?
		ANSIColors.printc("""
<warning> <red>Phasis #2 closed !<default> I received the last exception  <neg>%s<Neg>.
""" % str(sys.exc_info()[1]) )
		raise
###############################################################################

###############
##### End #####

if __name__ ==  '__main__':
	import ParseCommandArgs
	#: This variable is the preprocessor, given to description and epilog by ParseCommandArgs,
	#:  * erase: to print with no colors.
	#:  * sprint: to print with colors.
	preprocessor = ANSIColors.sprint if ANSIColors.ANSISupported else ANSIColors.erase
	#:preprocessor = __builtin__.str	#:, if you want to *see* the balises.
	#: Generate the parser, with another module.
	parser = ParseCommandArgs.parser_default(\
		description = '<green>BombermanClient <red>module<reset> and <blue>script<reset>.',\
		epilog = """\n\
<yellow>About:
======<reset>
 This is the client for a <neg>multiplayer Bomberman Game<Neg> (MPRI 1-21 projet, 2013).
 This project is hosted here <u>https://bitbucket.org/vcohen/projet_reseau<U>.
 The doc for this project can be find here <u>http://perso.crans.org/~besson/publis/Bomberman/_build/html/<U>.""", \
		version = __version__, date = __date__, author = __author__, \
 		preprocessor = preprocessor)
	#: Description for the part with '--file' and '--generate' options.
	group = parser.add_argument_group(preprocessor('<yellow>About network connection<reset>'), preprocessor("""\
<b>This program <u>is a client<U>. So, it *have* to be connected to a server, with a TCP port : <reset>
"""))
	#: Remember that action can be used to many things.
		#: FIXME make required.
	group.add_argument("-s","--server", help = preprocessor("The <neg>address of the server<Neg> (eg '138.231.139.1', or 'bomberman-server.crans.org'). Default is %s." % SERVEUR_INIT)) #:, required = True)
	group.add_argument("-p","--port", type = int, help = preprocessor("The <neg>port<Neg> on which the connection to the server will be established (eg 9312, or 12882).\n\t This port *have* to be an <default>open port on your machine<reset> and have to be <default>the listened port of the server<reset> ! Default is %s." % PORT_INIT)) #:, required = True)
	#: Description for pseudo and color options.
	group = parser.add_argument_group(preprocessor('<yellow>About customisation<reset>'), preprocessor("""\
<b>With this program, <u>you will be<U> a Bomberman player. And this player can be customized with a <u>pseudo<U> and a <u>color<U> : <reset>
"""))
	group.add_argument('-P', '--pseudo', default = pseudo_Init, help = preprocessor(""" Set the <neg>client's pseudo<Neg>. Default is random or picked up from <neg>ConfigClient.py<Neg> (For instance, %s).""" % pseudo_Init ))
	group.add_argument('-C', '--color', choices=ANSIColors.simpleColorList, default = color_Init, help = preprocessor(""" Set the <neg>client's color<Neg>. 8 different colors are available : <black>black<default>, <red>red<default>, <green>green<default>, <yellow>yellow<default>, <blue>blue<default>, <magenta>magenta<default>, <cyan>cyan<default>, <white>white<reset>. Default is random or picked up from <neg>ConfigClient.py<Neg>. (For instance, %s)""" % color_Init ))
	#: For music.
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--music', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, the program will <blue>launch some music<reset> during the game. <red>Still experimental.<reset>"""))
	group.add_argument('--nomusic', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, music will <blue>not be used<reset>. This is the <neg>default<Neg> comportment."""))
	#: For X Window of PyGame. FIXME
	#:	group = parser.add_mutually_exclusive_group()
	#:	group.add_argument('--window', action='store_true', default = True, help = preprocessor(""" If <yellow>present<reset>, the program will <blue>use a graphical Window<reset> during the game. Still not perfect (update freezes sometime). This is the <neg>default<Neg> comportment."""))
	#:	group.add_argument('--nowindow', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, <blue>no window will be used<reset>. Can be usefull to play in textmod (but <red>PyGame is still required<reset> to Keybinding, sound etc), for example if you don't have a X Server."""))
	#: For music effect.
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--soundeffect', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, the program will <blue>use some music effect<reset> during the game, mainly when a bomb blows.<reset>"""))
	group.add_argument('--nosoundeffect', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, music effect will <blue>not be used<reset>. This is the <neg>default<Neg> comportment."""))
	#: The parser is done,
	#: Use it to extract the args from the command line.
	args = parser.parse_args()

	ANSIColors.xtitle(".: Bomberman Client, v%s, made by %s :." % (__version__, __author__))
	print_clear(".: Welcome in the Bomberman Client, v%s, made by %s. Last modification %s :." % (__version__, __author__, __date__))

	# Use those args.
	verb = (args.verbose > 1) or verb	# Default = True
	verb2 = (args.verbose > 2) and verb2	# Default = False
	if verb2:	print(" Processing command line args...")
	print("About verbosity: verb=%s, verb2=%s." % (verb, verb2))
	# Try to know if music is wanted. Default = False
	USE_MUSIC = (USE_MUSIC or args.music) and not(args.nomusic)
# Try to know if window is wanted. Default = True. FIXME
#	USE_WINDOW = (USE_WINDOW or args.window) and not(args.nowindow)
	# Try to know if music effects are wanted. Default = False
	USE_SOUND_EFFECT = (USE_SOUND_EFFECT or args.soundeffect) and not(args.nosoundeffect)

	# Print with ANSI escape code for colors if possible
	ANSIColors.ANSISupported = (not(args.noANSI) and ANSIColors.ANSISupported) or args.ANSI
	# Disable all escape codes for color to be generated
	if not(ANSIColors.ANSISupported):
		ColorOff()
	else: ColorOn()
	ANSIColors.printc("/initialization/ ANSI escape code for colors supports = <green>%s<white>." % ANSIColors.ANSISupported)
	# Print with non ASCII caracters for boxes if possible
	Board.UTFSupported = not(args.noUTF) and Board.UTFSupported
	ANSIColors.printc("/initialization/ UTF escape code for boxes supports = <green>%s<white>." % Board.UTFSupported)

	#: Set the server and the port.
	server = args.server if args.server else SERVEUR_INIT
	port = args.port if args.port else PORT_INIT

	# Pseudo and color.
	try:
		pseudo = args.pseudo[:32]
	except:
		pseudo = pseudos_CST[ os.getpid() % len(pseudos_CST) ]+"_"+str(os.getpid())
	try:
		color = args.color[:32]
	except:
		color = ANSIColors.simpleColorList[ os.getpid() % len(ANSIColors.simpleColorList)]

	ANSIColors.printc("/init/ <yellow>The game will run on the server : (%s:%i)<reset><white>." % (server, port))
	if USE_NOTIFY:  ANSIColors.notify("Phasis #1 of Bomberman Client is going to start (with the server %s:%i)" % (server, port), obj=".: Bomberman Game :.", icon="bomberman.gif")
	ANSIColors.xtitle(".: Phasis #1 of Bomberman Client (connected to %s:%i) -- Pseudo=%s, Color=%s :." % (server, port, pseudo, color))
	# Launch the step 1.
	try:
	 player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages = waiting_room(server = (server, port), pseudo = pseudo, color = color)
	except Exception as e:
	 ANSIColors.printc("<ERROR> <red> The waiting room <neg>died<Neg> !<default>. I received the last exception <neg>%s<Neg>." % str(e))
	 raise e
	# The game is initialized
	if USE_NOTIFY:  ANSIColors.notify("Phasis #2 of Bomberman Client is going to start (with the server %s:%i)" % (server, port), obj=".: Bomberman Game :.", icon=(PICTURE_player % ( 1+(player.id % 8) )) )
	ANSIColors.xtitle(".: Phasis #2 of Bomberman Client (connected to %s:%i) -- Pseudo=%s, Color=%s, Id=%i :." % (server, port, player.pseudo, player.color, player.id))
	try:
	 main(player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages)
###############################################################################
	except KeyboardInterrupt:
	 ANSIColors.printc("""
<warning> <red> The game is done<default>.
<warning>  I <yellow>guess<default> you closed it, probably with an EOF (<black>Ctrl+D<default>) or a SIGTERM signal (<black>Ctrl+C<default>).
<warning>  <green>Feel free to send any comment, suggestion or bug : <white> <u><neg>%s<reset>.
""" % (__email__))
	 sys.stdout.flush()
	 sys.stderr.flush()
	 os._exit(1)
###############################################################################
	except socket.error as e:
	 if USE_MUSIC:
	 	time.sleep(TIME_FADEOUT)
	 	pygame.mixer.music.stop()
	 if USE_WINDOW:  pygame.display.quit()
	 try:
	  player.close()
	 except:
	  ANSIColors.printc("""
<ERROR> <magenta> I failed when I tried to close the player <neg>%s<Neg>. Cause nb2 = <neg>%s<Neg>...
""" % (str(player), str(sys.exc_info()[1])) )
#:	  raise	#FIXME ?
	 ANSIColors.printc("""
<ERROR> <magenta>Connection closed !<default>. So the game died. The possible cause might be <neg>%s<Neg>.
""" % str(e))
	 raise e
###############################################################################
	except Exception as e:
	 if USE_MUSIC:
	 	time.sleep(TIME_FADEOUT)
	 	pygame.mixer.music.stop()
	 if USE_WINDOW:  pygame.display.quit()
	 ANSIColors.printc("""
<ERROR> <red><u> The game died badly !<U><default> I received the last exception <neg>%s<Neg>.
""" % str(e))
#:	 raise e	# FIXME
###############################################################################
	finally:
	 ANSIColors.printc("""
<ERROR> <red> The game is done<default>... I received the last exception <neg>%s<Neg>.
""" % str(sys.exc_info()[1]) )
	 sys.stdout.flush()
	 sys.stderr.flush()
#:	 raise	# FIXME ?
	# End that's it.
	ANSIColors.printc("""
<green><neg> The game is done<white>, and I didn't receive any unhandled exceptions in the end<reset> (good job !)...
The second phasis seems to give <neg>you<Neg> as the winner.
<black>I'm quiting nicely now... <green>Feel free to send any comment, suggestion or bug : <white> <u><neg>%s<reset>.
""" % ( __email__ ) )
	# Now, quit.
	os._exit(0)

###############################################################################
# DONE.
