#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" This module implement two classes for Bomberman players, and one exception for their deaths.

PlayerServer:
-------------
 The class PlayerServer is a high-level representation of a Bomberman player, for the server.

Player:
=======
 The class Player is the same thing, but without additionnal *plumbing*, for the client.
 All the plumbing about connection to the server is *hidden*, using the socket module.

 The following method are availables to use network :
  * connect	-- to initialize the connection,
  * send	-- to send a message,
  * close	-- to close the connection.

Example:
--------
 And those methods *have to be used*, I don't want to see anything *durty* like :
  >>> f = player0.socket_player.mfile()
  >>> f.write("I can send messages to my server !")
  >>> f.close()
  >>> # Don't do this !

 The good way to do is :
  >>> player0.send("I can send messages to my server !")
  >>> # Do this !

.. warning::
   The player's pseudos are checked to be small enough, so they **have to be smaller than 32 caracters** (otherwise they will be cut).

"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.4c'
__date__='ven. 15/02/2013 at 22h:24m:29s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules #
import socket #, sys, atexit, thread

#2#################
# Project Modules #
import ANSIColors	# ANSIColors.py : just some colors definition.
import Bomb	# Bomb.py : implement the simple bomb system. (actions, representation etc)

##############################################################################

## Lists of constants for building a player.
from Constants import *
import ParseMessageOut

class PlayerDeath(Exception):
	""" Exception Class for handling the death of a Player.

	Attributes:
	 * player	-- the player which is dying.
	 * ingury	-- the ingury receive by the player.
	  (ex: player had 2 pv, and receive 3 damages : ingury=3).
	 * msg	-- the message annoucing the death, which have to be printed to the player.

	Example:
	 You can annouce the death of a player *player0* with this :
	  >>> raise PlayerDeath(player0, ingury=3, msg='You died :(')
	  >>> # In this example, player0 had 2 pv, and receive 3 damages : so he died.

	"""
	def __init__(self, player, ingury=1, msg=death_message_Init):
	 """ Construction of a PlayerDeath exception.
	 """
	 self.player = player	#: the player which is dying.
	 self.ingury = ingury	#: the ingury receive by the player.
	 self.msg = msg	#: the message annoucing the death, which have to be printed to the player.

	def __str__(self):
	 """__str__(self) -> str
	  A pretty string for the exception. (with colors if self.player supports color)."""
	 return "The player %s received %i ingur%s, so he is dying... The server sent the following message %s." % (self.player, self.ingury, "y" if self.ingury<2 else "ies", self.msg)

