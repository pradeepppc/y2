#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This module implement a class (Board.Board) for Bomberman board, which is basically a **matrix** of states, represented with the class Board.State.

Specials states:
================
	* empty	-- an empty spot, with NOTHING on it.
	* dmur	-- a destructible wall, with JUST the wall on it.
	* umur	-- an undestructible wall, with JUST the wall on it.
	* expl	-- an empty spot, with JUST an explosion tag on it.

Warning:
========
   .. warning::
      **Use those constants state only with copy.copy(..).**
       **overwise it will work with references over those constants.**

Example :
=========
	>>> for i, j, spot in board:
	>>>  spot=Board.empty

	All spots of [board] are now the same, so all modification like

	>>> board[i,j].explosion=True

	will be done on *ALL spot of [board]*.
	 **And that's not what we want to**.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='1.1a'
__date__='jeu. 14/02/2013 at 02h:59m:40s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules #
import sys, copy

#2#################
# Project Modules #
import Bonus	# Bonus.py : implement the simple bonus system. (actions, representation etc)
import Bomb	# Bomb.py : implement the simple bomb system. (actions, representation etc)
import ANSIColors	# ANSIColors.py : just some colors definition.
import Matrix	# Matrix.py : simple module to manipulate matrix, for the board.

##############################################################################
from Constants import *
import ParseMessageOut

####################################################
#: Try to know if the encoding is UTF-8 supported.
UTFSupported = False
try:
 UTFSupported=('UTF-8' == sys.stdout.encoding) or ('UTF-8' == sys.stdin.encoding)
except Exception as e:
	try:
		if sys.stdout.isatty():
			ANSIColors.writec("\t<WARNING> /UTF-8/ seems to <red>not be supported<white> (and the detection ends <u><red>badly<U> : %s<white> !).\n" % str(e), file=sys.stderr)
	except:
		sys.stderr.write("\t<WARNING> /UTF-8/ seems to <red>not be supported<white> (and the detection ends <u><red>badly<U><white> !).\n")
if not UTFSupported:
	try:
		if sys.stdout.isatty():
			ANSIColors.writec("\t<INFO> /UTF-8/ seems to <red>not be supported<white> (but the detection ends <u><green>nicely<U><white> !).\n", file=sys.stderr)
	except:	pass
####################################################

