#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" A simple functionnal module to manipulate matrices,
and a simple class for matrices.

Efficiency:
===========
.. warning::
  This module *is not designed* to be used for mathematics purpose.
  And the list of list structure is **not good** for efficiency of maths calculus.
	
  The Matrix.Matrix class is designed to be used as a data type, 
  and **pretty printing is the main goal**.

Example:
========
>>> m=Matrix.Matrix(0,2,3) # Creating a matrix. 2 lines, 3 colums.
>>> print repr(m) # Representation of m.mat is done with usual representation of a list.
maxStr=3;mat=[[0, 0, 0], [0, 0, 0]]
>>> print m # beautiful !
┌─┬─┬─┐
│0│0│0│
├─┼─┼─┤
│0│0│0│
└─┴─┴─┘
>>> m.box=Matrix.boxASCII
>>> print m # less pretty... but more universal (only ASCII symbols)
/-+-+-\\
|0|0|0|
+-+-+-+
|0|0|0|
\\-+-+-/
>>> m[1,2]='ok' # Support different data type for one matrix.
>>> m.box=Matrix.boxnoASCII
>>> print m
┌──┬──┬──┐
│0 │0 │0 │
├──┼──┼──┤
│0 │0 │ok│
└──┴──┴──┘
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.4b'
__date__='jeu. 14/02/2013 at 03h:00m:35s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

#1###############
# Usual Modules #
import copy

def matrix_init(value, lx = 1, ly = 1):
	""" A shortcut to create a matrix [lx] * [ly], initialized with value [value].
	Element in (i,j), i for x, j for y, is given by <matrix>[i][j].
	 x, i, lx are for columns.
	 y, j, ly are for lines.
	
	The returned value IS NOT a instance of Matrix.Matrix class !"""
	res = list()
	for i in range(lx):
	 res.append(list())
	 for j in range(ly):
	  res[i].append(copy.copy(value))
	return res

#: UTF8 (noASCII) box caracters to print boxes.
boxnoASCII={
	'e':' ',	#: Empty
	'h':'─',	#: Horizontal
	'v':'│',	#: Vertical
	'tr':'┐',	#: Top Right corner
	'tl':'┌',	#: Top Left corner
	'bl':'└',	#: Bottom Left corner
	'br':'┘',	#: Bottom Right corner
	'c':'┼',	#: Cross
	'cr':'├',	#: Cross right
	'cl':'┤',	#: Cross left
	'ct':'┴',	#: Cross top
	'cb':'┬'	# Cross bottom
}

#: ASCII caracters to print boxes
boxASCII={
	'e':' ',	#: Empty
	'h':'-',	#: Horizontal
	'v':'|',	#: Vertical
	'tr':'\\',	#: Top Right corner
	'tl':'/',	#: Top Left corner
	'bl':'\\',	#: Bottom Left corner
	'br':'/',	#: Bottom Right corner
	'c':'+',	#: Cross
	'cr':'+',	#: Cross right
	'cl':'+',	#: Cross left
	'ct':'+',	#: Cross top
	'cb':'+'	# Cross bottom
}

def tostr(mat, lgmax=3, lgmaxANSI=36, box=boxnoASCII):
	""" Uses ANSI box symbol to print the matrix [mat], understandood as a list of list of element.
	[mat] have to be a matrix of printable element, with str(element),
	 (ie, instances of a class providing __str__ method).
	
.. warning::

   str(element) have to return a string OVER ONE UNIQUE LINE.
   Example: str(element) = "D", "P", "C", "F", "R", "T" for a chess game.
   But you can use ANSIColors escaped string to augment possibilities.

About:
 * [lgmax] will be the max number of caracters seen in the screen in one part of the box.
 * [lgmaxANSI] will be the max number of caracters really printed for each box.
	WARNING: might be different than [lgmax] because ANSIColors escaped codes are longer.

Box:
 Uses the box, a dictionnary containing c, cr, cl, ct, cb, br, bl, tl, tr, h, v, e.
 Two boxes are preset : boxANSI and boxNoANSI.
 The first one is the default value, and uses ANSI specials caracters, not supported for all encoding (try UTF8).
 The second one is less pretty (see examples), but more universal because \\ / + - | are supported for all encoding.
"""
	lx=len(mat)
	ly=len(mat[0])
	# Determine hline and longr
	longr=1
	for i in range(lx):
	 for j in range(ly):
	  longr=max(longr,len(str(mat[i][j])))
	  longr=min(longr, lgmax)
	hline=""
	hline+=box['h']*longr
	# Begin
	res=box['tl']+hline
	for i in range(lx):
	 for j in range(ly):
	  if i==0:
	   if j>0: res+=box['cb']+hline
	   if j==ly-1: res+=box['tr']+"\n"
	  else:
	   if j==0: res+=box['cr']+hline
	   else: res+=box['c']+hline
	 if i > 0: res+=box['cl']+"\n"
	 for j in range(ly):
	  mas=str(mat[i][j])[:lgmaxANSI]
	  while len(mas)<longr:
	   mas+=box['e']
	  res+=box['v'] + mas
	 res+=box['v']+"\n"
	for j in range(ly):
	 if j==0: res+=box['bl']
	 else: res+=box['ct']
	 res+=hline
	res+=box['br']
	return res

#: Now, the Matrix.Matrix class
class Matrix():
	""" A class to represent matrices.
	
Attributes:
 * mat	-- list of list of values,
 * box	-- a box dictionnary for printing lines
 * maxStr	-- max length of printed element of [mat]."""
	
	def __init__(self, value=None, lx=1, ly=1, box=boxnoASCII, maxStr=3, new=True):
	 """ Create a matrix filled of values = [value], dimensionized at [lx]*[ly].
	 If [new], all values in the new matrix are fresh copies of [value].
	 If almost all situations, it's better to have [new]=True (otherwise you work with references, without saying it)."""
	 self.maxStr=maxStr	#: max length of printed element of [mat].
	 self.box=box	#: a box dictionnary for printing lines
	 self.mat = list()	#: list of list of values,
	 for i in range(lx):
	  self.mat.append(list())
	  for j in range(ly):
	   if new: self.mat[i].append(copy.copy(value))
	   else: self.mat[i].append(value)

	def lx(self):
	 """ lx(self) -> integer
	  Number of laws."""
	 return len(self.mat)

	def ly(self):
	 """ ly(self) -> integer
	  Number of rows."""
	 return len(self.mat[0])
	
	def __eq__(self, m):
	 """ self.__eq__(m) <==> m == self"""
	 return m.mat == self.mat
	
	def __contains__(self, u):
	 """ self.__contains__(y) <==> y in self"""
	 res = False
	 for i in range(self.lx()):
	  for j in range(self.ly()):
	   res = res or (u == self[i,j])
	 return res
	
	def __len__(self):
	 """ Dimension of a matrix."""
	 return (self.lx() * self.ly())

	def __str__(self):
	 """ Transformation to a string.
	 Warning : here it's different to __repr__."""
	 return tostr(self.mat, box=self.box, lgmax=self.maxStr)

	def __getitem__(self, (i,j)):
	 """ A shortcut to self.mat[i][j].
	 Allow self[i,j]"""
	 return self.mat[i][j]

	def __setitem__(self, (i,j), val):
	 """ A shortcut to self.mat[i][j]=val
 Allow self[i,j] = v.
 
 Warning:
 	Use copy.copy to be sure of producing a fresh copy of [val]."""
	 self.mat[i][j]=copy.copy(val)

	def __repr__(self):
	 """ Toplevel representation of a Board, to a string."""
	 return "mat=%s" % repr(self.mat)

#END