class PlayerServer(object):
	""" A Class to define a Bomberman player, **for the server**.

	Attributes:
	(About the player)

	 * pseudo	-- his pseudo.
	 	will be used for printing the player in the board in textual mode.
	 	It has to begin with a ASCII caracter, the other are free.
	 * color	-- his favorite color.
	 	can be one of the following : black, red, green, yellow, blue, magenta, cyan, white.

	(About his connection : here the player is **not yet** connected to the server)
	 * id	-- an integer representing the player uniquely both in the client and the server.
	  (for now, it's just PORT2 if there is a connection, or -1 if not).
	  PORT2 is the port of the socket of the client, as it is saw **FROM THE SERVER**.
	  But, no worry, everything is hidden !

	(About the party)

	 * pv	-- number of point of life (PV).
	 * nb_bomb	-- number of bomb dropped in the field (by default, this is limited to 1).
	 * x	-- his position in x axis,
	  (integer between 0 and Nx-1, dimension of the board, typically Nx=8 or 12).
	 * y	-- his position in y axis,
	  (integer between 0 and Ny-1, dimension of the board, typically Ny=8 or 12).
	 * templatebomb	-- the default bomb's caracteristic. This is a Bomb.BombNoOwner instance.
	 * direction	-- one of 'right', 'left', 'front', 'back'. Represent the last direction's move for the player.
	"""

	id_global = -1

	def __init__(self, pseudo=pseudo_Init, color=color_Init, pv=pv_Init,\
		 nb_bomb=nb_bomb_Init, x=x_Init, y=y_Init, templatebomb = Bomb.BombNoOwner()):
	 """ Simple constructor of a player, not yet connected to anything.

	 About:
	  * [id] is PORT2, the port of the socket assuring the connection between the player and his server,
	    as soon as available; and is an increasing integer (from 0) otherwise (increase by one for each new Player).
	  * *templatebomb* is the default bomb which will be dropped by the player.

	 Example:
	  >>> # On the server, for example hosted on the computer naereen-corp.crans.org,
	  >>> #  while listening to the port 9312, detect a new client, which claimed to be Naereen,
	  >>> #  and said to like green. So the server is creating a local version of the player, to the local version of the game.
	  >>> player0=PlayerServer("Naereen", "green")
	 """
	 # Increase this class attribute
	 PlayerServer.id_global = PlayerServer.id_global + 1
	 # All Player.PlayerServer instance attributes
	 self.pseudo = pseudo	#: his pseudo.
	 self.color = color	#: his favorite color.
	 self.pv = pv	#: number of point of life (PV).
	 self.nb_bomb = nb_bomb	#: number of bomb dropped in the field (by default, this is limited to 1).
	 self.x = x	#: his position in x axis,
	 self.y = y	#: his position in y axis,
	 self.templatebomb = templatebomb	#: the default bomb which will be dropped by the player.
	 self.id = PlayerServer.id_global	#: an integer representing the player uniquely both in the client and the server.
	 self.direction	= 'front'	# Default.

	def __str__(self):
	 """ A simple conversion from a Player to a string.
	 The string returned can be used to print informations about the player.
	 """
	 return ("%s%s%s%s" % (ANSIColors.tocolor(self.color), self.pseudo, ANSIColors.reset, ANSIColors.white))

	def __repr__(self):
	 """ Toplevel representation of [self]."""
	 return ("pseudo=%s; id=%i; color=%s; pv=%i; nb_bomb=%i; x=%i; y=%i; direction=%s; default bomb=(%s)" % (self.pseudo, self.id, self.color, self.pv, self.nb_bomb, self.x, self.y, self.direction, repr(self.templatebomb)))

	def drop(self):
	 """ Give the bomb dropped by a player, as a Bomb.Bomb instance.
	 Increase the current number of bomb owns by the player.
	 The returned Bomb.Bomb have a symlink to the Player in attribute *owner*.

	 Example:
	  >>> board[player1.x, player1.y].bomb = player1.drop()
	  >>> # Ok
	  >>> player1.move( i = player1.x + 1)
	  >>> # Move the player to the right by one (warning without checking !)
	  >>> board[player1.x, player1.y].bomb = player1.drop()
	  >>> # **NOT OK** the player cannot drop an other bomb (the max number is currently 1).
	 """
	 self.nb_bomb += 1
	 ANSIColors.printc("\t/B/ The player %s <green>dropped a bomb<white>. It's his %i nst." % (self, self.nb_bomb))
	 return Bomb.add_owner(self.templatebomb, self)

	def move(self, i=None, j=None):
	 """ A simple way to move the player from his spot to (i,j).

.. warning::
   The move **have to be valid**, **IT IS NOT RE CHECK HERE**.
   Therefore, i,j are checked to be **valid positive integers** here.

Example:

 Move the player to the right by one (without checking !) :
  >>> player1.move(player1.x + 1, player1.y)

Example 2:

 You can also specify only the direction to change :
  >>> player1.move(i = player1.x + 1)
	 """
	 if i==None: i=self.x
	 if j==None: j=self.y
	 if type(i)!=type(0) or type(j)!=type(0): return SIGNAL_TYPE_WRONG
	 if i<0: return SIGNAL_I_NEGATIVE
	 if j<0: return SIGNAL_J_NEGATIVE
	 else:
	 	if i < self.x:	self.direction = 'back'
	 	if i > self.x:	self.direction = 'front'
	 	if j > self.y:	self.direction = 'right'
	 	if j < self.y:	self.direction = 'left'
		self.x = i
		self.y = j
		return 0

	def hurt(self, ingury=1):
	 """ A shortcut to reduce the [pv] attribute of a Player by a number [ingury] of ingury.
 This method trigger here the eventual death of the player.
 Print an *ANSIColored* message to signal the death of the player in case.

.. warning::
   Might raise a PlayerDeath exception if the player dies after suffering [ingury].

Example :
 >>> i,j = player0.x, player0.y
 >>> if board[i, j].bomb:
 >>> 	player0.hurt(ingury = board[i, j].bomb.force)
 >>> else:
 >>>	print 'No ingury ! Ouf...'
	 """
	 self.pv -= ingury
	 ANSIColors.printc("\t<red>/h/ The player [%s<red>] have suffered %i damages.<white>" % (self, ingury))
	 if self.pv <= 0:
	  # Here, the player is dead.
	  raise PlayerDeath(self, ingury, ("{%s} is dead because he suffered %i damages." % (str(self), ingury)))
	  # On the server, this exception have to be handle nicely
	  # (e.g. by simply informing all other (alive) clients that [self] is dead.)
	 return ingury != 0