# Defines the state of one spot on the board
class State:
	""" A Class for the element of the board.

	Attributes:
	 * wall	-- True if the case is a wall, false if it is empty (ie : can be occupyed by a player, or/and a bomb, or/and a bonus).
	 * destr	-- True or False, if the case can be destroy (CONVENTION: a piece of wall is destroid in one explosion).
	 * bomb	-- A Bomb.Bomb instance (no need for more than 1).
	 * players	-- List of Player.noPlayer if there is a player, a Player.Player instance if there is one.
	 * explosion	-- A boolean for a visual effect of an explosion !
	 * bonus	-- None if there is no bonus, or a Bonus.Bonus instance if there is one (only one bonus in a state).

	This class can be used both by the client and the server.
	But, for the server each players in the attribute players are instances of Player.PlayerServer; and for the client, the client's player is a Player.Player instance, and all other players are Player.Player.
	"""

	def __init__(self, wall=True, destr=False, bomb=None, players=copy.copy([]), explosion=False, bonus=None): ##, offsets=copy.copy([])):
	 """ Simple constructor of state, assigned with default value (an undestructible piece of wall).
	 Each parameters can be directly assigned.

	 For example, myState=State(wall=False, players=[myself]) return a State initializing as containing the player [myself]."""
	 self.wall = wall	#: True if the case is a wall, false if it is empty (ie : can be occupyed by a player, or/and a bomb, or/and a bonus).
	 self.destr = destr	#: True or False, if the case can be destroy (CONVENTION: a piece of wall is destroid in one explosion).
	 self.bomb = bomb	#: A Bomb.Bomb instance (no need for more than 1).
	 self.players = players	#: List of Player.noPlayer if there is a player, a Player.Player instance if there is one.
	 self.explosion = explosion	#: A boolean for a visual effect of an explosion !
	 self.bonus = copy.copy(bonus)	#: None if there is no bonus, or a Bonus.Bonus instance if there is one (only one bonus in a state).

	def to_send(self):
	 """ This method is imported from ParseMessageOut."""
	 return ParseMessageOut.str_of_state(self)

	def is_free(self):
		""" self.is_free() -> True|False
		 Determine if a player can be placed in the spot *self*. """
		return not(self.wall or self.bomb)

	def strNoUtf(self):
	 """ Simple transformation of a state to a universal (no UTF, only ASCII) string of 3 caraters."""
	 if self.wall:
	 	if self.destr: return '[D]'
	 	return '[U]'
	 s1, s2, s3=" ", " ", " "
	 if self.bonus: s1=self.bonus.strNoUtf()[0]
	 if self.players:
	 	s2=str(self.players[0].pseudo[0])
	 	try:
	 		s2.decode('ascii')
	 	except:
	 		s2 = str( self.players[0].id )
	 # BUG: if pseudo contains UTF caracters, there is a problem.
	 # FIXED
	 if self.bomb: s3=str(max(0, self.bomb.timer))[0]
	 if s3==" " and self.explosion:	s3="*"
	 if s1==" " and self.explosion:	s1="*"
	 return s1 + s2 + s3

	def strUtf(self):
	 u""" Simple transformation of a state to a non ASCII (*i.e.* with UTF caracters) **string of 3 caraters**.
	 For a wall, 3 grey blocks if it can be brocken, or 3 black blocks.
	 For an explosion, a *little sun* is used.

	 If those caracters do not seems pretty, try to change the encoding *used* **here** to **UTF-8**.

	 **Sorry, I didn't succeed in putting those caracters here** in this docstring, because pyDoc doesn't have compatibility with UTF8.
	  And I like pyDoc.
	  I really do :)
	  By the way, I wrote the script **makePydoc.sh**.
	  Take a look !
	 """
	 if self.wall:
	 	if self.destr: return '░░░'
	 	return '▓▓▓'
	 s1, s2, s3=" ", " ", " "
	 if self.bonus:
	  s1=self.bonus.strNoUtf()[0]
#:	  s1 = repr( self.bonus )[0]
#:	  print "Bonus: "+s1, s1, str(s1)
	 if self.players: s2="%s%s%s" % (ANSIColors.tocolor(self.players[0].color), self.players[0].pseudo[0], ANSIColors.white)
	 if self.bomb: s3=str(max(0, self.bomb.timer))[0]
	 if s3==" " and self.explosion:	s3="☼"
	 if s1==" " and self.explosion:	s1="☼"
	 return s1 + s2 + s3	# FIXME: s2.encode('utf-8') ?

	def __str__(self):
	 """ __str__(self) <=> str(self) -> 'str'
	  Generic conversion to a string, choose an UTF8 representation if it is **available**."""
	 if UTFSupported:
	 	return self.strUtf()
	 else:
	 	return self.strNoUtf()

	def __repr__(self):
	 """Toplevel representation of [self], is str(self)."""
	 return ("wall=%s; destr=%s; bomb=%s; players=%s; bonus=%s; explosion=%s" % (self.wall, self.destr, self.bomb, self.players, self.bonus, self.explosion) )

	def __eq__(self, s):
	 """ self.__eq__(s) <==> s == self"""
	 return s.__dict__ == self.__dict__

	def hit(self, ingury=1):
	 """ Destroy the element in case [self] with [ingury] damages.

	 Cases:
	  * If it's a destructible wall, break it, return SIGNAL_WALL_BREAKE=2.
	  * If it's a undestructible wall, break it, return SIGNAL_WALL_NOT_BREAKE=4.
	  * If it's a bomb, destroy it, return SIGNAL_BOMB_HURT.
	  * If it's a player, hurt it with [ingury] ingury(ies), return SIGNAL_PLAYER_HURT=3.
	     The player in this case can die, raising Player.PlayerDeath.
	 """
	 if self.destr:	# Become empty if it's a destructible wall.
	  if self.wall: ANSIColors.printc("\t/D/ <red> A destructible wall have been founded. Now the spot is empty !<white>")
	  self.wall = False
	  self.destr = False
	  return SIGNAL_WALL_BREAKE
	 for p in self.players:
	  p.hurt(ingury)	# Eventually, player die.
	 if self.bomb:
	  self.bomb.timer=0
	  ANSIColors.printc("\t/b/ <red> A bomb have been founded, his timer is getting <u>reduce to 0<U> immediatly !<white>")
	  return SIGNAL_BOMB_HURT
	 if self.players:	# if one players was hurted
	  return SIGNAL_PLAYER_HURT
	 if self.wall:	# if the wall is undestructible
	  return SIGNAL_WALL_NOT_BREAKE
	 return 0 #: Nothing special happened.

