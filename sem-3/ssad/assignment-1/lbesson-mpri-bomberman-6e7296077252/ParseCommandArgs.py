#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
A simple module to generated parsers for the command args of all others scripts.

Warning:
========
.. warning::
   This module use 'argparse', a new 2.7 module.
   That brokes the *retrocompatibility* with Python 2.6... Sorry !

More infos:
===========
 For more informations about argparse, go to `the 2.7.3 doc <http://docs.python.org/2.7/library/argparse.html>`_.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	#: Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.22'
__date__='ven. 15/02/2013 at 00h:12m:27s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
try:
	import os, sys, time
	__date__ = time.strftime("%a %d/%m/%Y at %Hh:%Mm:%Ss", time.localtime(os.lstat(sys.argv[0]).st_mtime))
	del os, sys, time
except:	pass

#1###############
# Usual Modules #
import argparse

########################################
#### Default values for new parsers ####

def default_epilog(version, date, author):
 """ This return the default epilog used to new parsers,
 which contains a copyright paragraph, determined by the three arguments version, date, author.
 """
 return """\n\

<yellow>Copyrigths:
===========<reset>
   Version %s, (c) 01-2013 (last modif: %s). Written in Python 2.7.3 (<u>http://www.python.org<U>).
    The parser of command line arguments is generated with argparse and ParseCommandArgs modules.
   By %s,
    ENS de Cachan (M1 Mathematics & M1 Computer Science MPRI).
    
   For Naereen Corp.,
    <u>mailto:naereen-corporation[AT]laposte.net<U>.
    <u>https:sites.google.com/site/naereencorp<U>.""" % (version, date, author)

#: The default description, used when generate a parser by parser_default function !
default_description = "WARNING: No description had been given to ParseCommandArgs.parser_default..."

def add_default_options(parser, version=__version__, date=__date__, author=__author__):
	""" parser_default(parser, version, date, author) -> argparse.ArgumentParser instance.
	
	Return the parser *parser*, modified by adding default options for the project,
	 which put the options : --version, --verbose, --noANSI and --noUTF
	 and others basic options."""
	parser.add_argument('-v', '--verbose', help="Used to increase verbosity (can be put more than once).", action='count')
	parser.add_argument('--version', action='version', version='%(prog)s '+version)
	#################################################
	#: Let those two lines, just to remember that others stuffs.
	parser.add_argument('--noANSI', help="If present, ANSI escape code from ANSIColors are *disable*.", action='store_true', default=False)
	parser.add_argument('--ANSI', help="If present, ANSI escape code from ANSIColors are *forced* to be printed (even if the output is detected to be a pipe).", action='store_true', default=False)
	parser.add_argument('--noUTF', help="If present, no UTF caracters will be used, and all will be ASCII. The default comportment is **TO USE** UTF8 caracters (mainly for box drawing) !", action='store_true', default=False)
	return parser

# To make a default parser.
def parser_default(description=default_description, \
	epilog="WARNING: No extra epilog had been given to ParseCommandArgs.parser_default...", \
	version=__version__, date=__date__, author=__author__, \
	preprocessor = str):
	""" parser_default(parser, version, date, author) -> argparse.ArgumentParser instance.
	
	Make a new *parser*, initialized by adding default options for the project (with add_default_options)
	 The default description is *default_description*,
	 The epilog will *epilog*, then default_epilog(version, date, author).
	
	preprocessor can be ANSIColors.sprint or __builtin__.str (default value)
	 (*i.e.* a string -> string function),
	 and it will be used as a **preprocessor** for *description* and *epilog* value.
	
	Example:
	 >>> parser = parser_default(description='<DELETE>A description.',\
		epilog='The description will no begin by the balise DELETE, thanks to sprint preprocessing.',\
 		preprocessor=lambda s: s.replace('<DELETE>', ''))
 	"""
#FIXME:
#######
# Passing RawDescriptionHelpFormatter as formatter_class= indicates that description and epilog are already correctly formatted and should not be line-wrapped:
# RawTextHelpFormatter maintains whitespace for all sorts of help text, including argument descriptions.
# The other formatter class available, ArgumentDefaultsHelpFormatter, will add information about the default value of each of the arguments:
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,\
		description=preprocessor(description), prefix_chars='-+',\
		epilog=preprocessor(epilog + default_epilog(version, date, author)))
	# change the function *add_default_options*, not this one.
	parser = add_default_options(parser, version, date, author)
	return parser

# DONE
