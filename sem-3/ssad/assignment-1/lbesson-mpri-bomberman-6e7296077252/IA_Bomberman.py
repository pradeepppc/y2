#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" This program is an experimental **BOT** for our *Bomberman multiplayer game*.

Textual example
---------------
  This show how the **textual mode** *looks like during the game* with *one* server and *3 bots*.
  The server is in the left top corner.
  In this example, the server have been *interrupted* with *Ctrl+C*.

.. image:: images/exemple_ia.png
   :scale: 78 %
   :align: center

Graphical example
------------------
  This show how the **graphical mode** *looks like during the game* with *one* server and *3 bots*.
  The server is in the left top corner.

.. image:: images/exemple_ia3.png
   :scale: 78 %
   :align: center

Why ?
=====

.. tip::
  This program is **not** designed to *kiss Kasparov ass*... :)

 It is design to be able to **play alone**, with *IA* for opponents.
  * That means, you can launch a few on your computer and then launch you client (and play with it),
  * Or, a server can launch in on his side, to reduce the *required number* of players, or simply make an automatic opponent (like the *"play against the computer"* options of *multiplayer* games).

How to launch it
----------------

 **Exactly like the client** (see `the BombermanClient module <BombermanClient.html>`_).
  For instance, to get the description :
   $ ./IA_Bomberman.py --help

  On option is available : the **frequency** of the bot.
  The frequency of the server is limited, but you can change the number of action send *each seconds* by the bot.
  For example, a reasonable value is 10 :
   $ ./IA_Bomberman.py --frequency 10

  And, like for the *client*, you can change the **port** and the **address** of the server to play with :
   $ ./IA_Bomberman.py --frequency 10 --server 137.124.67.13 --port 12882

About
-----

 For now, it is quite limited : the *bot* plays *randomly* !

 No complex analysis of the board is done, neither that complex heuristic to attack others players or breaking free walls.

 .. seealso::
    But this is in study !
"""

__author__='Lilian BESSON'	#: Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__email__='lilian.besson[AT]normale.fr'
__version__='0.7b'	#: Version of this module
__date__='dim. 17/02/2013 at 17h:20m:13s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
try:
	import os, sys, time
	__date__ = time.strftime("%a %d/%m/%Y at %Hh:%Mm:%Ss", time.localtime(os.lstat(sys.argv[0]).st_mtime))
	del os, sys, time
except:	pass

RUNNING_BOT    =   True
# Constant that tell to the BombermanClient.py module that it has been called from the bot
from BombermanClient import *

##################################
#    Playing with directions     #
##################################

DIR = ['UP', 'DOWN', 'LEFT', 'RIGHT']

def randDir(no = []):
	tmpDir = copy.copy(DIR)
	for a in no:
		if a in tmpDir:
			tmpDir.remove(a)
	return random.choice(tmpDir)

def verti(move_to_send):
	return move_to_send in ['UP', 'DOWN']

def horiz(move_to_send):
	return move_to_send in ['RIGHT', 'LEFT']

def orthog_of_move(move_to_send):
	if   verti(move_to_send):	return random.choice(['RIGHT', 'LEFT'])
	elif horiz(move_to_send):	return random.choice(['UP', 'DOWN'])
	else: return randDir()

def opposite_of_move(move_to_send):
	if   move_to_send == 'UP':	return 'DOWN'
	elif move_to_send == 'RIGHT':	return 'LEFT'
	elif move_to_send == 'LEFT':	return 'RIGHT'
	elif move_to_send == 'DOWN':	return 'UP'
	else: return randDir()

def mean(l):
	if l:
		return sum(l) / float(len(l))
	else:
		return 0.0

def indices_of_players(board, player=None):
	indices_i = []
	indices_j = []
	for i, j, spot in board:
		for p in spot.players:
		    if player:
		      if p.id != player.id:
			indices_i.append(p.x)
			indices_y.append(p.y)
		    else:
			indices_i.append(p.x)
			indices_y.append(p.y)
	return (indices_i, indices_j)

def indice_moyen(board, player):
	i, j = indices_of_players(board, player)
	return int(mean(i)), int(mean(j))

def direction_moyenne(board, player):
	i, j = indice_moyen(board, player)
	x, y = player.x, player.y
	a = i - x
	b = j - y
	# vecteur (a,b)
	if abs(a) > abs(b):
		if a>0:
			return 'RIGHT'
		elif a<0:
			return 'LEFT'
		else:
			return random.choice(['RIGHT', 'LEFT'])
	elif abs(a) < abs(b):
		if b<0:
			return 'DOWN'
		elif b>0:
			return 'UP'
		else:
			return random.choice(['DOWN', 'UP'])
	else:
		if a<0: return randDir(no='RIGHT')
		if a>0: return randDir(no='LEFT')
		if b<0: return randDir(no='UP')
		if b>0: return randDir(no='DOWN')
		else:	randDir()

# Probability of dropping a bomb.
# Set to 0 for a bot that will not kill itself !
PROBA_BOMB = 0.03

FREQUENCE_IA = 5

##################################
##### Main loop for the game #####

def run_bot(board, pl, clock, player, num_thread=0):
 """ run_bot(board, pl, clock, player, num_thread=0) -> Exception raised.

