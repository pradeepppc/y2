#!/usr/bin/python
# -*- encoding: utf-8 -*-

""" A simple IRC server.
 From TP1 of MPRI Courses "Net Project".
 Ex2 (QU3) (QU4) (QU5) (QU6)

.. warning::
   This script is **deprecated**, don't use it.
"""

__author__='Lilian BESSON (mailto:lilian.besson[AT]normale.fr)'	# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__version__='0.95'
__date__='jeudi 07 02 2013, at 23h:17m:30s'	#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.

import socket, sys, select, os

# Non usual module ! FIXME : explain how to install it
import ToolReadline	# ToolReadline.py : uses readline to allow beautiful text inputs.
import ANSIColors	# ANSIColors.py : just some colors definition.

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
	AsZenity=False #: Here disabled
except:
	print "\t/!/ Zenity not found : read arguments from the command line."
#: Args for all Zenity call
kwargs={'title':'IRC server', 'window-icon':'server'}

def exit_with_Zenity(msg_erreur):
	""" A remplacement for sys.exit : print an error message with Zenity before executing sys.exit.
	"""
	if AsZenity:
		PyZenity.ErrorMessage(msg_erreur)
	sys.exit(msg_erreur)

HOST, PORT='127.0.0.1', 2048	#: Default values
PRINT_ALL_MESSAGE=1		#: 1 to print messages
LISTEN_NB_CST=16		#: Nb of input socket authorized (a max)

def create_bind_socket(server = (HOST, PORT)):
	""" Create a socket and bind it to the port @port and the addresse @host."""
	msocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	msocket.bind(server)
	msocket.listen(LISTEN_NB_CST)
	return(msocket)

def create_data_socket(listen_socket, NB_CLIENT=0):
	""" Create a data socket from the socket @listen_socket."""
	mfile=listen_socket.makefile()
	data_socket, data_address=listen_socket.accept()
	NB_CLIENT+=1
	ANSIColors.printc('\t/3/ A client connects to <green>addr:%s with port:%i<white>,' % data_address)
	ANSIColors.printc('\t/3/ This client is the <black>%ith<white> to connects.' % NB_CLIENT)
#	sys.stdout.flush()
	return(data_socket, data_address, NB_CLIENT)

#: Pieces of text to be printed before each input, and each output.
WRAPPER_OUT='$:OUT: '	#: Piece of text to be printed before each output.
WRAPPER_IN=':IN:$ '	#: Piece of text to be printed before each input.

def broadcast_message_list(message = 'No message was gave', list_client = [], origin='UNKNOW', PRINT_ALL_MESSAGE=PRINT_ALL_MESSAGE):
	""" Broadcast the message @message to each of the client in a list of client @list_client.
	@origin permits to print some usefull informations for delivering the origin of the message the all connected clients."""
	for client in list_client:
		fclient=client.makefile()
#:		fclient.write('From['+origin+']'+WRAPPER_OUT + message)
		fclient.write(message)
		fclient.flush()
	if PRINT_ALL_MESSAGE:
	 ANSIColors.printc('\t/1/ The message [<yellow>%s<white>], tagged from %s, <green>is delivering<white> to all <u>%i other clients<U>,' % ((message[:(len(message) - 1)] ), origin, len(list_client)))
#	 sys.stdout.flush()

##########################
##### User interface #####

#: The help message, which can be printed to the user when invoking *'\\?'*
help_User="""
Welcome in IRC server v%s.
	Wrote by %s, last version dated of %s.
	Wrote in Python 2.6+, using PyZenity for interactive interface, and ANSIColors for colors in output messages.
	Reference page for this software is : https://sites.google.com/site/naereencorp/liste-des-projets/irc.

Your are an IRC server, which accepts client using UDP sockets.
All messages enter from here will be broadcasted to all connected clients, and here are printed all messages from other clients, connection and disconnection of clients, and more.

The following commands are enabled :
	\\h, \\help, \\? : print this help,
	\\out : logout (as like Ctrl+D),
	\\kill <ADDR, PORT> : close manually the clients registering with (ADDR, PORT).
	  /!\\ NOT YET IMPLEMENTED FIXME
""" % (__version__, __author__, __date__)