#: Special States:

empty	= State(wall=False)	#: An *empty spot*, with NOTHING on it.
dmur	= State(wall=True, destr=True)	#: A *destructible wall*, with JUST the wall on it.
umur	= State(wall=True, destr=False)	#: An *undestructible wall*, with JUST the wall on it.
expl	= State(wall=False, destr=False, explosion=True)	#: An empty spot, with JUST an **explosion tag** on it.

class Board:
	""" A Class to define a Bomberman board.

	Attributes:
	 * lx	-- his dimension over horizontal axe x.
	 * ly	-- his dimension over vertical axe y.
	 * nb	-- max number of player, (for usual boards, it's 4).
	 * mat	-- the map of State instances, coded as a matrix.
 	  For call convention, take a look at [Matrix] module.
 	  [mat.box] will be used for printing, so it can be
	  modified by other stuff.

	This class can be used both by the client and the server.
	"""

	def __init__(self, state=copy.copy(State()), lx=lx_Max, ly=ly_Max, nb=nbmax_Max, maxStr=3, utf=UTFSupported):
	 """ Simple constructor of an empty board.
	 Contains a [map] attribute initialized with all elements equal to a copy of [state].
	 The board is a rectangle, of length [lx] over [ly].
	 [maxStr] is passed throw the underlying matrix, and will be used for printing (see Matrix.tostr).
	 [utf] is true to use non ASCII caracters for printing the matrix, false otherwise."""
	 self.lx = lx	#: his dimension over horizontal axe x.
	 self.ly = ly	#: his dimension over vertical axe y.
	 self.nb = nb	#: max number of player, (for usual boards, it's 4).
	 self.mat = Matrix.Matrix(state, lx, ly, maxStr = maxStr)	#: the map of State instances, coding as a matrix (ie. Matrix.Matrix instance).
	 if utf:
	  self.mat.box = Matrix.boxnoASCII
	 else:
	  self.mat.box = Matrix.boxASCII

	def bombs(self):
	 """ Simply return a list of Bomb.Bomb associated with their position.
	 Example : [(0,1,<bomb>), (1,3,<bomb>)]

	 FIXME: it shall be useless now.
	 """
	 bombs=[]
	 for i in range(self.lx):
	  for j in range(self.ly):
	   if self.mat[i,j].bomb:
	    bombs.append((i,j, self.mat[i,j].bomb))
	 return bombs

	def players(self):
	 """ Simply return a list of Player.Player associated with their position."""
	 res=[]
	 for i in range(self.lx):
	  for j in range(self.ly):
	   if self.mat[i,j].players:
	    for p in self.mat[i,j].players:
	     res.append(p)
	 return res

	def str_of_players(self, pl):
	 """ This method is imported from ParseMessageOut."""
	 return ParseMessageOut.str_of_players(self, pl)

	def __str__(self):
	 """ Transformation to a string, using Matrix.Matrix.__str__ method."""
	 return str(self.mat)

	def __repr__(self):
	 """ Toplevel representation of a Board, to a string."""
	 return ("lx=%i; ly=%i; nb=%i; %s" % (self.lx, self.ly, self.nb, repr(self.mat)))

	def __getitem__(self, (i,j)):
	 """ A shortcut to self.mat[i,j].
	 Allow self[i,j]."""
	 return self.mat[i,j]

	def __setitem__(self, (i,j), val):
	 """ A shortcut to self.mat[i,j]=val
	 Allow self[i,j] = v."""
	 self.mat[i,j]=val

	def __contains__(self, u):
	 """ self.__contains__(u) <==> u in self"""
	 return u in self.mat

	def __eq__(self, b):
	 """ self.__eq__(b) <==> b == self"""
	 return b.mat == self.mat

	def fill(self, val):
	 """ Set all state of the board to [val]."""
	 for i in range(self.lx):
	  for j in range(self.ly):
	   self.mat[i,j] = copy.copy(val)