An experiment function (designed to be threaded), to make a *non*-interactive Bomberman Player.
The goal is to have an automatic player.
 """
 try:
  ANSIColors.printc("""
/run_bot/ <neg>Thread number %i<Neg> : initialized. Infinite loop (freq=%i) to display the board :
%s
""" % ( num_thread, CLOCK_FREQUENCY, str(board) ))
###############################################################################
  time_after = time.time()

  last_move = randDir()
  next_move = []
  # FIXME ?
  assert( FREQUENCE_IA >= 1.0)
  assert( FREQUENCE_IA < 80.0)
  # Loop start !
  while True:
   clock.tick(FREQUENCE_IA)
   time_before = time_after
   time_now = time.time()
   if (time_now - time_before) > (1.0 / FREQUENCE_IA):
	time_after = time_now
	#######################################################################
	# Here is done the "IA" computation.
	if next_move:
		move_to_send = next_move.pop()
	else:
		if random.random() < PROBA_BOMB:
			move_to_send = 'BOMB'
			d = randDir()
			next_move.append(d)
#:			next_move.append(orthog_of_move(d))
		else:
			move_to_send = randDir()
#:			move_to_send = direction_moyenne(board, player)
#:			next_move.append( randDir(no=move_to_send) )
	ANSIColors.printc("<neg> IA : <Neg> I chosed move_to_send=<neg><u>%s<U><Neg>.\n" % move_to_send)
	#######################################################################
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
<warning>	/run_bot/ <neg>Thread number %i<Neg> : failed with exception <neg>%s<Neg>.
	/run_bot/ Now it will try to kill the caller (with <red>thread.interrupt_main()<white>).
""" % ( num_thread, str(sys.exc_info()[1]) )) )
  sys.stderr.flush()
  thread.interrupt_main()
