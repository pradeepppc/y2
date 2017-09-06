#!/usr/bin/python
# -*- encoding: utf-8 -*-

""" A simple IRC client.
 From TP1 of MPRI Courses "Net Project".
 Ex1 (QU1) (QU2)

.. warning::
   This script is **deprecated**, don't use it.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.93'
__date__='jeudi 07 02 2013, at 23h:17m:30s'	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

import socket, sys, thread, os

# Non usual module ! FIXME : explain how to install it
import ToolReadline	# ToolReadline.py : uses readline to allow beautiful text inputs.
import ANSIColors	# ANSIColors.py : just some colors definition.
from Constants import SERVEUR_INIT, PORT_INIT	# Constants.py : default constants.

def ColorOff(verb=False):
	""" Turn off the support of ANSI Colors.
	Can be used other somewhere else, or on other modules, AFTER importing ANSIColors module !"""
	for n in ANSIColors.colorList:
	 exec('ANSIColors.%s=\"\"' % n)
	 if verb: print "\t/-/ ANSIColors.%s deleted." % n
	print "\t/-/ ANSIColors disabling..."

def ColorOn(verb=False):
	""" Turn on the support of ANSI Colors.
	Can be used other somewhere else, or on other modules, AFTER importing ANSIColors module !"""
	for n in ANSIColors.colorList:
	 exec('ANSIColors.%s=ANSIColors._%s' % (n, n))
	 if verb: print "\t/+/ ANSIColors.%s recreated." % n
	ANSIColors.printc("\t/+/ ANSIColors <green>enabling...<white>")

try:
	import PyZenity
	AsZenity=False
except:
	print "\t/!/ Zenity not found : read arguments from command line."
#: Args for all Zenity call
kwargs={'title':'IRC server', 'window-icon':'server'}

def exit_with_Zenity(msg_erreur):
	""" A remplacement for sys.exit : print an error message with Zenity before executing sys.exit.
	"""
	if AsZenity:
		PyZenity.ErrorMessage(msg_erreur)
	sys.exit(msg_erreur)

HOST, PORT=SERVEUR_INIT, PORT_INIT	#: Default values, from Constants.py
PRINT_ALL_MESSAGE=1		#: 1 to print messages
WRAPPER_PRINTED=0		#: 1 to print >> and << in output and input.

def create_socket_client(server = (HOST, PORT)):
	""" Create a socket designed to be a client, and connect it to @server.
	Return a socket."""
	msocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	msocket.connect(server)
	return(msocket)

# Pieces of text to be printed before each input, and each output.
WRAPPER_IN=''	#: Piece of text to be printed before each input
WRAPPER_OUT='<< '	#: Piece of text to be printed before each output.

##########################
##### User interface #####

#: The help message, which can be printed to the user when invoking *'\\?'*
help_User="""
Welcome in IRC client v%s.
	Wrote by %s, last version dated of %s.

Your are connected to a local IRC server using UDP sockets.
All messages enter from here will be broadcasted to all other connected clients, and here are broadcasted all messages from other clients.

The following commands are enabled :
	\\h, \\help, \\? : print this help,
	\\out : logout violently (not like Ctrl+D or Ctrl+C).