def action_on_readstr(readstr):
	""" Reaction to special message readed from the keyboard !"""
	if readstr in ['\\h\n', '\\help\n', '\\?\n']:
		ANSIColors.printc('\t/?/ <blue>Help : \\h or \\help or \\?<white>:')
		print help_User
		return True
	if readstr in ['\\out\n']:
		ANSIColors.printc('\t/!/ <red>Server closed<white>, because <green>server wants to, by sending an EOF signal with \\out command !<white>')
		os._exit(0)
	if readstr in ['\\kill\n']:
		ANSIColors.printc("""\t \\kill <ADDR, PORT> : close manually the clients registering with (ADDR, PORT).
	  <red><u>/!\\ NOT YET IMPLEMENTED FIXME !<U><white>""")
	  	return True
	return False

# Main function
def irc_server(server = (HOST, PORT), PRINT_ALL_MESSAGE=PRINT_ALL_MESSAGE):
	""" Create a server with addr,port=@server, listening on HOST at PORT,
	 and run it as a server which accepts client on it and broadcast every message from on client to all the other clients.
	 Returns the socket_server when all connections are closed or the server decides to close himself.

	Attention : to be respectuous of TCP conventions, if the connection is closed from the server stdin (Ctrl + C), the returned socket has to be closed by the programmer.

	DEBUG, PRINT_ALL_MESSAGE: are options for parametrize behaviour of client."""
	list_client=[]
	dict_client=[]
	NB_CLIENT=0
	socket_server=create_bind_socket(server)
	ANSIColors.printc('\t/0/ <green>Server IRC <u>seems<U> to be well initialized...<white>')
	ANSIColors.printc("\t/?/ Enter <blue>\\?<white> for <u>more help<U>.")
	try:
	 while 1:
		list_listen=list_client + [socket_server, sys.stdin]
		list_in, ee, eee = select.select(list_listen, [], []) # ee and eee useless
		for socket_in in list_in:
#		 print socket_in
		 if(socket_in is sys.stdin):
		   read_msg=sys.stdin.readline()
		   if action_on_readstr(read_msg):
		    continue
		   if len(read_msg)==0:
		   	ANSIColors.printc('\t/9/ Server sends <u>an EOF signal<U> : <red>server is closing<white> ...')
		   	raise KeyboardInterrupt
		   ANSIColors.printc('\t/1/ Server <blue>%s:%i <green>sends a message<white>.' % server)
		   origin='Server[%s:%i]' % (server)
		   broadcast_message_list(read_msg, list_client, origin)
		 else:
		  file_in=socket_in.makefile()
		  if(socket_in is socket_server):
		 	new_client, address_client, NB_CLIENT=create_data_socket(socket_server, NB_CLIENT)
			for client in list_client:
			  fclient=client.makefile()
			  fclient.write(ANSIColors.sprint('\t/3/ A new client connects to <green>addr:%s with port:%i<white>,\n' % address_client))
			  fclient.write(ANSIColors.sprint('\t/3/ This client is the <blue>%ith<white> to be connected to the <u>same<U> IRC Server as yourse !\n' % NB_CLIENT))
			  fclient.flush()
		 	list_client.append(new_client)
		 	dict_client.append(address_client)
		  else:
#		  	indice_client=list_client.index(socket_in)
#		 	address_client=dict_client[indice_client]
		  	address_client=socket_in.getpeername()
#		  	print (socket_in.getpeername() == address_client)
#		  	print socket_in.getpeername()
#		  	print dict_client.index(address_client)
		 	indice_client=dict_client.index(address_client)
		 	ANSIColors.printc('\t/=/ Listening to client <blue>%s<white>, number <red>%s<white> :' % (str(address_client), str(indice_client)))
		 	# Read a message from of the available client
		 	read_msg=file_in.readline()
		 	if len(read_msg)>0:
		 	 list_client.remove(socket_in)
		 	 ANSIColors.printc('\t/1/ Client <blue>%s:%i <green>sends a message<white> :' % address_client)
		 	 origin='Client[%s:%i]' % address_client
		 	 broadcast_message_list(read_msg, list_client, origin)
		 	 list_client.append(socket_in)
		        else: # nothing readed from the client : he logged out or exited
		 	 socket_in.shutdown(socket.SHUT_RDWR)
		 	 socket_in.close()
		 	 dict_client.remove(address_client)
		 	 list_client.remove(socket_in)
		 	 ANSIColors.printc('\t/5/ Client <green>%s:%i<white> <red><u>logged out<U><white> !' % address_client)
			 for client in list_client:
			   fclient=client.makefile()
			   fclient.write(ANSIColors.sprint('\t/5/ Client %s:%i logged out !\n' % address_client))
			   fclient.flush()
	except:
		ANSIColors.printc('\n\t/6/ <red>Server is closing<white>, because <blue>server wants to<white> !')
		for isocket in list_client:
			fclient=isocket.makefile()
			fclient.write(ANSIColors.sprint('\n\t/6/ Server <green>%s:%i<white> <red><u>is closing because he ask to : you are getting disconnected !<U><white> Bye !\n' % server))
			isocket.close()
			#isocket.shutdown(socket.SHUT_RDWR)
