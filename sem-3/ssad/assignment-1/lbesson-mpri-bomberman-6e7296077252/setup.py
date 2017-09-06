#!/usr/bin/env python
# -*- coding: utf8 -*-
""" Install script for the three MPRI Bomberman programs (independantly from each other)."""
# http://cx-freeze.readthedocs.org/en/latest/distutils.html#distutils-setup-script

import sys
from cx_Freeze import setup, Executable
print "setup.py has been called."

# Dependencies are automatically detected, but it might need fine tuning.

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Options
# (cf. http://cx-freeze.readthedocs.org/en/latest/distutils.html for more options)
options = {
    # "bdist_msi": { }  # FIXME: for Windows
    # "bdist_dmg": { }  # FIXME: for Mac OS X
    "build_exe": {
        "compressed": True,
        "includes": [
            # Pygame utilise numpy
            "pygame",
            "pygame.locals",
            "numpy",
            "numpy.core",  # FIXME
            "numpy..core",  # FIXME
            # # Mine  # FIXME
            "AffichPygame",  # /home/lilian/mpri-bomberman/
            "ANSIColors",  # /home/lilian/mpri-bomberman/
            "Board",  # /home/lilian/mpri-bomberman/
            "Bomb",  # /home/lilian/mpri-bomberman/
            "BombermanClient",  # /home/lilian/mpri-bomberman/
            "BombermanServer",  # /home/lilian/mpri-bomberman/
            "Bonus",  # /home/lilian/mpri-bomberman/
            "ConfigClient",  # /home/lilian/mpri-bomberman/
            "ConfigServer",  # /home/lilian/mpri-bomberman/
            "Constants",  # /home/lilian/mpri-bomberman/
            # "IA_Bomberman",  # /home/lilian/mpri-bomberman/
            "KeyBinding",  # /home/lilian/mpri-bomberman/
            "Matrix",  # /home/lilian/mpri-bomberman/
            "ParseCommandArgs",  # /home/lilian/mpri-bomberman/
            "ParseMessageIn",  # /home/lilian/mpri-bomberman/
            "ParseMessageOut",  # /home/lilian/mpri-bomberman/
            "Player",  # /home/lilian/mpri-bomberman/
            "PyZenity",  # /home/lilian/mpri-bomberman/
            "scanf",  # /home/lilian/mpri-bomberman/
            "SimpleGame",  # /home/lilian/mpri-bomberman/
            "ToolReadline",  # /home/lilian/mpri-bomberman/
            # Basic modules
            "os",
            "pickle",
            "sys"
        ],
        "include_files": [
            "bomberman.png",  # /home/lilian/mpri-bomberman/
            "bomberman.gif",  # /home/lilian/mpri-bomberman/
            "datas/"  # /home/lilian/mpri-bomberman/
        ],
        "path": sys.path + ["/home/lilian/mpri-bomberman"],  # FIXME ?
        # # I do not understand the goal of this option
        # "replace_paths": [
        #     ("/home/lilian/mpri-bomberman/", ""), # "/home/lilian/mpri-bomberman/build/"),
        #     ("/usr/lib/python2.7/dist-packages/", "") # "/home/lilian/mpri-bomberman/build/")
        # ],
        "packages": [
            "pygame",
            "pygame.locals",
            "numpy",
            "numpy.core",  # FIXME
            "numpy..core",  # FIXME
            # # Mine  # FIXME
            "AffichPygame",  # /home/lilian/mpri-bomberman/
            "ANSIColors",  # /home/lilian/mpri-bomberman/
            "Board",  # /home/lilian/mpri-bomberman/
            "Bomb",  # /home/lilian/mpri-bomberman/
            "BombermanClient",  # /home/lilian/mpri-bomberman/
            "BombermanServer",  # /home/lilian/mpri-bomberman/
            "Bonus",  # /home/lilian/mpri-bomberman/
            "ConfigClient",  # /home/lilian/mpri-bomberman/
            "ConfigServer",  # /home/lilian/mpri-bomberman/
            "Constants",  # /home/lilian/mpri-bomberman/
            "IA_Bomberman",  # /home/lilian/mpri-bomberman/
            "KeyBinding",  # /home/lilian/mpri-bomberman/
            "Matrix",  # /home/lilian/mpri-bomberman/
            "ParseCommandArgs",  # /home/lilian/mpri-bomberman/
            "ParseMessageIn",  # /home/lilian/mpri-bomberman/
            "ParseMessageOut",  # /home/lilian/mpri-bomberman/
            "Player",  # /home/lilian/mpri-bomberman/
            "PyZenity",  # /home/lilian/mpri-bomberman/
            "scanf",  # /home/lilian/mpri-bomberman/
            "SimpleGame",  # /home/lilian/mpri-bomberman/
            "ToolReadline",  # /home/lilian/mpri-bomberman/
            # Basic modules
            "os",
            "pickle",
            "sys"
        ],
        "excludes": ["Tkinter"],
        # FIXME: exclude also  , "pygame.tests", "pygame.examples"],
        "silent": True
    }
}


# http://cx-freeze.readthedocs.org/en/latest/distutils.html#cx-freeze-executable
# Build 3 executables
executables = [
    Executable(
        script="BombermanServer.py",
        # initScript="Console",
        base=base,
        icon="bomberman.png"),
    Executable(
        script="BombermanClient.py",
        # initScript="Console",
        base=base,
        icon="bomberman.png"),
    Executable(
        script="IA_Bomberman.py",
        # initScript="Console",
        base=base,
        icon="bomberman.png")
]

# Launch cx_Freeze setup command
setup(
    # FIXME: Name of many executables?
    name="MPRI Bomberman",
    author="Lilian Besson",
    author_email="bessonATcrans.org".replace("AT", "@"),
    download_url="https://bitbucket.org/lbesson/mpri-bomberman/downloads/",
    license="GPLv3",
    options=options,
    executables=executables,
    # FIXME: Description of many executables?
    description="MPRI Bomberman game -- (C) Lilian Besson 2012-15",
    version="0.1a"
)


# TODO: see http://www.py2exe.org/index.cgi/Tutorial for Windows.

# TODO: At the end, on Windows, we should make a self-extracting archive thanks to IExpress (https://en.wikipedia.org/wiki/IExpress).
# (cf. https://en.wikipedia.org/wiki/Self-extracting_archive)

# TODO: see https://pythonhosted.org/py2app/ for Mac OS X.
