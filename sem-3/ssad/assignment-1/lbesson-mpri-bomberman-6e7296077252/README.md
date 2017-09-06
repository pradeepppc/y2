MPRI 1-21 net programming project
=================================
> A multi-player Bomberman game, with formal semantics and an open protocol.


This repository hosts a fork of [my initial game](https://bitbucket.org/lbesson/mpri-bomberman/), to update it a little bit on Linux (Ubuntu 14.10), and use it as a demo of awesome Python 2.7 features for the CS101 Course at Mahindra Ecole Centrale (spring semester 2015).


----

![Screenshot of the game, for the server](http://perso.crans.org/besson/publis/Bomberman/images/exempletextual_server.png "Screenshot of the game, for the server")


----

### Author:
Lilian Besson (*for more details, see the AUTHOR file in the source*).

### Language:
Python v2.7.8

**Warning:** all what follows might be outdated, as I wrote it two years ago (and I do not have time to read it again and update it).

----

Documentation
-------------
The doc can be consulted on one of this page :

* on **ENS de Cachan** website : [publis/Bomberman/_build/html/](http://www.dptinfo.ens-cachan.fr/~lbesson/publis/Bomberman/_build/html/ "Hosted by the dpt info of 'ENS de Cachan'").
* on **Cr@ns** website [publis/Bomberman/_build/html/](http://perso.crans.org/besson/publis/Bomberman/_build/html/ "Hosted by the 'Cr@ns' association").

**All the details (installation, options, etc) are in the doc**.
Anyway, here are some information.

----

Installation
============
Dependencies
------------
The project is *entirely written in Python* 2.7 (version *2.7.3+* is working).

For more details about the **Python** language, see [the official site](http://www.python.org> "Python power !").
Python 2.7.1 or higher is **required**.

The project also **require** the following *unusual module(s)* :

1. pygame (for GUI): can be found [here on their official site](http://www.pygame.org/download.shtml "Python power !").
2. scanf (for parsing) : **it is** distributed *with the project*. You can also download it [here on Berkeley's website](https://hkn.eecs.berkeley.edu/~dyoo/python/scanf/ "Thank for the developper of this software !").

Plateform(s)
------------
The project have been initially *developped* on *GNU/Linux* (Ubuntu 11.10).
It is (*obviously*) still working is more recent Ubuntu, like the last one 14.10.

#### Warning (Windows)
It also have been quickly tested on *Windows 7* **with the Cygwin environment** and Python 2.7.

The test on Windows *without Cygwin* is still in developpment.

#### Warning (Mac OS X)
It shall also work on *Mac OS X*, but **not been tested**.
Any suggestion or returns is welcome !
Where things can be different between *Mac* and the others plateform is with the *sockets* (Linux use *BSD sockets*, and *Mac* don't).
In particular, some network error handling can work on *Linux* but no on *Mac*.

What is the important part ?
----------------------------
The project is in two parts : **a server, and a client**, represented as the two following Python scripts :

1. the server **BombermanServer.py**;
2. the client **BombermanClient.py**.

Those two can be called with the option `--help` to show how to used them.
All options are explained in this *help* message.

How to quickly use it
---------------------
If you simply want to use it, follow those points :

1. In a first terminal, launch a server (for example from the computer **opened** on the web, and known as *bomberman.crans.org*):

   `$ ./BombermanServer.py --server bomberman.crans.org --port 13882`

   This launch the server, listening on port 13882. The game will be launched with a board 11x11, waiting for 3 players.

2. In *a second terminal*, launch a client and connect it to this server:

   `$ ./BombermanClient.py --server bomberman.crans.org --port 13882 --pseudo "Luke" --color "blue"`

   This launch the game, playing with the server previously launched, and with a player called "Luke", and colored with blue.
   This game uses an interactive window (GUI) if possible, otherwise it will try to launch in text mode (TUI) but *the TUI is still experimental*.

3. Find **2 other friends to play with you**, tell them the `--server` and `--port` argument for their client, and that's it !

4. More options :

	* `--music`, `--nomusic` : **enable**, or **disable** the *soundtrack* during the game (for the client),
	* `--soundeffect`, `--nosoundeffect` : **enable**, or **disable** the *soundeffect* during the game (for the client),
	* `--ANSI`, `--noANSI` : idem for the *ANSI* escape color codes,
	* `--noUTF` : might also be able to force pure ASCII text mode *(it works, but it is uglier than with UTF8 !)*,

5. Moreover, the two files **ConfigClient.py** and **ConfigServer.py** can be edited to keep your favorite parameters from one session to an other.

#### Note
If you are interesting, an *experimental* bot is in progress. That mean, a program that play *by itself*.
 By now, it is **quite limited**, but **it works** :)
 Of course, a *human* player will beat an *automatic* one very easily,
 but at least this allow to test everything without switching between 3 windows to play successively one of each players.
 And as far as I tried, one human player *vs* 7 bots can't win ;)

----

![A client](http://perso.crans.org/besson/publis/Bomberman/images/example_IA.png "Screenshot of the game, for IA clients.")


About the project
=================
This project was realised for the MPRI 1-21 **net programming lesson**. I received the mark *16.9/20* for my work.

The MPRI is the **Parisian Master for Research in Computer Science** (*Master Parisien de Recherche en Informatique* in French).

I worked with *Lucas Hosseini* and *Vincent Cohen-Addad*, and if you are curious, there work is [here on bitbucket](https://bitbucket.org/vcohen/projet_reseau "check this out !").


About the doc
=============
The documentation is produced mainly with **Sphinx**, the Python's documentation generator.

Contact me
----------
Feel free to contact me, either with a bitbucket message (my profile is [lbesson](https://bitbucket.org/lbesson/ "here")), or via an email at **lilian DOT besson AT ens-cachan DOT fr**.

License
-------
This project is released under the **GPLv3 license**, for more details, take a look at the LICENSE file in the source.
*Basically, that allow you to use all or part of the project for you own business.*