#		#socket_server.shutdown(socket.SHUT_RDWR)
		socket_server.close()
		exit_with_Zenity('\t/6/ All connected clients may be closed, and server exit properly ! Bye !')


##########################
##### User interface #####

#: Help message for this program or this module
#: (Keep in mind that it's mainly designed to be a program, called from the command line)
HELP="""./IRCserver.py [HOST PORT [OPTIONS]] | -z [OPTIONS]

Create a server listening on HOST at PORT, and run it as a server which accepts client on it and broadcast every message from on client to all the other clients.

Options:
========
 *	--interactive, -i, -z, --zenity	Force Zenity interactivity : read args HOST and PORT interactively,
		 with Zenity and PyZenity (don't use it unless you are sure to have both).
 *	-ni, --non-interactive	Disable Zenity interactivity : read args HOST and PORT from command line, Default.
 *	-h,--help	Print this help message.
 *	-a	Print all message incomming from the client or outcomming to the server with verbous information.
 *	--debug	Launch program in debug mod with pygdb.

Example:
========
	$ ./PyRlwrap.py ./IRCserver.py naereen-corp.crans.org 9312 -a

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

if __doc__:	__doc__=__doc__ + '\n' + HELP	#FIXME ?

def main(args, HOST=HOST, PORT=PORT):
	""" Create a socket on an host=args[1] with port=int(args[2]),
	 and run a client on it."""
	try:
		PRINT_ALL_MESSAGE=('-a' in args)
		if len(args)>1:
		  HOST=args[1]
		if len(args)>2:
		  PORT=int(args[2])
		ANSIColors.printc('\t/0/ <blue>Server IRC is initializing at <green><u>%s:%i<U><white>...' % (HOST, PORT))
		sys.stdout.flush()
		irc_server( (HOST, PORT), PRINT_ALL_MESSAGE)
	except SystemExit:
		raise
	except KeyboardInterrupt:
		raise
	except socket.error:
	 exit_with_Zenity('/!\\ Connection refused because server was able to launch ! /!\\\n\tMaybe the port %i is already used on the address %s' % (PORT, HOST))
	except:
		exit_with_Zenity('/!\\ Connection refused or closed very badly /!\\ Reason : '+str(sys.exc_info()[0])) # Exit
	 # In case the sys.exit doesn't work

#: Args for all Zenity call
kwargs={'title':'IRC server', 'window-icon':'server'}

def ask_arg(HOST, PORT):
	""" Use PyZenity to ask interactivly the arguments of the program.
	"""
	try:
	 ZHOST=PyZenity.GetText("Please, entry a valid IPv4 address for this IRC server :", HOST, False)
	 if (ZHOST is None):
	  raise KeyboardInterrupt
	 ZPORT=PyZenity.GetText("Please, entry an open TCP port for this IRC server :", str(PORT), False)
	 if (ZPORT is None):
	  raise KeyboardInterrupt
	 return ['<ZenityInteractivity>', ZHOST, str(ZPORT), '-a']
	except:
	 PyZenity.ErrorMessage("Error : you must enter both a valid address and a valid port !")
	 PyZenity.InfoMessage( ("The default values %s:%i will be used !" % (HOST, PORT) ))
	 return ['<DefaultValues>', HOST, PORT, '-a']


if __name__ == '__main__':
	if ('-h' in sys.argv) or ('--help' in sys.argv):
	 exit_with_Zenity(HELP)
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
	if '--debug' in ARGS:
	 import pdb
	 pdb.run('main(ARGS)')
	else:
	 main(ARGS)

#END
