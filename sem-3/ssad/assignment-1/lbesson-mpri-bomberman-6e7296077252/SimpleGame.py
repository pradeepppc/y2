#!/usr/bin/python
# -*- encoding: utf-8 -*-

""" This module implement a simple Bomberman game.
No concrete net yet (just some try : connect all players to a server, and log all move).

.. warning::
   This script is **deprecated**, don't use it.
   Delete me ! I'm useless now...

Can also be used as a program, currently just for testing.
./SimpleGame.py [OPTIONS]

Options:
========
 * --help, -h	Exit and print this help message.
 * -v1	Increase verbosity (default).
 * -v2	Increase again ! (not very good).
 * --debug	Run with pygdb.
 * --noANSI	Disable colors and escape caracters from ANSIColors.
		 Usefull to run the program with bpython.
 * --noUTF	Disable UTF caracters for boxes printing. 
		 Uggly, but more universal !
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.00b'
__date__='jeu. 14/02/2013 at 05h:17m:53s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules #
import sys, copy, random

#2#################
# Project Modules #
#:import Bomb	# Bomb.py : implements the simple bomb system. (actions, representation etc)
import Player	# Player.py : implements the simple player system. (actions, representation etc)
import ANSIColors	# ANSIColors.py : just some colors definition.
import Matrix	# Matrix.py : simple module to manipulate matrix, for the board.
import Board	# Board.py : two classes Board.Board and Board.State.
import KeyBinding	# KeyBinding.py : implements the key binding.
import ParseMessageOut	# ParseMessageOut.py : pretty printing of data types, for exchange on the net.
#:import ToolReadline	# ToolReadline.py : make sure that raw_input is used as it have to.
##############################################################################
from Constants import *
from AffichPygame import *

#####################################
#### Creating the game variable. ####

def initGame(lx=LX_CST, ly=LY_CST, nb=NB_PLAYER, server=(SERVEUR_INIT, PORT_INIT)):
	""" Creating all Game variables."""
	# Pseudos and colors for players
	pseudos, colors = pseudos_colors(nb)
	# Start position
	Mi, Mj=start_position(TYPE_MAP, lx, ly, nb)
	# This one is always like this.
	nbmax=len(pseudos)
	if nbmax>NB_PLAYER or 0>nbmax:
	 sys.exit(ANSIColors.sprint("\n\t/E/ <red>Nb of players (=len(players)) have to be strictly in [|1;%i|] !<white>" % NB_PLAYER))

	# Example of list of player.
	pl=list()
	for i in range(nbmax):
#:		pl.append(Player.Player(info_server=server, pseudo=pseudos[i], color=colors[i]))
		pl.append(Player.PlayerServer(pseudo=pseudos[i], color=colors[i]))
		# Just a try about creating the players FIXME
#:		ANSIColors.printc("\t/n/ This player is number #%i, id=%i <blue>Tap '?' or 'help' for help<white>\n%s" % (i, pl[i].id, keyBindingList[i].get_help()))

#:	atexit.register(closeAll, pl=pl)	#: FIXME

	# Convert players to state
	spl=list()
	for i in range(nbmax):
	 spl.append(Board.State(wall=False, players=[pl[i]]))

	# Initialize the board
	board = Board.Board(Board.empty, lx, ly)
	print board

	for i, j, spot in board:		#: ok.
		newspot = copy.copy( random.choice( [Board.dmur, Board.empty] ) )
		if PROBA_UMUR > random.random():
		 newspot = copy.copy( Board.umur )
#:		print newspot	#: DELETE
		newspot.players = copy.copy([])
		board[i,j] = copy.copy(newspot)
	print board

	for i in range(nbmax):
		# do not use copy.copy here : spl[i] are pointers to pl[k]
		pl[i].move(Mi[i],Mj[i])
		board[Mi[i], Mj[i]] = spl[i]
	print board
	# Initialize the board
		#:	board=Board.Board(Board.empty, lx, ly)

		#:	for i in range(lx):
		#:	 for j in range(ly):
		#:	  # FIXME : it is NOT normal that I'm obliged to fix it here. (no players initially)
		#:	  if (i==2 or i==lx-3) or (j==2 or j==ly-3):
		#:	   board[i,j]=copy.copy(Board.State(wall=True, destr=True))
		#:	  if (i==2 or i==lx-3) and (j==2 or j==ly-3):
		#:	   board[i,j]=copy.copy(Board.State(wall=True, destr=False))
		#:	  board[i, j]=copy.copy(board[i, j])
		#:	  board[i, j].players=copy.copy([])

		#:	for i in range(nbmax):
		#:		# do not use copy.copy here : spl[i] are pointers to pl[k]
		#:		pl[i].move(Mi[i],Mj[i])
		#:#:		board.mat.mat[Mi[i]][Mj[i]]=spl[i]
		#:		board[Mi[i],Mj[i]] = spl[i]
	return (nbmax, lx, ly, pl, board, Mi, Mj)

######################
#### Using Pickle ####

def save_current_game(variables_to_save, info="variables_to_save"):
	""" Save all variables content the list *variables_to_save*, in a .pkl file.
	
	The game can be restored then, by setting all variables equals
	 to their previous values
	 (**of course** this only work if the .pkl file is still there)."""
	ANSIColors.writec("<reset><white>\n")
	return ParseMessageOut.try_pickling(variables_to_save, info=info)

########################
#### Principal Loop ####

def main(nbmax, lx, ly, pl, board, Mi, Mj, verb=verb, verb2=verb2, keyBindingList=keyBindingList):
	""" Big loop to test some behaviour.
	How to print bombs and bonuses in text mod ?
	How to move players, allow theme to drop bombs ?
	Make bombs explosion ?
	
	There are a lot of stuff to work arround !
	
	Parameters:
	===========
		* [nbmax]	Is max number of players,
		* [lx], [ly]	Are lenght of the board,
		* [pl]	Is the list of player (represented as Player.Player instances),
		* [board]	Is ... the board (represented as Board.Board instance !),
		* [Mi], [Mj]	Are list of players' position to initiate the game,
		* [verb], [verb2]	Are option for verbosity of the game,
		* [keyBindingList]	Is a KeyBinding.KeyBinding to map key to moves.
			For now, just ONE key (from a to z, A to Z, or ASCII caracters e.g. ~?;/ etc...).
	"""
	# Use initialization from AffichPygame.
	# Initialization of the pygame window.
	pygame.init()
	# Initialization of music mixer.
	pygame.mixer.init()
	# Resolution of the screen.
	resX, resY = RESOLUTION_X*lx, RESOLUTION_Y*ly
	screen = pygame.display.set_mode((resX, resY))
	pygame.display.set_caption('.: Bomberman - MPRI - 1-21 - (c) Lilian BESSON :.')
	# Background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((14, 0, 0))	#: A dark brown.
	global spotsSprites
	# Make the sprites for the spots.
	spotsSprites = listsprite_of_board(board)
	# Make the window.
	screen.blit(background, (0, 0))
	pygame.display.flip()
	# Initialization of the clock frequency.
	clock = pygame.time.Clock()
	ANSIColors.printc("\t/pygame/ <INFO> The screen is initializing with resolution (%i,%i) (in pixels: %i,%i).<white>" % (lx,ly, resX,resY))
	# Launching the music.
	pygame.mixer.music.load('datas/sound/' + MUSIC_loop)
	pygame.mixer.music.play(-1)
	# Change how to print boxes of the board (|-+/\\ or nonANSI)
	if Board.UTFSupported:
		board.mat.box=Matrix.boxnoASCII
	else:
		board.mat.box=Matrix.boxASCII
	ANSIColors.writec("\a\n\t/s/ <green>Bomberman game is going to start ... <white>\n")
	nb_turn=1
	try:
		# Handle exceptions
		while True:
		 #: To ensure that the printing is not too quick.
		 clock.tick(CLOCK_FREQUENCY)
		 # Infinite loop, may quite with all players' death except one.
	 	 # FIXME : try to simulate "synchronisation" step
	 	 assert(len(pl) > 0)
 		 save_current_game((nbmax, lx, ly, pl, board, Mi, Mj), info="(nbmax, lx, ly, pl, board, Mi, Mj)")
#:	 	 pl[0].send(ParseMessageOut.str_of_board_and_player(board, pl), True)
	 	 for event in pygame.event.get():
			if event.type == QUIT:
				return (nbmax, lx, ly, pl, board, Mi, Mj)
			elif event.type == KEYDOWN:
				ANSIColors.printc("\t/pygame/ <warning> A key have been pressed : %i => %s.<white>" % (event.key, KeyBinding.print_keynum_as_str(event.key)))
				if event.key == K_ESCAPE:
					return (nbmax, lx, ly, pl, board, Mi, Mj)
				if event.key == K_RIGHT: ANSIColors.printc("\t/pygame/ <INFO> Moving right.<white>")
				if event.key == K_LEFT: ANSIColors.printc("\t/pygame/ <INFO> Moving left.<white>")
				if event.key == K_UP: ANSIColors.printc("\t/pygame/ <INFO> Moving up.<white>")
				if event.key == K_DOWN: ANSIColors.printc("\t/pygame/ <INFO> Moving down.<white>")
				if event.key == K_SPACE: ANSIColors.printc("\t/pygame/ <INFO> Dropping bomb.<white>")
		 for k in range(nbmax):
			player=pl[k]
		 	# Loop over player. k is an index of a player.
		 	print_clear(board)
		 	# PYGAME stuff.
			spotsSprites = listsprite_of_board(board)
			screen.blit(background, (0, 0))
			pygame.display.flip()
			spotsSprites.update()
			spotsSprites.draw(screen)
			# Print.
			pygame.display.flip()
		 	# Clear the screen, and print the [board] (using Board.Board.__str__)
			for itmp in range(board.lx):
			 for jtmp in range(board.ly):
			  if board.mat[itmp,jtmp].explosion: board.mat[itmp,jtmp].explosion=False
		 	# The explosion is just print once
		 	if verb2:
			 	tmp="\t/P/ "
			 	for kk in range(nbmax):
			 	 tmp+=("PV[%s]=%i;" % (pl[kk], pl[kk].pv))
			 	ANSIColors.printc("<white>%s<white>" % tmp)
			 	# If verb2, print all players' PV
			# Store old positions
#:			Mi_old=Mi
#:			Mj_old=Mj
			i=Mi[k]
			j=Mj[k]
		 	# get moves
#:		 	sys.stdout.flush()
			try:
			 inp='K_'+raw_input("[Turn %i] Move for player #%i (this player is :[%s]) located in (%i,%i) =? " % (nb_turn, k, player, i, j))
			 len(inp)
			except KeyboardInterrupt:
			 ANSIColors.printc("\a\n\t/raw_input/ <red>FAIL !<white>  Maybe you hit ^C or ^D ?\n")
			 raise KeyboardInterrupt
#:		 	sys.stdout.flush()
			if inp in ["="]:	#: Save the game *rigth* now.
 				save_current_game((nbmax, lx, ly, pl, board, Mi, Mj), info="(nbmax, lx, ly, pl, board, Mi, Mj)")
			if inp in ["!", "$", "stop"]:
				raise KeyboardInterrupt
			if inp=="":
				continue
				# Do nothing.
			if keyBindingList[k].ok(inp, 'help'):
				ANSIColors.printc("\t/h/ <blue>Tap '?' or 'help' for help<white>\n%s" % keyBindingList[k].get_help())
				continue
			move_to_send=""
			bool_action=False
			#: Analyse moves, validate them, update the new position
			#: but this new position (i,j) will be checked later.
			if keyBindingList[k].ok(inp, 'up'):
				if i>0: move_to_send+="UP"
				if verb2: ANSIColors.printc("\t/u/ <blue>Player #%i <white>[%s]<white> wants to go <green>up<white>." % (k, player))
				i=max(0,i-1)
			if keyBindingList[k].ok(inp, 'down'):
				if i<lx: move_to_send+="DOWN"
				if verb2: ANSIColors.printc("\t/d/ <blue>Player #%i <white>[%s]<white> wants to go <green>down<white>." % (k, player))
				i=min(lx-1,i+1)
			if keyBindingList[k].ok(inp, 'left'):
				if j>0: move_to_send+="LEFT"
				if verb2: ANSIColors.printc("\t/l/ <blue>Player #%i <white>[%s]<white> wants to go <green>left<white>." % (k, player))
				j=max(0,j-1)
			if keyBindingList[k].ok(inp, 'right'):
				if j<ly: move_to_send+="RIGHT"
				if verb2: ANSIColors.printc("\t/r/ <blue>Player #%i <white>[%s]<white> wants to go <green>right<white>." % (k, player))
				j=min(ly-1,j+1)
			if keyBindingList[k].ok(inp, 'bomb'):
				if board[i,j].bomb:
				 ANSIColors.printc("\t/!/ <u><red>This is not allowed<U><black>, you cannot drop a second bomb <u>here<U>.<white>")
				elif player.nb_bomb >= NB_BOMB_MAX_ALLOW:
				 ANSIColors.printc("\t/!/ <u><red>This is not allowed<U><black>, you cannot drop a new bomb on the board (max allow : %i).<white>" % NB_BOMB_MAX_ALLOW)
				else:
				 move_to_send+="BOMB"
				 board[i,j].bomb=player.drop() # a new bomb
				 bool_action=True
			# If the new place is new, and is not a wall, move the player to it
			if verb2 and (move_to_send != "BOMB") and bool_action: ANSIColors.printc("\t/w/ <green>Player #%i<white> wants to move from (%i,%i) to (%i,%i)." % (k, Mi[k], Mj[k], i, j))
			if (move_to_send != "BOMB"):
				if (not board[i,j].wall) and ((i != Mi[k]) or (j != Mj[k])):
	#				player=board[Mi[k], Mj[k]].players.pop()
	# FIXME 
					board[Mi[k], Mj[k]].players.remove(player)
					if verb: print "\t/o/ Old spot : (%i, %i) => %s" % (Mi[k], Mj[k], repr(board[Mi[k], Mj[k]]))
					board[i,j].players.append(player)
					# here the move is really stores
					if verb2: ANSIColors.printc("\t/w/ <green>Player #%i<white> well moved from (%i,%i) to (%i,%i)." % (k, Mi[k], Mj[k], i, j))
					Mi[k]=i
					Mj[k]=j
					# Try to store positions internally in the players
					player.move(i,j)
					bool_action=True
					if verb: print "\t/n/ New spot : (%i, %i) => %s" % (i, j, repr(board[i, j]))
				elif board[i,j].wall:
					if verb2: ANSIColors.printc("\t/!/ <green>Player #%i<white> can not move from (%i,%i) to (%i,%i) because there is a wall in the wanted spot." % (k, Mi[k], Mj[k], i, j))
				elif i==Mi[k] and j==Mj[k]:
					if verb2: ANSIColors.printc("\t/!/ <green>Player #%i<white> can not move from (%i,%i) to (%i,%i) because there is the natural limitation of the board." % (k, Mi[k], Mj[k], i, j))
				else:
					if verb2: ANSIColors.printc("\t/!/ <green>Player #%i<white> can not move from (%i,%i) to (%i,%i)." % (k, Mi[k], Mj[k], i, j))
			if move_to_send and bool_action:
#:#:#			 move_to_send=("MOVE(id=%i;%s)" % (player.pseudo, player.color))+move_to_send+")"
			 move_to_send=ParseMessageOut.str_of_move(move_to_send)
#:			 ANSIColors.printc("\t/#/ <green>Player #%i<white> try to send a message [%s] to the server %s. He is known as %s." % (k, move_to_send, str(player.info_server), str(player.info_connection)))
#:		 	 try:
		 	  #FIXME a test to send all moves sequences to the server
#:			  player.send(move_to_send, verb or verb2)
#:			 except:
#:			  print "\t/F/ Failure : %s send %s. Verbosity=%s" % (str(player), move_to_send, str(verb or verb2))
				
		 board.tic(1, True) # Handle all bombs
		 ANSIColors.printc("\t/t/ <blue>New turn !<white>")
		 nb_turn+=1
	# Handling of all uncaugth exception
	except:
		raise
#:	except Exception as e:
#: 		save_current_game((nbmax, lx, ly, pl, board, Mi, Mj), info="(nbmax, lx, ly, pl, board, Mi, Mj)")
#:		closeAll(pl)
#:		ANSIColors.printc("\n\t/!/ <red>Game closed !<black> nicely close all players : TODO<white> %s" % e)
#:		raise e

###############
##### End #####

if __name__ == '__main__':
	#: import argparse #: No longer used here. FIXED.
	import ParseCommandArgs
	#: Generate the parser, with another module.
	#: This variable is the preprocessor, given to description and epilog by ParseCommandArgs,
	#:  * erase: to print with no colors.
	#:  * sprint: to print with colors.
	preprocessor = ANSIColors.sprint if ANSIColors.ANSISupported else ANSIColors.erase 	#:preprocessor = __builtin__.str, if you wanna to *see* the balises.
	#: Generate the parser, with another module.
	parser = ParseCommandArgs.parser_default(\
		description='<green>SimpleGame <red>module<reset> and <blue>script<reset>.',\
		epilog="""\n\