###############################################################################

	def destroy_bomb(self, i, j, toc = toc_default, radius = force_default,\
		print_on_all=None, str_of_blowbomb=None, list_clients=None, origin=None,\
		FORCE = False, verb = False):
	 """ Just decrease the timer of the bomb in the board[i,j], [toc] is the time spent during ticking.

 FIXME: make sure it spreads from the spot, in the right direction. Seems ok.

 FORCE is here to allow the destruction of a bomb even if its timer is not ok...

.. warning::
   This function is quite **long**, make sure it works correctly !
	 """
	 if (self.mat[i,j].bomb) or FORCE:
	    if (self.mat[i,j].bomb.timer > 0) and not(FORCE):
	     if verb:	ANSIColors.printc("\t/b/ One bomb \t[%s] found in <black>(%i, %i)<white> : it's <u>not<U> explosing..." % (self.mat[i,j].bomb, i,j))
	    else:
	     ANSIColors.printc("\t/B/ One bomb [%s] found in <red>(%i, %i)<white> : it's explosing..." % (self.mat[i,j].bomb, i,j))
	     try:
	      self.mat[i,j].bomb.owner.nb_bomb -= 1
	      ANSIColors.printc("\t/B/  <green>Hehehe : this bomb have an <u>owner<U> (<neg>%s<Neg>) !<white>. He now possess %i bomb(s) in the board !" % (str(self.mat[i,j].bomb.owner), self.mat[i,j].bomb.owner.nb_bomb))
	     except Exception as e:
	      ANSIColors.printc("\t/B/  <red>Ohohoh : this bomb doesn't have an <u>owner<U> attribute !<white>. Cause : %s." % str(e))
	     # the owner of the bomb lost one of his bomb(s).
	     localbomb=self.mat[i,j].bomb
	     if radius > 0:
	     	localbomb.force = radius
	     	ANSIColors.printc("\t/B/ Overpassing this bomb's force with the function argument <neg>%i<Neg> !" % radius)
	     else:
	     	radius = max(min(localbomb.force, 10), 1)
	     	ANSIColors.printc("\t/B/ Using a new bomb's force : <neg>%i<Neg> !" % radius)
############################ For BombermanServer
	     if list_clients:
	      try:
	       tmp = ""
	       for s in list_clients:	tmp += "[%s:%i], " % s.getsockname()
	       ANSIColors.printc("""
/destroy_bomb/ I'm trying to informs the clients in <neg>%s<Neg> that I found an exploding bomb in (%i,%i).
""" % ( tmp, i, j ))
	       print_on_all( str_of_blowbomb(i,j,radius) , list_clients, origin)	# FIXED ?
	      except:
	       ANSIColors.printc("/destroy_bomb/ <red> Fails <white> when I tried to inform my clients.")
############################ For BombermanServer
	     self.mat[i,j].bomb = copy.copy(None) # the bomb is deleted after inguried all spots.
	     ii=i
# Top
	     for jj in range(j, min(self.ly, j+1+localbomb.force)):
	       return_signal = self.mat[ii, jj].hit(localbomb.power)
	       self.mat[ii, jj].explosion=True
	       if SIGNAL_BOMB_HURT == return_signal:
	        # there is a bomb in (ii, jj), with timer = 0 now
	        ANSIColors.printc("\t/!/ The explosion <red>touched an other bomb<white> : it's gonna to explode to !<white>")
	        if jj!=j or ii!=i: self.destroy_bomb(ii, jj, toc=toc, verb=verb, radius=radius,\
			print_on_all=print_on_all, str_of_blowbomb=str_of_blowbomb,\
			list_clients=list_clients, origin=origin, FORCE=FORCE)
	        # make the bomb in (ii, jj) explode
	       if SIGNAL_WALL_BREAKE == return_signal:
	        ANSIColors.printc("\t/D/ The explosion have been stoped by a destructible wall in (%i,%i) !<white>" % (ii, jj))