class Player(PlayerServer):
	""" A Class to define a Bomberman player, **for the client**.

	Attributes:
	(About the player)

	 * pseudo	-- his pseudo.
	 	will be used for printing the player in the board in textual mode.
	 	It **have to begin with a ASCII caracter**, the other are free.
	 * color	-- his favorite color.
	 	can be one of the following : black, red, green, yellow, blue, magenta, cyan, white.

	(About his connection : here the player **is** connected to the server)
	(Currently, pickling is in test, and __setstate__ and __getstate__ are used to save and restore the connection.)

	 * info_server	-- the information about a server on which he is connected to (a tuple (HOTS, PORT)). (new from Player.PlayerServer)
	 * socket_player	-- the socket identifying his connection, (HOST, PORT2), with PORT2 != PORT. (new from Player.PlayerServer)
	 * info_connection	-- a simple string containing (HOST, PORT2).
	 * id	-- an integer representing the player uniquely both in the client and the server.

	(About the party)

	 * pv	-- number of point of life (PV).
	 * nb_bomb	-- number of bomb dropped in the field (by default, this is limited to 1).
	 * x	-- his position in x axis,
	  (integer between 0 and Nx-1, dimension of the board, typically Nx=8 or 12).
	 * y	-- his position in y axis,
	  (integer between 0 and Ny-1, dimension of the board, typically Ny=8 or 12).
	 * templatebomb	-- the default bomb's caracteristic. This is a Bomb.BombNoOwner instance.

	Examples:
	 On each intersting methods here defined, an example is shown,
	  from creating a player, stored in 'player1', to several examples of methods.
	"""

	#: A strictly increasing integer.
	#:  Each new instance of *Player* have this number in his attribute *id*.
	id_global = -1

	def __init__(self, info_server=info_server_Init, pseudo=pseudo_Init, color=color_Init, pv=pv_Init,\
		 nb_bomb=nb_bomb_Init, x=x_Init, y=y_Init, templatebomb = Bomb.BombNoOwner()):
	 """ Simple constructor of a player.
	 He/She will be named [pseudo], and colorised [color], and connected on the server [info_server].
	 The connection is established with a socket, given by [socket_player] attribute.
	 ** This step could failed : so creating a connected player could failed. For now, it can't.

	 About:
	  * [info_server] is a tuple (HOST, PORT), giving the information about the server.
	     While there is no connection, it is ('None', id).
	  * [id] is PORT2 if there is a connection,
	     otherwise it is a unique integer (strictly increasing for each new Player.PlayerServer).
	  * *templatebomb* is the default bomb which will be dropped by the player.

	 Example:
	  >>> # For example on the computer client.crans.org, user 'Naereen', who likes green,
	  >>> # want to play on Bomberman with the server hosted at naereen-corp.crans.org, on the port 9312.
	  >>> player1=Player(('naereen-corp.crans.org', 9312), color="green", pseudo="Naereen")
	 """
	 # Increase this class attribute
	 Player.id_global = Player.id_global + 1
	 # All Player.PlayerServer instance attributes
	 self.pseudo = pseudo	#: his pseudo.
	 self.color = color	#: his favorite color.
	 self.pv = pv	#: number of point of life (PV).
	 self.nb_bomb = nb_bomb	#: number of bomb dropped in the field (by default, this is limited to 1).
	 self.x = x	#: his position in x axis,
	 self.y = y	#: his position in y axis,
	 self.templatebomb = templatebomb	#: the default bomb which will be dropped by the player.
	 self.direction	= 'front'	# Default.
	 #: About the id :
	 #:  an integer representing the player **uniquely both** in the client and the server.
	 #:  A good client shall receive it from the server (when phasis #2 begin).
	 self.id = Player.id_global
	 self.info_connection = ('<not yet connected>', self.id)	#: a simple string containing (HOST, PORT2).
	 #: the information about a server on which he is connected to (a tuple (HOTS, PORT)). (new from Player.PlayerServer)
	 self.info_server = info_server
	 self.socket_player = None	#: The connection is done in *connect*.
	 self.connect(info_server)

	def __repr__(self):
	 """ __repr__(self) <=> repr(self)
	  Representation of [self] as a string."""
	 return ("pseudo=%s; id=%i; color=%s; pv=%i; nb_bomb=%i; x=%i; y=%i; server=(%s); info_connection=(%s); default bomb=(%s)" % (self.pseudo, self.id, self.color, self.pv, self.nb_bomb, self.x, self.y, str_of_InfoServer(self.info_server), str_of_InfoServer(self.info_connection), repr(self.templatebomb)))

	def hurt(self, ingury=1):
	 """ A shortcut to reduce the [pv] attribute of a Player by a number [ingury] of ingury.
	 Handle here the death of the player.
	 Print an *ANSIColored* message to signal the death of the player in case.

	 Might raise a PlayerDeath exception if the player **dies** after suffering [ingury].

	 Example:
	  >>> i, j = player0.x, player0.y
	  >>> if board[i, j].bomb:
	  >>> 	player0.hurt(ingury = board[i, j].bomb.force)
	  >>> else:
	  >>> 	print "No ingury ! Ouf..."
	 """
	 self.pv -= ingury
	 ANSIColors.printc("\t<red>/h/ <u>YOU<U> [<white>%s<red>] have suffered %i damages.<white>" % (self, ingury))
	 if self.pv <= 0:
	 	# Here, the player is dead.
	 	raise PlayerDeath(self, ingury, ("<u>YOU<U> [<white>%s<red>] are dead because you suffered %i damages.\nGAME OVER !" % (str(self), ingury)))
	 return ingury != 0

	def connect(self, info_server=info_server_Init):
	 """ Try to connect to the server.
	 Exactly the same way it's done when creating the player.
	  except it raise exception properly here.

	 Example:
	  >>> # From the client, trying to connect to a new server.
	  >>> player1.connect('bomberman-server.crans.org', 13882)
	 """
	 if self.info_connection[0] != '<not yet connected>':
	 	ANSIColors.printc("\t/n/ Old connection was %s. <blue>Trying a new one to the server %s<white> ..." % (self.info_connection, info_server))
	 try:
	  self.socket_player = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	  self.socket_player.connect(info_server)
	  self.info_connection = self.socket_player.getsockname()
