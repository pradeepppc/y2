#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" Generical classe and functions from Pygame to make the graphical user interface (GUI).
This script provides shortcuts and utilities to *other modules*,
but it can also be used to check the compatibility with *pygame*.

 In a terminal, launching the scrit, with **$ ./AffichPygame.py**, will launch a demo.

 .. warning::
    The *Python* binding to **SDL**, **Pygame**, is **required** for the project as well as for this demo.

Example:
========
  This show how the **graphical window** *looks like during the game* (for the *client*) :

.. image:: images/exemplegraphical.png
   :scale: 80 %
   :align: center

About:
------
 This module use the datas store in **./datas/** folder.
  * The sprites are made with '.png' pictures, usually this is supported on every platform;
  * The soundtrack is made with '.mp3' tracks.

 .. warning::
    On some Linux distribution *mp3* are not supported !
     Maybe we have to install some *extra* libs.
    Or maybe you don't have a sound server.

 .. hint::
    You can disable music for the client and the bot with the *--nomusic* and *--nosoundeffect* options.

Soundtrack:
===========

.. For more details about soundtrack, the file `sound/README <../../datas/sound/README.md>`_ can be usefull.
.. include:: datas/sound/README.md

Pictures:
=========

.. For more details about the pictures, the file `48_48/README <../../datas/48_48/README.md>`_ can be usefull.
.. include:: datas/48_48/README.md

.. warning::
   When the main window is initialized, this module try to set her *icon*.
    Sometime it works : so you can see a nice *bomberman* player as an icon for your window.
    Sometime it doesn't.
    I wasn't able to understand why this seems to act *randomly*, sorry.

TODOs:
======
 * Try to update the sprite only when it changed.
 * Find a cool sound for game over.
"""

__author__='Lilian BESSON'	#: Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__email__='lilian.besson[AT]normale.fr'
__version__='1.0a'	#: Version of this module
__date__='dim. 17/02/2013 at 17h:24m:38s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

try:
	#1###############
	# Usual Modules #
	import os, sys, random, copy, time
	import thread
	#2#################
	# Project Modules #
	from Constants import *
	# FIXME
	# try:
	# 	if RUNNING_BOT:
	# 		USE_DIRECTION_FOR_PLAYER = False
	# 		print "Running a bot, so I disable the option USE_DIRECTION_FOR_PLAYER (regardless of the value in Constants.py)."
	# 	# else:
	# 	# 	USE_DIRECTION_FOR_PLAYER = True  # FIXME ?
	# except:
	# 	print "Not running a bot, so I might use the option USE_DIRECTION_FOR_PLAYER (if enabled in Constants.py)."
	import ANSIColors
	import KeyBinding
	import Player
	import ParseMessageIn, ParseMessageOut
	#####################
	# Pygame
	import pygame
	# Initialization of the pygame window.
	pygame.init()
	# Initialization of the music mixer.
	if USE_MUSIC: pygame.mixer.init()
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write(ANSIColors.sprint("\t<warning> <ERROR> <red>Fail<white> to launch module %s." % (err)))
	sys.exit(2)

########################################################
##### All resources (picture & music) for the game #####

#:Make your own `here <http://www.softicons.com/icon-tools/icon-converter>`_
#: Two different mode will be available : **48x48** and **32x32**.
#:
#:.. warning::
#:   By now, the 48x48 is **the only one** valid.
RESOLUTION_X, RESOLUTION_Y = 48, 48

# List of pictures (to make sprites).

PICTURE_block_destr = "block_destr.png"	#: For a destructible spot.
PICTURE_block_solid = "block_solid.png"	#: For an undestructible spot.
PICTURE_explosion = "explosion.png"
PICTURE_player = "player%i.png"		#: For players.
PICTURE_player_direction = "player_%s.png"		#: For players.
PICTURE_bomb = "bomb%i.png"		#: For bombs.
PICTURE_bonus = "bonus_%s.png"		#: For bonuses.
PICTURE_block_bonus = "block_bonus.png"	#: For a spot with a bonus.

# List of music (to make soundtrack).

MUSIC_world_clear = "world_clear.mp3"		#: When a player (not the active one) win the game.
MUSIC_bonus_main = "item.mp3"			#: When the active player get a bonus.
MUSIC_explosion = "explosion.mp3"		#: When a bomb is exploding.
MUSIC_loop_list = ["battle.mp3", "oeuf.mp3", "menu.mp3"]	#: Random : choose from this list !
#MUSIC_loop = random.choice(MUSIC_loop_list)	#: For the main loop.

def MUSIC_loop():
	""" MUSIC_loop() -> music file name
	"""
	return random.choice(MUSIC_loop_list)	#: For the main loop.

########################################################
#### Tool functions to interact with datas database ####

def color_to_number(color):
	""" Convert one of the following color ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'],
	 to an integer between 1 and 8 (to choose the right picture)."""
	if color == "black":		return 1	#: Bomberman classic !
	elif color == "red":		return 2	#: Mario 2 !
	elif color == "green":		return 8	#: Link !
	elif color == "yellow":		return 4	#: Pikachu !
	elif color == "blue":		return 7	#: Sonic !
	elif color == "magenta":	return 6	#: Pac-Man !
	elif color == "cyan":		return 5	#: Wizard !
	elif color == "white":		return 3	#: Mario 1 !
	else: return 0	#: This case **cannot** happen.

def load_tile_table(filename, width, height):
    """ A test to use a picture as an array of sub pictures.
    """
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

def namePicture_of_SpriteSpot(state, verb = False):
	""" Give the name of the picture used to print the *state*.

	If more than one player is in the same spot, return the first one.

	See how return more than one pictures,
	 and make a blur effect to show all of the returned pictures.
	"""
	if verb:	print "namePicture_of_state : state = %s." % str(state)
	if state.explosion and not( state.destr and state.wall ):
		return PICTURE_explosion
	if state.bomb:
		return (PICTURE_bomb % state.bomb.power)
	if state.wall:
		if state.destr:
		 return PICTURE_block_destr
		return PICTURE_block_solid
#:	if state.bonus:	# FIXME not implemented
#:		kind = state.bonus.kind[1:]
#:		return (PICTURE_bonus % kind)	#: ex. kind = ice --> 'bonus_ice.png'
	if state.players:
		# if USE_DIRECTION_FOR_PLAYER:  # FIXME
		if USE_DIRECTION_FOR_PLAYER and not('_IA_' in state.players[0].pseudo):
			return (PICTURE_player_direction % state.players[0].direction)
		# FIXME experimental.
		return (PICTURE_player % ( 1+(state.players[0].id % 8) ))
#:		return (PICTURE_player % (color_to_number(state.players[0].color)))
	else:
#:		ANSIColors.printc("\t/pygame/ <WARNING> Fail when trying to put a picture name for the state: %s <reset> (repr=%s)<white>" % (str(state), repr(state)))
		return "!! NOTHING_TO_LOAD !!"

####################################
##### Load music and pictures ######

def load_png(name, verb = False):
	""" Load a picture, and return a image object.

	The picture **have to be** in the folder *./datas/48_48/*, or *./datas/32_32/*,
	 otherwise, error might occur quickly :s !

	About:
	 A lot of pre set pictures are from softicons.com,
	 and a few of them where made by their tools [http://www.softicons.com/icon-tools/icon-converter]."""
	fullname = os.path.join('datas/%i_%i/' % (RESOLUTION_X, RESOLUTION_Y), name)
	if verb:	ANSIColors.printc("\t/pygame/ <INFO> Trying to load the picture : %s <reset><white>" % fullname)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except:
		if verb:	ANSIColors.printc("\t/pygame/ <ERROR> Fail when loading the picture :%s <reset><white>" % fullname)
		raise
	return image, image.get_rect()

def play_music(name, number=-1, volume=1.0, time=0.0, verb = True):
	""" Load a music. Set the volume to *volume*, and play it *number* time.
	To play in loop, set *number=-1*.

	The music **have to be** in the folder *./sound/*,
	 otherwise, error might occur quickly :s !

	**About the soundtrack:**
	 The default soundtrack is from many different sources.
	 This is an exhaustive list :
	  * Pokemon Red (Nintendo (c) 1995 - GameFreak);
	  * The Legend of Zelda - Ocarina of Time, Link's awakening (Nintendo (c) 1991 & 1997);
	  * Super Mario World 1 (Nintendo (c) 1985);
	  * Super Smash Bros Melee (Nintendo (c) 2001 - HAL Laboratory).

	**Copyrigths:**
	 The game is released under the *GPLv3 Licence,*
	  but the soundtrack **is not** distributed freely with the game (at least, not under a free licence).
	 Although, you can download it from the same source that the game (just not in the same archive).
	"""
	fullname = os.path.join('datas/sound/', name)
	if verb:	ANSIColors.printc("\t/pygame/ <INFO> Trying to load the music : %s <reset><white>" % fullname)
	try:
		pygame.mixer.music.set_volume(volume)
		pygame.mixer.music.load(fullname)
		pygame.mixer.music.play(number, time)
	except:
		if verb:	ANSIColors.printc("\t/pygame/ <ERROR> Fail when loading the music :%s <reset><white>" % fullname)
		raise

##############################################
#### One classe for the SDL printed board ####

class SpriteSpot(pygame.sprite.Sprite):
	""" A simple class for a spot (instance of Board.State) in the board.
	This one is more oriented around moves by direct order.

	FIXME: use update ?
	"""

	def __init__(self, state, pos=(0, 0)):
		""" Spot is a wrapper around Board.State, and state is attend to be one of this."""
		self.state = state #: The Spot contain a state.
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png(namePicture_of_SpriteSpot(state))
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.speed = RESOLUTION_X
		self.movestate = "still"
		self.movepos = [0, 0]
		self.reinit(pos)

	def reinit(self, pos):
		""" Initialize the sprite, make it stable."""
		self.rect.move_ip(pos)
		self.movestate = "still"
		self.movepos = [0, 0]

	def update(self):
		""" Update the position of the sprite.

		For now, it is done **stupidly** : the sprites are all recomputed each turn.
		FIXME: make sure this is done more cleverly."""
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

#################################################################
#### Convert a Board.Board to a list of pygame.sprite.Sprite ####

TRY_UPDATE_CLEVERLY	= False	#: If true, try to update ony the changed sprites.
oldboard		= "not yet :("

def listsprite_of_board(board, verb = False):
	""" listsprite_of_board(board, verb = False) -> pygame.Sprites
	"""
	spots = []
	if verb:	print_clear(board)
	for i, j, spot in board:		#: ok.
	 update = True
	 if TRY_UPDATE_CLEVERLY:
		 try:		update = (spot != oldboard[i, j])	# if possible, try to not update the sprite.
		 except:	pass
	 if update:
	  try:
	   if namePicture_of_SpriteSpot(spot, verb=verb) != "!! NOTHING_TO_LOAD !!":
	    spots.append(SpriteSpot(spot, pos=(RESOLUTION_Y*j, RESOLUTION_X*i)))
	  except Exception as e:
	   ANSIColors.printc("\t/pygame/ <ERROR> PB when converting %s to a sprite. Cause : %s.<reset><white>" % (repr(spot), e))
	   pass
	oldboard = board	#: FIXME
	return pygame.sprite.RenderPlain(spots)

###############################################################################
def toggle_explosion(board, pl, clock, MAKE_DESTROY=False, num_thread=0, FORCE=False, \
	print_on_all=None, list_clients=None, origin=None, player = None):
 """toggle_explosion(board, pl, clock, MAKE_DESTROY=False, num_thread=0) -> infinite loop
 A small function to toggle explosions tag when they have to be erased.

 On the *server*, **MAKE_DESTROY** is True, and is False on the client.

 Have to be threaded too.
 """
 try:
 	ANSIColors.printc("""
/toggle_explosion/ <neg>Thread number %i<Neg> : initialized. Infinite loop (freq=%i) to handle explosion...
%s
""" % ( num_thread, CLOCK_FREQUENCY, str(board) ))
	while True:
		clock.tick(TIME_EXPLOSION)
		for itmp ,jtmp, spottmp in board:
			board[itmp, jtmp].explosion = False
		board.tic(toc=1, MAKE_DESTROY=MAKE_DESTROY, FORCE=FORCE, \
			print_on_all=print_on_all, str_of_blowbomb=ParseMessageOut.str_of_blowbomb,\
			list_clients=list_clients, origin=origin)
		# print_clear(board)  # FIXME do not print the board constantly ?
		# print_pvs_player(pl)
###############################################################################
 # End of the game (GameOver).
 except ParseMessageIn.GameOver as e:
    player2, msg = e.player, e.msg
    if player:
	if player2.id == player.id:
		ANSIColors.printc("""
<warning>\t/end of the game/ <green> You win !!<white> You received the message '%s'.
""" % msg)
		ANSIColors.printc("""
<warning>\t/end of the game/ <green> The game is closing now.<white>""")
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
    else:
    	ANSIColors.printc("<warning> <red>on toggle_explosion (server side), I picked up a GameOver exception... <neg>%s<Neg>.\n/restarting toggle_explosion/" % str(e))
    	print_on_all( ParseMessageOut.str_of_gameover(player2), list_clients, origin )
    	# End of the game.
    	return True
#:    	toggle_explosion(board, pl, clock, MAKE_DESTROY, num_thread, FORCE, \
#:		print_on_all, list_clients, origin, player)
###############################################################################
 # Death of players.
 except Player.PlayerDeath as e:
    player2, ingury, msg = e.player, e.ingury, e.msg
    if player:
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
    else:
    	ANSIColors.printc("<warning> <red>on toggle_explosion (server side), I picked up a PlayerDeath exception... <neg>%s<Neg>.\n/restarting toggle_explosion/" % str(e))
    	toggle_explosion(board, pl, clock, MAKE_DESTROY, num_thread, FORCE, \
		print_on_all, list_clients, origin, player)
###############################################################################
# End of the main loop (shall not happen).
 except:
  sys.stderr.write(ANSIColors.sprint("""
<warning>	/toggle_explosion/ <neg>Thread number %i<Neg> : failed with exception <neg>%s<Neg>.
	/toggle_explosion/ Now it will try to kill the caller (with <red>thread.interrupt_main()<white>).
""" % ( num_thread, str(sys.exc_info()[1]) )))
  sys.stderr.flush()
  thread.interrupt_main()
#:  raise
 os._exit(1)

######################################################################################
#### Main loop, for tests only (in fact, this have to be done in BombermanClient) ####

def main(nbmax, lx, ly, pl, board, Mi, Mj, verb = False):
	""" The main loop for **testing**.

	Notice that every thing here will have to be put **in the correct spot** in BombermanClient."""
	# Initialization of the pygame window.
	pygame.init()
	# Initialization of music mixer.
	if USE_MUSIC: pygame.mixer.init()
	# Resolution of the screen.
	resX, resY = RESOLUTION_X*lx, RESOLUTION_Y*ly
	if USE_FULLSCREEN:
		screen = pygame.display.set_mode((resX, resY), pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode((resX, resY))
	pygame.display.set_caption('.: Bomberman %ix%i (Res %ix%i) | MPRI 1.21 | (c) Lilian BESSON :.' % (lx, ly, resX, resY))
	pygame.display.set_icon( load_png("player.gif", verb = True)[0] )
	# Background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((20, 0, 0))	#: A dark brown.
	# Initialization of sprites for the game.
	spotsSprites = listsprite_of_board(board, verb=verb)
	# Make the window.
	screen.blit(background, (0, 0))
	pygame.display.flip()
	# Initialization of the clock frequency.
	clock = pygame.time.Clock()

#:	table = load_tile_table("datas/48_48/bomb_tiles.png", 24,24)
#:	for x, row in enumerate(table):
#:	  for y, tile in enumerate(row):
#:	    screen.blit(tile, (x*9, y*5))
#:	pygame.display.flip()

	ANSIColors.printc("\t/pygame/ <INFO> The screen is initializing with resolution (%i,%i) (in pixels: %i,%i).<white>" % (lx,ly, resX,resY))
	# Launching the music.
	if USE_MUSIC:
		time_main_loop = 0.0
		play_music(MUSIC_loop, time=time_main_loop, volume=0.50)
		ANSIColors.printc("\t/pygame/ <INFO> The Pygame music mixer is initialized, playing datas/sound/%s.<white>" % (MUSIC_loop))
	# This show what to put in the BombermanClient.main loop.
	while 1:
		#: To ensure that the printing is not too quick.
		clock.tick(CLOCK_FREQUENCY)

		for event in pygame.event.get():
			if event.type == QUIT:
				if USE_MUSIC:
				 ANSIColors.printc("\t/pygame/ <INFO> The Pygame music mixer is now playing datas/sound/%s.<white>" % (MUSIC_world_clear))
				 play_music(MUSIC_world_clear, number=1, volume=0.40)
				 pygame.mixer.music.fadeout(TIME_FADEOUT * 1000)
				return (nbmax, lx, ly, pl, board, Mi, Mj)
			elif event.type == KEYDOWN:
				ANSIColors.printc("\t/pygame/ <warning> A key have been pressed : %i => %s.<white>" % (event.key, KeyBinding.print_keynum_as_str(event.key)))
				if event.key == K_ESCAPE:
					if USE_MUSIC:
					 ANSIColors.printc("\t/pygame/ <INFO> The Pygame music mixer is now playing datas/sound/%s.<white>" % (MUSIC_world_clear))
					 play_music(MUSIC_world_clear, number=1, volume=0.40)
					 pygame.mixer.music.fadeout(TIME_FADEOUT * 1000)
					return (nbmax, lx, ly, pl, board, Mi, Mj)
				if event.key == K_RIGHT:
					ANSIColors.printc("\t/pygame/ <INFO> Moving right.<white>")
				if event.key == K_LEFT:
					ANSIColors.printc("\t/pygame/ <INFO> Moving left.<white>")
				if event.key == K_UP:
					ANSIColors.printc("\t/pygame/ <INFO> Moving up.<white>")
				if event.key == K_DOWN:
					ANSIColors.printc("\t/pygame/ <INFO> Moving down.<white>")
				if event.key == K_SPACE:
					ANSIColors.printc("\t/pygame/ <INFO> Dropping bomb.<white>")
					pygame.mixer.music.pause()
					time_main_loop = pygame.mixer.music.get_pos()
					play_music(MUSIC_explosion, number=1, volume=0.50)
					pygame.mixer.music.queue('datas/sound/' + MUSIC_loop())
				spotsSprites = listsprite_of_board(board)
		# Update.
		screen.blit(background, (0, 0))
		pygame.display.flip()
		spotsSprites.update()
		spotsSprites.draw(screen)
		# Print.
		pygame.display.flip()


if __name__ == '__main__':
	import SimpleGame
	# Create the board,
	try:
	 from ParseMessageIn import try_unpickling
	 nbmax, lx, ly, pl, board, Mi, Mj=try_unpickling("(nbmax, lx, ly, pl, board, Mi, Mj)")
	 for i in range(lx):
	  for j in range(ly):
	   board[i,j] = copy.copy(board[i,j])
	   board[i,j].players = copy.copy(board[i,j].players)
	 ANSIColors.printc("\t/load/ <green>Succeed to load<reset><white> \tthe game from a save file<reset><white>...")
	except Exception as e:
	 print e
	 server, port = SERVEUR_INIT, PORT_INIT
	 nbmax, lx, ly, pl, board, Mi, Mj = SimpleGame.initGame(server=(server, port))
	try:
	 nbmax, lx, ly, pl, board, Mi, Mj = main(nbmax, lx, ly, pl, board, Mi, Mj)
	except Exception as e:
	 print "ERROR:%s" % e
	if USE_MUSIC:
	 	time.sleep(TIME_FADEOUT)
	 	pygame.mixer.music.stop()
	if USE_WINDOW:  pygame.display.quit()
	ANSIColors.printc("\n\t/end/ <green>The game is done.<reset><white>\n")

#END#