#:	        if BREAK_ON_WALL: break
	       if SIGNAL_WALL_NOT_BREAKE == return_signal:
	        ANSIColors.printc("\t/U/ The explosion have been stoped by a undestructible wall in (%i,%i) !<white>" % (ii, jj))
	        if BREAK_ON_WALL: break
	       if verb:	ANSIColors.printc("\t/h/ The bomb found in <green>(%i, %i)<white> hurts the case <red>(%i, %i)<white> with power %i because this spot is clos enough (force=%i)." % (i, j, ii, jj, localbomb.power, localbomb.force))
# Bottom
	     for jj in range(j-1, -1+max(0, j-1-localbomb.force), -1):
	       if j>1 and jj==j-1-localbomb.force: continue
	       return_signal = self.mat[ii, jj].hit(localbomb.power)
	       if verb:	ANSIColors.printc("\t/h/ The bomb found in <green>(%i, %i)<white> hurts the case <red>(%i, %i)<white> with power %i because this spot is clos enough (force=%i)." % (i, j, ii, jj, localbomb.power, localbomb.force))
	       self.mat[ii, jj].explosion=True
	       if SIGNAL_BOMB_HURT == return_signal:
	        # there is a bomb in (ii, jj), with timer = 0 now
	        ANSIColors.printc("\t/!/ The explosion <red>touched an other bomb<white> : it's gonna to explode to !<white>")
	        if jj!=j or ii!=i: self.destroy_bomb(ii, jj, toc=toc, verb=verb, radius=radius,\
			print_on_all=print_on_all, str_of_blowbomb=str_of_blowbomb,\
			list_clients=list_clients, origin=origin, FORCE=FORCE)
	        # make the bomb in (ii, jj) explode
	       if SIGNAL_WALL_BREAKE == return_signal:
	        ANSIColors.printc("\t/D/ The explosion have been stoped by a destructible wall in (%i,%i) !<white>" % (ii, jj))
#:	        if BREAK_ON_WALL: break
	       if SIGNAL_WALL_NOT_BREAKE == return_signal:
	        ANSIColors.printc("\t/U/ The explosion have been stoped by a undestructible wall in (%i,%i) !<white>" % (ii, jj))
	        if BREAK_ON_WALL: break
	     jj=j
# Right
	     for ii in range(i+1, min(self.lx, i+1+localbomb.force)):
	       return_signal = self.mat[ii, jj].hit(localbomb.power)
	       if verb:	ANSIColors.printc("\t/h/ The bomb found in <green>(%i, %i)<white> hurts the case <red>(%i, %i)<white> with power %i because this spot is clos enough (force=%i)." % (i, j, ii, jj, localbomb.power, localbomb.force))
	       self.mat[ii, jj].explosion=True
	       if SIGNAL_BOMB_HURT == return_signal:
	        # there is a bomb in (ii, jj), with timer = 0 now
	        ANSIColors.printc("\t/!/ The explosion <red>touched an other bomb<white> : it's gonna to explode to !<white>")
	        if jj!=j or ii!=i: self.destroy_bomb(ii, jj, toc=toc, verb=verb, radius=radius,\
			print_on_all=print_on_all, str_of_blowbomb=str_of_blowbomb,\
			list_clients=list_clients, origin=origin, FORCE=FORCE)
	        # make the bomb in (ii, jj) explode
	       if SIGNAL_WALL_BREAKE == return_signal:
	        ANSIColors.printc("\t/D/ The explosion have been stoped by a destructible wall in (%i,%i) !<white>" % (ii, jj))
#:	        if BREAK_ON_WALL: break
	       if SIGNAL_WALL_NOT_BREAKE == return_signal:
	        ANSIColors.printc("\t/U/ The explosion have been stoped by a undestructible wall in (%i,%i) !<white>" % (ii, jj))
	        if BREAK_ON_WALL: break
