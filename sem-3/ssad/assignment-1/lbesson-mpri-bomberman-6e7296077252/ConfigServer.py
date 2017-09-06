#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" A configuration file for the **server**.

You can edit it to fit your favorite configuration.

List of all parameters
======================
"""

# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__author__='Lilian BESSON'
__email__='lilian.besson[AT]normale.fr'
__license__='GPLv3'
__version__='1.1a'	#: Version of this module
#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__date__='mer. 20/02/2013 at 19h:04m:31s '

###############################################################################
#: The name of the profile.
profile_name	=	"Server, version of %s." % __date__

#:Number of loop each seconds.
#:
#:.. warning::
#:   If too slow the game is not playable.
#:   If too quick, *PyGame* might complain about it.
CLOCK_FREQUENCY	=  40.0

#: If notifications (with *notify-send*) will be used.
USE_NOTIFY		=	True

#:The default server.
#:
#:.. warning::
#:   This one is on *local* mode.
#:
#:.. seealso::
#:   You might set a *real* server, like *bomberman.crans.org*.
#:    *Of course*, this also work perfectly : the game was designed for a *network programming lesson* :).
SERVEUR_INIT	=	'0.0.0.0'	# '138.231.139.176'

#: The port of the listening connection for the server.
PORT_INIT	=	12882

#:If true, use a pickling file to save current game state for the server
#:
#:.. warning::
#:   This is still experimental and quite limited.
#:USE_PICKLING = False

#: To be very verbous with all **outputed** messages (*i.e.* send to the network), produced with ParseMessageOut
#:PRINT_ALL_PARSEOUT	=	True

#: To be very verbous with all **parsed** messages, produced with ParseMessageIn
#:PRINT_ALL_PARSEIN	=	True

#: Max number of bombs allowed to be droped by one player.
#:  Can be changed if you want to try with this.
#:  **To fit our protocole**, and to have the same behaviour that other server,
#:  the default value is **1**.
NB_BOMB_MAX_ALLOW	=  1

###############################################################################