""" % (__version__, __author__, __date__)

def action_on_readstr(readstr):
	""" Reaction to special message readed from the keyboard !"""
	if readstr in ['\\h\n', '\\help\n', '\\?\n']:
		ANSIColors.printc('\t/?/ <blue>Help : \\h or \\help or \\?<white>:')
		print help_User
		return True
	if readstr in ['\\out\n']:
		ANSIColors.printc('\t/!/ <red>Client closed<white>, because <green>client wants to, by sending an EOF signal with \\out command !<white> (this is dirty, don\'t used it !)')
		os._exit(0)
	return False

def run_client(msocket, server, PRINT_ALL_MESSAGE=PRINT_ALL_MESSAGE, WRAPPER_PRINTED=WRAPPER_PRINTED):
	""" An infinite loop over the @msocket, which have to be a client socket assumed te be connected with @server (just used to print some usefull informations).
	Concurrently, read from stdin on client and write on stdout on server, and read on stdin on server and write on stdout on client. Use thread.

	DEBUG, PRINT_ALL_MESSAGE, WRAPPER_PRINTED: are options for parametrize behaviour of client."""
	msocket_name=("%s:%i" % msocket.getsockname())
	server_name=("%s:%i" % server)
	mfile=msocket.makefile()
	# Definition of the function we want to parallelize
	def read_write_inverse(sin, sout, server_to_client, nsin = "sin", nsout = "sout"):
	 """ Read input message from @sin and print them to @sout.
	@nsin and @nsout are string descriptors to print usefull informations about exchange messages.
	The Boolean @server_to_client is used to print >> in the beginning of client input lines, and << in output.
	 """
	 try:
	   while 1:
		 readstr=sin.readline()
		 if action_on_readstr(readstr):
		  continue
	# except:
		 # readstr=''
		 # Handle if server or client is closing
		 if len(readstr)==0:
		 	msocket.shutdown(socket.SHUT_RDWR)
		 	msocket.close()
		 if WRAPPER_PRINTED: # Not working yet for wrapper_in ! FIXME
		  sys.stdout.write(WRAPPER_IN)
		  sout.write(WRAPPER_IN)
		  sys.stdout.flush()
		  sout.flush()
		 if PRINT_ALL_MESSAGE:
		  ANSIColors.printc('\t/2/ Message [<yellow>%s<white>] readed from <blue>%s<white>,' % ((readstr[:(len(readstr) - 1)] ), nsin))
		  # We remove the last caracter to avoir printing the last \n
		  sys.stdout.flush()
		 if WRAPPER_PRINTED:
		  sout.write(WRAPPER_OUT+readstr+WRAPPER_IN) # This works but USELESS now
		 else:
		  sout.write(readstr)
		  sout.flush()
	 except:
	 	 #print server_to_client
		 if server_to_client:
			exit_with_Zenity('\t/5/ Client closed, because server closed !')
		 else:
		 	try:
		 	 len(readstr)
		 	except:
		 	 exit_with_Zenity('\t/5/ Client closed, because client wants to<white> (^C or process kill by another way) !')
			exit_with_Zenity('\t/5/ Client closed, because reads an EOF signal!')
	try:
	 ANSIColors.printc("\t/0/ <blue>Connection seems to be <green><u>well<U><blue> established<white> with the server <green><u>%s<U><white>," % server_name)
	 ANSIColors.printc("\t/0/ You are identified as the client <green><u>%s<U><white>." % msocket_name)
	 ANSIColors.printc("\t/?/ Enter <blue>\\?<white> for <u>more help<U>.")
	 # Start parallelization with threads
	 thread.start_new_thread(read_write_inverse, (sys.stdin, mfile, 1, msocket_name, server_name))
	 read_write_inverse (mfile, sys.stdout, 0, server_name, msocket_name)
	except SystemExit: # Was surely raised by one of the previous exit_with_Zenity
	 raise
	except:
	 # if some connexion problems appears but not properly handled previously
	 mfile.close()
	 msocket.shutdown(socket.SHUT_RDWR)
	 msocket.close()
	 exit_with_Zenity('/!\\ Connection refused or closed very badly /!\\ Reason : '+str(sys.exc_info()[0])+'.') # Exit
	 # In case the sys.exit doesn't work

#: Help message for this program or this module
#: (Keep in mind that it's mainly designed to be a program, called from the command line)
HELP="""./IRCclient.py [HOST PORT [OPTIONS]] | -z [OPTIONS]

Create a socket on HOST at PORT, and run it a client socket.