#:	  self.id = self.info_connection[1]
	  # Try to send the player's pseudo
	  self.send(ParseMessageOut.str_of_newplayer(self), True)
	  ANSIColors.printc("\t/!/ <green>Connection succeed to server %s<white> for player pseudo=%s; color=%s; pv=%i; <green>now seen as (%s), with id=%i.<white>" % (self.info_server, self.pseudo, self.color, self.pv, self.info_connection, self.id))
	 except socket.error as e:
	  ANSIColors.printc("\t/!/ <red><u>Connection refused (%s)<U> for the server %s<white> for player pseudo=%s; color=%s; pv=%i !" % (str(e), self.info_server, self.pseudo, self.color, self.pv))
	  raise e	#: have to do this for a Client player : the game
	  		#:  cannot start (and don't have to) if the server is unavailable.

	def close(self):
		""" Try to close nicely the connection with the server.
		"""
		self.socket_player.shutdown(socket.SHUT_RDWR)
		return self.socket_player.close()

	def send(self, msg="", v=True):
	 """ A try to send a message [msg] to the server.

	 About:
	  * [msg]	have not to terminate by a new line caracter (backslash + n), it is added automatically.
	  * [msg]	is not send if it's non empty.
	  * [v]	if true, print debug informations.

	 Example:
	  >>> # send a new color to the server, and change it locally
	  >>> player1.color='red'
	  >>> # but don't do this, use ParseMessage[In|Out] modules for this
	  >>> player1.send('color=%s' % player1.color)
	 """
	 try:
	  if msg:
		 mfile = self.socket_player.makefile()
		 if msg[-1]!='\n':
		 	mfile.write(msg+'\n')	# FIXME ?
		 else:
		 	mfile.write(msg)	# FIXME ?
		 mfile.flush()
