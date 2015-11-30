# Makefile para la aplicación epbdcalc / pyebpd
# Rafael Villar Burke, Daniel Jiménez González, 2015

# Para la generación del instalador para Win32 es necesaria la instalación de:
# - NSIS installer (makensis)
# - Plugin NewAdvSplash de NSIS
# - Compresor UPX
#   # La creación del instalador para Win32 se puede hacer en Windows o Linux
# La versión para win32 se hace con MSYS2

PYTHON = python


APPNAME=epbdcalc
VERSION=$(shell python -c"from pyepbd import __version__;print __version__")
ARCH=$(shell uname -m)
DATE=$(shell date +'%Y%m%d')
#_thisdir="$(dirname $0)"
UPXPATH?=$(subst /,\/,$(shell which upx))
DISTDIR?=$(subst /,\/,build/exe.mingw-2.7)
MAKENSIS?=$(shell which makensis)

# Create README.html from README.rst
PYRSTEXISTS:=$(findstring .py, $(shell which rst2html.py))
ifeq ($(PYRSTEXISTS), .py)
$(info Encontrado rst2html.py)
RST2HTML=rst2html.py
else
$(info Encontrado rst2html)
RST2HTML=rst2html
endif

#make windows installer by default
winbuild: manual README.html freeze installer

manual: ./docs/build/Manual_epbdcalc.pdf
	cp $< .

freeze: setup_exe.py
	$(PYTHON) setup_exe.py build
	sleep 5s

installer: setup.nsi
	$(MAKENSIS) setup.nsi

README.html: README.rst res/style.css
	$(RST2HTML) --stylesheet=./res/style.css README.rst > $@

setup.nsi: setup.nsi.in pyepbd/__init__.py
	sed 's/@APPNAME@/$(APPNAME)/g; s/@VERSION@/$(VERSION)/g; s/@ARCH@/$(ARCH)/g; s/@DATE@/$(DATE)/g; s/@UPXPATH@/$(UPXPATH)/g; s/@DISTDIR@/$(DISTDIR)/g' setup.nsi.in > setup.nsi

test check tests:
	pytest

clean:
	rm -rf build dist MANIFEST setup.nsi README.html Manual_epbdcalc.pdf
	find . -name *.pyc -exec rm {} \;
	find . -name *.swp -exec rm {} \;

# Los phony son los que no dependen de archivos y hay que considerar siempre no actualizados (rebuild)
.PHONY = setup.nsi winbuild clean test check tests