#:  raise
 os._exit(1)

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
		description = '<green>IA_Bomberman<red>module<reset> and <blue>script<reset>.',\
		epilog = """\n\
<yellow>About:
======<reset>
This program is an experimental BOT for our <neg>multiplayer Bomberman Game<Neg> (MPRI 1-21 projet, 2013).
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
<b>With this program, <u>you will launch<U> a Bomberman BOT. You can set his frequency :
"""))
	group.add_argument("-f","--frequency", type = int, help = preprocessor("The <neg>frequency<Neg> of moves for the IA player. Between 1 and 80. Default is %i." % FREQUENCE_IA))
	#: For music.
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--music', action='store_true', default = False, help = preprocessor(""" If <yellow>present<reset>, the program will <blue>launch some music<reset> during the game. <red>Still experimental.<reset>"""))
	group.add_argument('--nomusic', action='store_true', default = True, help = preprocessor(""" If <yellow>present<reset>, music will <blue>not be used<reset>. This is the <neg>default<Neg> comportment."""))
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

	ANSIColors.xtitle(".: IA Bomberman, v%s, made by %s :." % (__version__, __author__))
	print_clear(".: Welcome in the IA Bomberman, v%s, made by %s. Last modification %s :." % (__version__, __author__, __date__))
	verb = False
	verb2 = False
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

	# Try to know if music is wanted. Default = False
	USE_MUSIC = (USE_MUSIC or args.music) and not(args.nomusic)
	# Try to know if window is wanted. Default = True. FIXME
	#	USE_WINDOW = (USE_WINDOW or args.window) and not(args.nowindow)
	# Try to know if music effects are wanted. Default = False
	USE_SOUND_EFFECT = (USE_SOUND_EFFECT or args.soundeffect) and not(args.nosoundeffect)

	#: Set the server and the port.
	server = args.server if args.server else SERVEUR_INIT
	port = args.port if args.port else PORT_INIT

	try:	FREQUENCE_IA = max(1, min(int(args.frequency), 80))
	except:	pass
	try:
		assert( FREQUENCE_IA >= 1.0)
		assert( FREQUENCE_IA < 80.0)
	except:
		ANSIColors.writec("\n<warning> <ERROR> I told you, the frequency <neg>have<Neg> to be between 1 and 80... You gave me this %s ! I'm using 1 instead....\n" % str(FREQUENCE_IA), file=sys.stderr)
		sys.stderr.flush()
		FREQUENCE_IA = 1

	# Pseudo and color.
	pseudo = pseudos_IA[ (random.randint(1, FREQUENCE_IA) + os.getpid()) % len(pseudos_IA)]+"_IA_"+str(os.getpid())
	color = ANSIColors.simpleColorList[ (random.randint(1, FREQUENCE_IA) + os.getpid()) % len(ANSIColors.simpleColorList)]

	ANSIColors.printc("/init/ <yellow>The game will run on the server : (%s:%i)<reset><white>." % (server, port))
	if USE_NOTIFY:  ANSIColors.notify("Phasis #1 of IA Bomberman is going to start (with the server %s:%i)" % (server, port), obj=".: Bomberman Bot :.", icon="bomberman.gif"  )
	ANSIColors.xtitle(".: Phasis #1 of IA Bomberman (connected to %s:%i) Freq=%i -- Pseudo=%s, Color=%s :." % (server, port, FREQUENCE_IA, pseudo, color))
	# Launch the step 1.
	try:
	 player, nbmax, lx, ly, pl, board, Mi, Mj, List_ReceivedMessages, List_SentMessages = waiting_room(server = (server, port), pseudo = pseudo, color = color)
	except Exception as e:
	 ANSIColors.printc("<ERROR> <red> The waiting room <neg>died<Neg> !<default>. I received the last exception <neg>%s<Neg>." % str(e))
	 raise e
	# The game is initialized
	if USE_NOTIFY:  ANSIColors.notify("Phasis #2 of IA Bomberman is going to start (with the server %s:%i). Frequency=%i." % (server, port, FREQUENCE_IA), obj=".: Bomberman Bot :.", icon="bomberman.gif" )
	ANSIColors.xtitle(".: Phasis #2 of IA Bomberman (connected to %s:%i) Freq=%i -- Pseudo=%s, Color=%s, Id=%i :." % (server, port, FREQUENCE_IA, player.pseudo, player.color, player.id))
	try:
	 thread.start_new_thread( run_bot, (board, pl, pygame.time.Clock()), {'num_thread':2, 'player':player})
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
	#######################################################################
	except socket.error as e:
	#FIXME ?
	 ANSIColors.printc("""
<ERROR> <magenta>Connection closed !<default>. So the game died. The possible cause might be <neg>%s<Neg>.
""" % str(e))
	 try:
	  player.close()
	 except:
	  ANSIColors.printc("""
<ERROR> <magenta> I failed when I tried to close the player <neg>%s<Neg>. Cause nb2 = <neg>%s<Neg>...
""" % (player, str(sys.exc_info()[1])) )
#:	  raise	# FIXME.
#:	 raise e
	 sys.stderr.write("  The game is closing now... Thanks for using IA_Bomberman ! ... Exit code=2...")
	 sys.stderr.flush()
	 os._exit(2)
	#######################################################################
	except Exception as e:
	 ANSIColors.printc("""
<ERROR> <red><u> The game died badly !<U><default> I received the last exception <neg>%s<Neg>.
""" % str(e))
	 raise e
	except:
	 ANSIColors.printc("""
<ERROR> <red> The game is done<default>... I received the last exception <neg>%s<Neg>.
""" % str(sys.exc_info()[1]) )
	 sys.stdout.flush()
	 sys.stderr.flush()
#:	 raise
	#######################################################################
	# End that's it.
	ANSIColors.printc("""
<green><neg> The game is done<white>, and I didn't receive any unhandled exceptions in the end<reset> (good job !)...
The second phasis seems to give <neg>you<Neg> as the winner.
<black>I'm quiting nicely now... <green>Feel free to send any comment, suggestion or bug : <white> <u><neg>%s<reset>.
""" % ( __email__ ) )
	# Now, quit.
	os._exit(0)