#:		 if v:
		 ANSIColors.printc("<INFO> <neg>/Player.Player.send/ The player [%s, id=%i] <green>sent the message<white> [%s]<white> to his server [%s]." % (str(self), self.id, msg, str_of_InfoServer(self.info_server)))
		 return True
	  else:
		return False
	 except Exception as e:
		if v:
			ANSIColors.printc("<warning>\t/S/ <red>The player [%s<red>, id=%i] <u>fail<U> when trying to send<white> the message [%s] to his server <blue><u>[%s]<U><white>.\n\t/S/ <red>%s<white>." % (str(self), self.id, msg, str_of_InfoServer(self.info_server), e))
		return False

	def __getstate__(self):
		""" Used to save the Player.Player instance, for example with pickle.

Warning:
.. warning::
   The socket (attribute *socket_player*) is **not destroyed** by this operation,
   and the Player.Player *self* is **still** connected to his server.

Example of Saving:
 >>> output = open('player1.pkl', 'wb')
 >>> pickle.dump(player1, output, -1)
 >>> output.close()
		"""
		odict = self.__dict__.copy()	# copy the dict since we change it
		del odict['socket_player']	# remove socket entry
		ANSIColors.printc("\t/pickle/ Pickling the player %s. This player has id=%i, <yellow>but his un-pickling will change his id<reset><white> ..." % (str(self), self.id))
		ANSIColors.printc("\t/pickle/  His dictionary is : <neg>%s<Neg><white>." % str(odict))
		return odict

	def __setstate__(self, dict):
		"""  Used to reload the Player.Player instance, for example with pickle.

Warning:
.. warning::
   The socket (attribute *socket_player*) is **re created** by this operation,
   and the Player.Player *self* is **re connected** to his server.

Example of Loading:
 >>> pkl_file = open('player1.pkl', 'rb')
 >>> player1 = pickle.load(pkl_file)
 >>> pkl_file.close()
 >>> print player1 # !warning! : the connection is a new one.
		"""
		ANSIColors.printc("\t/pickle/ Remaking a player, with the dictionary : <black>%s<white>." % (str(dict)))
		self.__dict__.update(dict)	# update attributes
		ANSIColors.printc("\t/pickle/ Remaking the player %s. This player have now id=%i, <red>but his un-pickling had change his id<reset><white> ..." % (str(self), self.id))
		self.connect(self.info_server)	# Re connect the player.

#END