Options:
========
 *	-i, --interactive, -z, --zenity	
	Force Zenity interactivity : read args HOST and PORT interactively.
		 with Zenity and PyZenity (don't use it unless you are sure to have both).
 *	-ni, --non-interactive	Disable Zenity interactivity : read args HOST and PORT from command line, Default.
 *	-w	Print << in beginning of every output (experimental).
 *	-v	Be verbous (print usefull informations about connections).
 *	-h, --help	Print this help message.
 *	-a	Print all message incomming from the client or outcomming to the server.
 *	--debug	Launch program in debug mod with pygdb.

Example:
========
	$ ./PyRlwrap.py ./IRCclient.py naereen-corp.crans.org 9312 -v -a

Copyrigths:
===========
 (c) 09/2012
   By Lilian BESSON
    ENS de Cachan (M1 Mathematics & M1 Computer Science MPRI)
    mailto:lbesson[AT]ens-cachan.fr
    
   For Naereen Corp.
    mailto:naereen-corporation[AT]laposte.net
    https:sites.google.com/site/naereencorp/liste-des-projets/irc.
"""

__doc__=HELP

def main(args, HOST=HOST, PORT=PORT):
	""" Create a socket on an host=args[1] with port=int(args[2]), and run a client on it."""
	PRINT_ALL_MESSAGE=('-a' in args)
	WRAPPER_PRINTED=('-w' in args)
	try:
	 if len(args)>1:
	  HOST=args[1]
	 if len(args)>2:
	  PORT=int(args[2])
	 server=(HOST, PORT)
	 ANSIColors.printc("\t/./ <blue>Connection is establishing<white> with the server <green><u>%s:%i<U><white>," % server)
	 msocket=create_socket_client(server)
	except socket.error:
	 exit_with_Zenity('/!\\ Connection refused because server was not responding ! /!\\')
	except: # If connexion couldn't properly initialized
	 exit_with_Zenity('/!\\ Connection refused /!\\ Reason : '+str(sys.exc_info()[0]))
	run_client(msocket, server, PRINT_ALL_MESSAGE, WRAPPER_PRINTED)

def ask_arg(HOST, PORT):
	""" Use PyZenity to ask interactivly the arguments of the program."""
	try:
	 ZHOST=PyZenity.GetText("Please, entry the IPv4 address of the IRC server you want to connect :", HOST, False)
	 ZPORT=PyZenity.GetText("Please, entry the TCP port of the IRC server you want to connect  :", str(PORT), False)
	 if (ZHOST is None) or (ZPORT is None):
	  raise KeyboardInterrupt
	 #print(ZHOST, ZPORT)
	 return ['<ZenityInteractivity>', ZHOST, str(ZPORT), '-a']
	except:
	 PyZenity.ErrorMessage("Error : you must enter both a valid address and a valid port !")
	 PyZenity.InfoMessage( ("The default values %s:%i will be used !" % (HOST, PORT) ))
	 return ['<DefaultValues>', HOST, PORT, '-a']


if __name__ == '__main__':
	if ('-h' in sys.argv) or ('--help' in sys.argv):
	 sys.exit(HELP)
	# Try to know if the current terminal supports ANSI escaped colored codes.
	ANSISupported=(os.getenv('TERM') in ['xterm', 'screen-bce', 'screen', 'linux', 'xterm256']) and (sys.platform in ['linux', 'linux2'])
	# Disable all escape codes for color to be generated 
	if not(ANSISupported):
		ColorOff()
	else: ColorOn()
	if ('--interactive' in sys.argv) or ('-i' in sys.argv) or ('-z' in sys.argv) or ('--zenity' in sys.argv): # Force Zenity mod
		AsZenity=True
	# Determine ARGS
	if ('--non-interactive' in sys.argv) or ('-ni' in sys.argv) or not(AsZenity):
		ARGS=sys.argv
	else:
		ARGS=ask_arg(HOST, PORT)
	#print ARGS
	if '--debug' in ARGS:
	 import pdb
	 pdb.run('main(ARGS)')
	else:
	 main(ARGS)

#END
