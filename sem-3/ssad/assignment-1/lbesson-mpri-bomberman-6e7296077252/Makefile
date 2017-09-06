# Makefile for Sphinx documentation
#
#	This script is designed to be used with makePydoc, update__date__ and pylint.
#	The reference page for this software is :
#	https://sites.google.com/site/naereencorp/liste-des-projets/makepydoc
#
#	__author__='Lilian BESSON'
#	__email__='lilian.besson at normale dot fr'
#	__version__='12.3'
#	__date__='jeu. 14/02/2013 at 05h:18m:10s '
#
# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

###############################################################################
# Custom items
CP = /usr/bin/rsync --verbose --times --perms --compress --human-readable --progress --archive
#CP = scp
# an alias to remplace scp

total:	cleanALL all sendAll notify
	@echo "Pylint evaluated your code :"
	@grep -A 1 "Your code has been rated at" pylint/pylint_global.html

local:	cleanALL all notify

complete:	cleanALL update__date__ all sendAll notify

complete_doxygen: cleanALL update__date__ all doxygen sendAll notify

all:	pytorst pylint coverage pyreverse html html pyDoc rapport clean_pyc

notify:
	notify-send "Sphinx" "Generating documentation : done !"

notify_archive: archive
	notify-send "Sphinx : archiving" "Generating archive : done ! (~/projet_reseau.tar.gz)"

cleanALL: clean_build clean_pyc clean_pylint clean_pyreverse

clean_pyreverse:
	rm -f images/classes_*.svg images/packages_*.svg
	rm -f images/classes_*.png images/packages_*.png

pyreverse: clean_pyreverse
	./pyreverse.sh
	mv packages_Bomberman.* images/
	mv classes_Bomberman.* images/

pychecker:
	pychecker -# 1000 -t -9 -v -g -n -a -I -8 -1 -A -S self --changetypes -6 -q -m -c -f [A-Z]*.py

pyflakes:
	pyflakes [A-Z]*.py

clean_pylint:
	rm -f pylint/*.html _build/html/pylint/*

pylint: clean_pylint
	cd pylint/ && pylint -f html --files-output=y ../*.py; cd ..
	mkdir -p _build/html/pylint/
	cp pylint/* _build/html/pylint/
	./pylint.sh

doxygen:
	doxygen Doxyfile

archive: clean_pyc
	if [ -f ~/projet_reseau.tar.xz ]; then mv -f ~/projet_reseau.tar.xz ~/Documents/ ; fi
	## tar -jcvf ~/projet_reseau.tar.bz2 ./
	tar -Jcvf ~/projet_reseau.tar.xz ./

sendAll: notify_archive send

send: send_dpt send_zamok

send_dpt:
	$(CP) -r ./ lbesson@ssh.dptinfo.ens-cachan.fr:~/public_html/publis/Bomberman/
	$(CP) ~/projet_reseau.tar.xz lbesson@ssh.dptinfo.ens-cachan.fr:~/public_html/

send_zamok:
	$(CP) -r ./ besson@zamok.crans.org:~/www/publis/Bomberman/
	$(CP) ~/projet_reseau.tar.xz besson@zamok.crans.org:~/www/

pytorst:
	./pytorst.sh *.py
	@echo "Erase the conf.rst (conf.py is the Sphinx configuration file)."

clean_pyc:
	rm -f *.*~ *.py[co] */*.*~ */*.py[co]
	@echo "All *.pyc (Python compiled scripts) and *.py~ (temporary copies) files have been deleted !"
	rm -f savegame.ess .PyRlwrap.history .python.history.py database_clients.list
	@echo "The files savegame.ess .PyRlwrap.history .python.history.py database_clients.list, have been deleted !"

clean_build:
	cp -r _build _build_old/
	rm -rf _build/*

pyDoc:
	./makePydoc.sh

rapport:
	rst2pdf -s ./style.rst2pdf -l fr --default-dpi=1000 --baseurl="http://perso.crans.org/besson/publis/Bomberman/" -o MPRI_Bomberman_doc_fromRST.pdf -c rapport.rst.pytorst  #
#	cp _build/html/rapport.html ./
#	$(SPHINXBUILD) -b latex ./ $(BUILDDIR)/latex_rapport/ rapport.rst.pytorst
#	$(MAKE) -C $(BUILDDIR)/latex_rapport all-pdf
#	pdflatex $(BUILDDIR)/latex_rapport/MPRI_Bomberman_doc.tex && pdflatex $(BUILDDIR)/latex_rapport/MPRI_Bomberman_doc.tex

specif:
	pdflatex specification.tex && pdflatex specification.tex && hevea -o specification.html specification.tex
	pdflatex specification_slides.tex && pdflatex specification_slides.tex

update__date__:
	./update__date__.sh

coverage:
	$(SPHINXBUILD) -b coverage $(ALLSPHINXOPTS) $(BUILDDIR)/coverage
	@echo
	@echo "Build finished. The coverage pages are in $(BUILDDIR)/coverage."

########################## End of custom stuffs ###############################
###############################################################################

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  total      to make all the doc"
	@echo "  complete   to change dates and make all the doc"
	@echo "  all        to make all but no change and no synchronization"
	@echo "  notify     to simply notify the user that doc is done"
	@echo "  archive    to make an archive .tar.gz that contain the current repertory (and put it in ~/)"
	@echo "  pyreverse  generate a classes_[NAME OF THE PROJECT].png showing the UML diagram."
	@echo "  pyflakes   static and basic analysis for *ALL* .py modules in the main dir"
	@echo "  pychecker  static and a little bit advanced analysis for *ALL* .py modules in the main dir"
	@echo "  pylint     run a *complete* pylint execution for *ALL* .py modules in the main dir, and move the result to pylint/"
	@echo "  doxygen    to make the doc with doxygen and not with sphinx (it's bad, don't do it)"
	@echo "  complete_doxygen  to make like complete, but with doxygen"
	@echo "  sendAll    to copy all the content to a distant ssh server, using scp and not rsync)"
	@echo "  clean_build to move all _build/* in _build_old/"
	@echo "  specif     to generate specifications using pdflatex and hevea (from specification.tex and specification_slides.tex)"
	@echo "  update__date__  to change all __date__ variables to show the progression of your work"
	@echo "  coverage       to make coverage files (listing of non documented objects)"
	@echo "  // other Sphinx only options :"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  gettext    to make PO message catalogs"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/MPRIBombermanNetProgrammingProject.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/MPRIBombermanNetProgrammingProject.qhc"

devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/MPRIBombermanNetProgrammingProject"
	@echo "# ln -s $(BUILDDIR)/devhelp $$HOME/.local/share/devhelp/MPRIBombermanNetProgrammingProject"
	@echo "# devhelp"

epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
