#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" A configuration file for the **client**.

You can edit it to fit your favorite configuration.

Example:
^^^^^^^^

This show how the **textual mode** *looks like when *ANSI* Colors are disabled (for the *client* with option *--noANSI*) :

.. image:: images/exempletextual_noANSI.*
   :scale: 100 %
   :align: center

This show how the **textual mode** *looks like when *UTF* caracters are disabled (for the *client* with option *--noUTF*) :

.. image:: images/exempletextual_noUTF.*
   :scale: 100 %
   :align: center

List of all parameters
======================
"""

# Automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__author__='Lilian BESSON'
__email__='lilian.besson[AT]normale.fr'
__license__='GPLv3'
__version__='1.1a'	#: Version of this module
#: The date of the file, automatically update with update__date__.sh, a Naereen Corp. (c) bash script.
__date__='mer. 20/02/2013 at 19h:05m:40s '

###############################################################################
#: The name of the profile.
profile_name	=	"Client, version of %s." % __date__

#:Number of loop each seconds.
#:
#:.. warning::
#:   If too slow the game is not playable.
#:   If too quick, *PyGame* might complain about it.
#:   10 is good :)
CLOCK_FREQUENCY	=  10.0

#: If music will be used.
USE_MUSIC	=	False

#: If sound effects will be used.
USE_SOUND_EFFECT	=	True

#: If a graphical window will be used.
USE_WINDOW	=	True

#: If notifications (with *notify-send*) will be used.
USE_NOTIFY	=	True

#:To use the window in Full screen.
#:
#:.. warning::
#:   By now, fullscreen mod **is not supported**.
#:   It is still experimental.
#:   So, if you are curious, try it :) !
USE_FULLSCREEN	= False

try:
	from os import getlogin, getpid
	pseudo_Init = "Default" + "_" + str(getpid())
#:	pseudo_Init = getlogin().capitalize() + "_" + str(getpid())
	del getlogin, getpid
except:
#:	from os import getpid
#:	pseudo_Init = "Default" + "_" + str(getpid())
#:	del getpid
#:finally:
	pseudo_Init = "Default"

#: Your default color
color_Init	=	"cyan"

#: The default server.
#:
#:.. warning::
#:   This one is on *local* mode.
#:
#:.. seealso::
#:   You might set a *real* server, like *bomberman.crans.org*.
SERVEUR_INIT	=	'0.0.0.0'	# '138.231.139.176'

#: The port of the listening connection for the server.
PORT_INIT	=	12882

#: 1 to print messages
PRINT_ALL_MESSAGE	=	1

#: To be very verbous with all **outputed** messages (*i.e.* send to the network), produced with ParseMessageOut
#:PRINT_ALL_PARSEOUT	=	True

#: To be very verbous with all **parsed** messages, produced with ParseMessageIn
#:PRINT_ALL_PARSEIN	=	True

#: To check action on client side before sending them for validation.
#:  Still not well functional.
#:PLAYER_CHECK_ACTION	=	False

###############################################################################