<yellow>About:
======<reset>
 A lot of tests.""", \
		version=__version__, date=__date__, author=__author__, \
 		preprocessor=preprocessor)
	#: Description for the part with '--file' and '--generate' options.
	group = parser.add_argument_group('A SimpleGame test', preprocessor("""\
<b>**THIS** <u>is a test<U>. So, use it for tests ... <reset>
"""))
	#: Remember that action can be used to many things.
	group.add_argument("-s","--server", help="The address of the server (eg '138.231.139.1', or 'bomberman-server.crans.org').") #:, required=True)
	group.add_argument("-p","--port", type=int, help="The port on which the connection to the server will be established (eg 9312, or 12882).\n\t This port *have* to be an open port on your machine **and** have to be the listened port of the server !") #:, required=True)
	# A group for handling save restore
	group = parser.add_argument_group('Saving and restoring previous sessions :', preprocessor("""\
<b>This program <u>save his state<U> (the board, list of players etc) during the session<reset>,
 so if there is a problem, the last valid state of the game will be keeped.
And this program can of course restore such a state, to restart from where it was !
"""))
	group.add_argument('-l', '--load', help=preprocessor(""" If present, the server will try to restart a previously close session."""), action="store_true")
	group.add_argument('-f', '--file', help=preprocessor(""" Try to load the savegame from the file FILE if possible, launch a <red>new one<reset> if not."""))
	#: The parser is done,
	#: Use it to extract the args from the command line.
	args = parser.parse_args()
	#: Use those args.
	##################
	verb=(args.verbose >= 1) or verb	#: Default = True
	verb2=(args.verbose >= 2) and verb2	#: Default = False
	# Print with ANSI escape code for colors if possible
	ANSIColors.ANSISupported=(not(args.noANSI) and ANSIColors.ANSISupported) or args.ANSI
	# Disable all escape codes for color to be generated 
	if not(ANSIColors.ANSISupported):
		ColorOff()
	else: ColorOn()
	ANSIColors.printc("\t/!/ ANSI escape code for colors supports = <green>%s<white>." % ANSIColors.ANSISupported)
	# Print with non ASCII caracters for boxes if possible
	Board.UTFSupported=not(args.noUTF) and Board.UTFSupported
	ANSIColors.printc("\t/!/ UTF escape code for boxes supports = <green>%s<white>." % Board.UTFSupported)
	# Set the server and the port
	server = args.server if args.server else SERVEUR_INIT
	port = int(args.port) if args.port else PORT_INIT
	##########################################
	#: If a save game is available, load it !
#:	try:
	if args.load:
	 ANSIColors.printc("\t/load/ <yellow>Trying to load<reset><white> \tthe game from a save file<reset><white>...")
	 from ParseMessageIn import try_unpickling
#:	 import Constants
	 if args.file:
	  nbmax, lx, ly, pl, board, Mi, Mj=try_unpickling("(nbmax, lx, ly, pl, board, Mi, Mj)", fn=args.file)
	 else:	# use the default value !
	  nbmax, lx, ly, pl, board, Mi, Mj=try_unpickling("(nbmax, lx, ly, pl, board, Mi, Mj)")
	 for i in range(lx):
	  for j in range(ly):
	   board[i,j] = copy.copy(board[i,j])
	   board[i,j].players = copy.copy(board[i,j].players)
	 ANSIColors.printc("\t/load/ <green>Succeed to load<reset><white> \tthe game from a save file<reset><white>...")
#:	except Exception as e:
	else:
	 e = "<yellow>-l neither --load found if the argument.<reset>"
	#: Otherwise create a new game.
	 ANSIColors.printc("\t/load/ <u><red>Failed to load<reset><white> \tthe game from a save file...\n\t/load/ Cause : %s" % e)
	 ANSIColors.printc("\t/init/ <yellow>The game will run on the server : (%s:%i)<reset><white>" % (server, port))
	 nbmax, lx, ly, pl, board, Mi, Mj = initGame( server=(server, port))
	# The game is initialized
	###############################################
	main(nbmax, lx, ly, pl, board, Mi, Mj, verb=verb, verb2=verb2)

#END