# Left
	     for ii in range(i-1, -1+max(0, i-1-localbomb.force), -1):
	       if i>1 and ii==i-1-localbomb.force: continue
	       return_signal = self.mat[ii, jj].hit(localbomb.power)
	       if verb:	ANSIColors.printc("\t/h/ The bomb found in <green>(%i, %i)<white> hurts the case <red>(%i, %i)<white> with power %i because this spot is clos enough (force=%i)." % (i, j, ii, jj, localbomb.power, localbomb.force))
	       self.mat[ii, jj].explosion=True
	       if SIGNAL_BOMB_HURT == return_signal:
	        # there is a bomb in (ii, jj), with timer = 0 now
	        ANSIColors.printc("\t/!/ The explosion <red>touched an other bomb<white> : it's gonna to explode to !<white>")
	        if jj!=j or ii!=i: self.destroy_bomb(ii, jj, toc=toc, verb=verb, radius=radius,\
			print_on_all=print_on_all, str_of_blowbomb=str_of_blowbomb,\
			list_clients=list_clients, origin=origin, FORCE=FORCE)
	        # make the bomb in (ii, jj) explode
	       if SIGNAL_WALL_BREAKE == return_signal:
	        ANSIColors.printc("\t/D/ The explosion have been stoped by a destructible wall in (%i,%i) !<white>" % (ii, jj))
#:	        if BREAK_ON_WALL: break
	       if SIGNAL_WALL_NOT_BREAKE == return_signal:
	        ANSIColors.printc("\t/U/ The explosion have been stoped by a undestructible wall in (%i,%i) !<white>" % (ii, jj))
	        if BREAK_ON_WALL: break
# ok now the end
	     ANSIColors.printc("\t/B/ The old bomb found in <green>(%i, %i)<white> : it has just exploded, so it has been deleted." % (i,j))
	     return 0

	def tic(self, toc=toc_default, MAKE_DESTROY=True, verb=False, FORCE=False,\
		print_on_all=None, str_of_blowbomb=None, list_clients=None, origin=None):
	 """ Just decrease the timer of all bombs in the board, [toc] is the time spent during ticking.
	 MAKE_DESTROY is here to allow ticking the board without triggering any explosion.
	  Because for the client, timers are just for priting.

	 Call *destroy_bomb* whenever it is needed (*i.e.* when a timer is going non positive (<= 0).)"""
	 nb_bomb=0
	 # for all spot
	 for i in range(self.lx):
	  for j in range(self.ly):
	   # tic the bomb
	   if self.mat[i,j].bomb:
	     nb_bomb+=1	# a new bomb !
	     if self.mat[i,j].bomb.tic(toc) and MAKE_DESTROY:
		     self.destroy_bomb(i,j, toc=toc, verb=verb, FORCE=FORCE, \
			print_on_all=print_on_all, str_of_blowbomb=str_of_blowbomb, \
			list_clients=list_clients, origin=origin)
	 ANSIColors.printc("\t/t/ The board have been ticked, %i bomb(s) founded !<white>" % nb_bomb)

	def __iter__(self):
	 """ Special method to allow an iteration with a board.

.. warning::
   This seems to be wrong, use *board[i,j]* and not *spot*,
   **if you want to modify board[i,j]**.

 Example:
  >>> for i,j,spot in board:
  >>>  spot.destr=False; spot.wall=False; spot.explosion=True
  >>>  print "Spot at place (%i, %i)" % (i,j)

 The map is explored from (0,0) to (self.lx - 1, self.ly - 1),
  LINE by LINE (x loop first) then COLUMN by COLUMN (then y loop)."""
	 return IterBoard(self)

###############################################################################
class IterBoard:
	""" A class for build **an iterator for Board**.

	It's mainly done here to *learn* about iterator.
	This *workaround* allow the following shortcut :

	Example:
	 >>> for i,j,spot in board:
	 >>>  spot.destr=False; spot.wall=False; spot.explosion=True
	 >>>  print "Spot at place (%i, %i)" % (i,j)

	This is useful, to avoid double loop with i, j.
	 And moreover, this is interesting from the user : write 'for spot in board' is intuitive."""

	def __init__(self, board):
	 """ A wrapper around Board.Board class to build an iteratoir for a map."""
	 self.board=board	#: the board used for iteration
	 self.i = 0	#: current value of i (over axis x)
	 self.j = -1	#: current value of j (over axis y)

	def next(self):
	 """ Iterator for Board.Board !"""
	 if self.j < self.board.ly - 1:
	  self.j += 1
	 else:
	  self.j = 0
	  self.i += 1
	 if (self.i >= self.board.lx) or (self.j == self.board.ly):
          raise StopIteration
	 return self.i, self.j, self.board[self.i, self.j]

#END
