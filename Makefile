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

# Documentation from LaTeX sources
TEX_SOURCE_DIR :=./docs
TEX_BUILD_DIR :=build
TEX_SRCS := $(shell find ${TEX_SOURCE_DIR} -maxdepth 1 -type f -name '*.tex')
PDF_TARGETS := $(TEX_SRCS:%.tex=%.pdf)
$(info ${TEX_SRCS} ${PDF_TARGETS})

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

manual: ${PDF_TARGETS}

%.pdf:%.tex
	@echo "Conversión de $^ -> $@"
	cd ${TEX_SOURCE_DIR} && pdflatex --output-directory=${TEX_BUILD_DIR} $(notdir $^)
	cd ${TEX_SOURCE_DIR} && pdflatex --output-directory=${TEX_BUILD_DIR} $(notdir $^)
	cp ${TEX_SOURCE_DIR}/${TEX_BUILD_DIR}/$(notdir $@) $(notdir $@)

freeze: setup_exe.py
	$(PYTHON) setup_exe.py build
	sleep 5s

installer: setup.nsi
	$(MAKENSIS) setup.nsi

README.html: README.rst res/style.css
	$(RST2HTML) --stylesheet=./res/style.css README.rst > $@

setup.nsi: setup.nsi.in pyepbd/__init__.py
	sed 's/@APPNAME@/$(APPNAME)/g; s/@VERSION@/$(VERSION)/g; s/@ARCH@/$(ARCH)/g; s/@DATE@/$(DATE)/g; s/@UPXPATH@/$(UPXPATH)/g; s/@DISTDIR@/$(DISTDIR)/g;' setup.nsi.in > tmp && mv tmp setup.nsi

test:
	$(PYTHON) -m pytest pyepbd
	$(PYTHON) bin/epbdcalc.py pyepbd/examples/ejemplo6K3.csv
	$(PYTHON) bin/epbdcalc.py pyepbd/examples/ejemplo3PVBdC.csv

coverage:
	$(PYTHON) -m pytest --cov --cov-report=html pyepbd

#https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#packaging-your-project
.PHONY:dist
dist:
	rm -f dist/*.whl dist/*.tar.gz
	$(PYTHON) setup.py bdist_wheel
	$(PYTHON) setup.py sdist
	twine upload dist/*

clean:
	rm -rf build dist MANIFEST setup.nsi README.html Manual_epbdcalc.pdf
	find . -name *.pyc -exec rm {} \;
	find . -name *.swp -exec rm {} \;

# Los phony son los que no dependen de archivos y hay que considerar siempre no actualizados (rebuild)
.PHONY: setup.nsi winbuild clean test dist
