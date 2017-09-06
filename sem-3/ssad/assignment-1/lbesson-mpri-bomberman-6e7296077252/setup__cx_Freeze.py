#! python
# -*- coding: utf-8 -*-
"""
Distutils+cx_Freeze Freezer script for my MPRI-Bomberman game.
Still very experimental.

More information on
===================
- https://bitbucket.org/lbesson/mpri-bomberman/ for the source
- https://docs.python.org/2/distutils/setupscript.html for the details on setup.py scripts
- http://cx-freeze.readthedocs.org/en/latest/distutils.html#distutils for doc on cx_Freeze

TODO?
=====
- include images (in a CLEAN and automatic way... ?)


FIXME
=====
- received input from user is not working AT all (there might be a simple reason for that, go through PyGame doc for the modules I used)
- the UI is freezing at some point (even for the IA that are playing allone)
- fix bug when a client is disconnected : server is bugging
- fix bug : \n end on messages?
- x not in list x (I received the exception ...)


MORE?
=====
- include sound again (find a way to play it !!)
- test on two machines (test on 4 machines, and compatibility between Linux/Windows)
- create a .exe/.msi installer when everything will work well


@date: Mon Feb 25 16:15:21 2015.
@author: Lilian Besson for CS101 course at Mahindra Ecole Centrale 2015.
@license: GNU Public License version 3.
"""

import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
    path = sys.path,  # FIXME useless?
    include_msvcr = True,  # Include the MS VCR dll
    compressed = True,  # Compress the zip file
    optimize = 2,  # 0, 1 or 2. 2 is longer but produces smaller files
    init_script = 'Console',  # FIXME: it might be loading the thing from C:\Anaconda\... and not from the local folder
    # FIXME ?
    # Dependencies are automatically detected, but it might need fine tuning.
#    packages = ['os', 'sys', 'time', 'socket', 'select', 'copy', 'random', 'time', 'thread', 'scanf', 'socket', 'cPickle', 'pickle', 'argparse', 'subprocess', 'pygame', 'pygame.locals', 'Constants', 'ANSIColors', 'Matrix', 'Player', 'Board', 'ParseMessageOut', 'ParseMessageIn', 'AffichPygame'],
#    includes = ['os', 'sys', 'time', 'socket', 'select', 'copy', 'random', 'time', 'thread', 'scanf', 'socket', 'cPickle', 'pickle', 'argparse', 'subprocess', 'pygame', 'pygame.locals', 'Constants', 'ANSIColors', 'Matrix', 'Player', 'Board', 'ParseMessageOut', 'ParseMessageIn', 'AffichPygame'],
    excludes = ['numpy', 'scipy'],  # do not include LAPACK and co
)

# Options for the executables (http://cx-freeze.readthedocs.org/en/latest/distutils.html#cx-freeze-executable)
compress = True
icon = 'bomberman.ico'  # works well, but .png does not


# For a graphical program (not the case here)
# FIXME: after, the client and IA might be like this (in fact no... ?)
base_gui = None
if sys.platform == "win32":
    base_gui = "Win32GUI"

# For a console program
base_console = 'Console'


print "Building the three executables"
executables = [
    Executable('IRCserver.py',
               base=base_console, compress=compress),
    Executable('IRCclient.py',
               base=base_console, compress=compress),
    Executable('AffichPygame.py',
               base=base_console, icon=icon, compress=compress),
    Executable('BombermanServer.py',
               base=base_console, icon=icon, compress=compress),
    Executable('BombermanClient.py',
               base=base_console, icon=icon, compress=compress),
    Executable('IA_Bomberman.py',
               base=base_console, icon=icon, compress=compress)
]

setup(name='MPRI Bomberman (alpha demo)',
      version = '1.0',
      description = 'MPRI-Bomberman : multi-player Bomberman game written in Python 2.7 with PyGame (alpha demo)',  # FIXME one description for each executable
      license = 'GNU Public License (version 3)',
      author='Lilian Besson for CS101 course at Mahindra Ecole Centrale 2015.',
      author_email = 'CS101' + '@' + 'crans.org',
      url = 'http://perso.crans.org/besson/cs101/',
      options = dict(build_exe = build_exe_options),
      # Now we decide what to compile
      executables = executables,
      package_dir = {
          'BombermanServer': 'BombermanServer.py',
          'BombermanClient': 'BombermanClient.py',
          'IA_Bomberman': 'IA_Bomberman.py',
          'AffichPygame': 'AffichPygame.py'
      },
      # FIXME auto including of all the images does not work yet
      package_data = {
#          'BombermanClient': ['datas'],
#          'IA_Bomberman': ['datas'],
          'BombermanClient': ['datas/48_48/*.png'],
          'IA_Bomberman': ['datas/48_48/*.png'],
          'AffichPygame': ['datas/48_48/*.png']
      },
      data_files = [
#          ('datas', ['datas/*']),
          ('datas/48_48/', ['datas/48_48/*.png']),
      ],
)

print "Done with building... Check the dist/exe.win-amd64-2.7 folder for more details."
