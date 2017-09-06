#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.4c'
__date__='ven. 15/02/2013 at 02h:03m:48s '	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

import os, sys, signal, readline, time

SLEEP_TIME = 0 #: put 0 to delete wait timer

# Paramaters load
def main(args):
	""" [OPTIONS] [command [args]]

Provides a very simple clone of GNU rlwrap program : 
 it launchs command, with args, 
 and with a support of readline facilities to write text :
  * history,
  * search in history,
  * completion based on history,
  * Nano like keybinding (Ctrl + a : beginning of a line, Ctrl + e : end of a line, etc).

Options:
========
 *	--debug_pyrlwrap		Show rlwrap traceback in case of an exception,
 *	--verbous_pyrlwrap		Show a message when launching command,
 *	--historyName_pyrlwrap=NAME
		Precise the name of the history file, the default value is .pyrlwrap.history, in the current folder,
 *	--no_history_pyrlwrap		Don't use history file save and read,
 *	--prompt_pyrlwrap=PS	
		Set the prompt used to PS, the default value is '>' precedded by the numero of the command,
 *	--Prompt_pyrlwrap		Force a prompt,
 *	--colorSupport_pyrlwrap		Force the prompt to be colored,
 *	--help_pyrlwrap			Show this help message.

Warning:
=========
 This program is under GPLv3 licence, and freely distributed by the Naereen Corp.
 In particular, it doesn't provide **any guaranty**.
	
 For example, synchronisation of prompt message, '> ' or the custom one, is not yet perfect. If it bother you, run with --noPrompt__pyrlwrap.
 To any bugs, suggestions, or questions, feel free to contact us : naereen-corporation[AT]laposte.net.

Copyrigths:
===========
 Naereen Corp.
  * mailto:naereen-corporation[AT]laposte.net
  * https:sites.google.com/site/naereencorp/liste-des-projets/pyrlwrap/
	"""
	used_options=0
	liste_options=['--verbous_pyrlwrap', '--no_history_pyrlwrap', '--colorSupport_pyrlwrap', '--noPrompt_pyrlwrap']
	liste_parameters=['--prompt_pyrlwrap=', '--historyName_pyrlwrap=']
	
	debug_pyrlwrap=('--debug_pyrlwrap' in args)
	verbous_pyrlwrap=('--verbous_pyrlwrap' in args)
	historyUse_pyrlwrap=not('--no_history_pyrlwrap' in args)
	historyName_pyrlwrap='.PyRlwrap.history'
	colorSupport_pyrlwrap=('--colorSupport_pyrlwrap' in args) or (os.getenv('TERM') in ['xterm', 'screen-bce'])
	usePrompt_pyrlwrap=('--Prompt_pyrlwrap' in args)
	
	PS1='> '
	
	for i in args:
		for j in liste_parameters:
			if i[:len(j)] == j:
				if j == '--prompt_pyrlwrap=':
					PS1=i[len(j):]
				if j == '--historyName_pyrlwrap=':
					historyName_pyrlwrap=i[len(j):]
				used_options = used_options + 1
		if i in liste_options:
			used_options = used_options + 1

	green=''
	red=''
	if colorSupport_pyrlwrap:
		green='\033[01;32m'
		red='\033[01;31m'
	white='\033[37m'
	
	if not os.path.isfile(historyName_pyrlwrap):
		if verbous_pyrlwrap:
			print "pyrlwrap: the file %s is absent, and is going to be created in the current directory..." % historyName_pyrlwrap
		file = open(historyName_pyrlwrap, 'w')
		if verbous_pyrlwrap:
			file.write('## Created by pyrlwrap ##\n')
		file.flush()
		file.close()
		readline.clear_history()

	if verbous_pyrlwrap:
		print "pyrlwrap: is going be used to wrap text edition for the following command, with %i options :" % used_options
		print args[1+used_options:]
		if historyUse_pyrlwrap:
			print "pyrlwrap: is going to use %s as an history file." % historyName_pyrlwrap

	if historyUse_pyrlwrap:
		readline.read_history_file(historyName_pyrlwrap)

	# Begin real stuff.
	#  Inspired from [http://maemo.gitorious.org/maemo-af/contextkit/blobs/a8f956de1a98f313b9f0da15e6075a36c67770b3/python/context-rlwrap]
	rfd, wfd = os.pipe()
	pid = os.fork()

	if pid == 0:
	 try:
	    os.close(wfd)
	    os.dup2(rfd, 0)
	    args.pop(used_options)
	    os.execvp(args[0], args)
	 except:
	    sys.exit("pyrlwrap: %s not found" % str(args))
	else:
	    def childied(n, f):
		p, ec = os.waitpid(pid, 0)
		sys.exit(ec)
	    signal.signal(signal.SIGCHLD, childied)
	    os.close(rfd)
	    time.sleep(SLEEP_TIME)
	    try:
	    	nbCommand=0
		while True:
		    if historyUse_pyrlwrap:
		    	readline.write_history_file(historyName_pyrlwrap)
		    ps1W=('%s%i%s%s%s' % (red, nbCommand, green, PS1, white))
		    if not(usePrompt_pyrlwrap):
		    	ps1W=''
		    sys.stdout.flush()
		    l = raw_input(ps1W)
		    sys.stdout.flush()
		    os.write(wfd, l + '\n')
		    sys.stdout.flush()
		    nbCommand = nbCommand + 1
	    	    time.sleep(0.3)
	    except (KeyboardInterrupt, SystemExit):
	    	if debug_pyrlwrap: raise
	    except: pass

# Redefine a __doc__ for the program / module.
__doc__="""PyRlwrap.py -- a simple readline wrapper

Usage: PyRlwrap.py %s

.. warning::
   This script works well, but it is not cleaned up, so reading the source is not nice.
""" % main.__doc__

if __name__ == '__main__':
	if len(sys.argv) < 2 or ('--help_pyrlwrap' in sys.argv):
	    sys.exit(__doc__)
	main(sys.argv)
