# Fetching a new version:
#
#  - Update TIMESTAMP to be today's date
#
#  - Go to https://github.com/KiCad/kicad-source-mirror
#    Look for "latest commit" hash
#    Copy the hash to MAIN_REV
#
#  - Go to https://github.com/KiCad/kicad-library
#    Look for "latest commit" hash
#    Copy the hash to LIB_REV
#
#  - Go to https://github.com/blairbonnett-mirrors/kicad-doc
#    Look for "latest commit" hash
#    Copy the hash to DOC_REV

# TIMESTAMP:=2014.03.13
# MAIN_REV:=d00fae58
# LIB_REV:=742f6843
# DOC_REV:=80fc0ae7

# TIMESTAMP:=2014.07.20
# MAIN_REV:=2196ed21
# LIB_REV:=44688196
# DOC_REV:=12c2a3b1

TIMESTAMP:=2014.11.15
MAIN_REV:=9245b90
LIB_REV:=2c93827
DOC_REV:=b544666

# Use parallel xz if it's available, otherwise fall back to xz
# (installing the pxz package will make compression much faster
# on a multicore machine)
XZ:=$(shell type -p pxz || type -p xz)

repos: kicad-source-mirror/README.txt kicad-library/README.md kicad-doc/CMakeLists.txt kicad-walter-libraries/robots.txt

kicad-source-mirror/README.txt:
	git clone https://github.com/KiCad/kicad-source-mirror.git

kicad-library/README.md:
	git clone https://github.com/KiCad/kicad-library.git

kicad-doc/CMakeLists.txt:
	git clone https://github.com/blairbonnett-mirrors/kicad-doc

kicad-walter-libraries/robots.txt:
	mkdir -p kicad-walter-libraries
	wget --recursive --timestamping --level=1 --cut-dirs=1 --accept=zip --no-host-directories --directory-prefix=kicad-walter-libraries --no-verbose http://smisioto.no-ip.org/elettronica/kicad/kicad-en.htm

update: kicad-source-mirror/README.txt kicad-library/README.md kicad-doc/CMakeLists.txt
	git -C kicad-source-mirror pull
	git -C kicad-library pull
	git -C kicad-doc pull
	wget --recursive --timestamping --level=1 --cut-dirs=1 --accept=zip --no-host-directories --directory-prefix=kicad-walter-libraries --no-verbose http://smisioto.no-ip.org/elettronica/kicad/kicad-en.htm

tars: kicad-$(TIMESTAMP).tar.xz kicad-libraries-$(TIMESTAMP).tar.xz kicad-doc-$(TIMESTAMP).tar.xz kicad-walter-libraries-$(TIMESTAMP).tar.xz

kicad-$(TIMESTAMP).tar.xz: kicad-source-mirror/README.txt
	(cd kicad-source-mirror && git archive --prefix=kicad-$(TIMESTAMP)/ --format=tar $(MAIN_REV)) | $(XZ) > $@

kicad-libraries-$(TIMESTAMP).tar.xz: kicad-library/README.md
	(cd kicad-library && git archive --prefix=kicad-libraries-$(TIMESTAMP)/ --format=tar $(LIB_REV)) | $(XZ) > $@

kicad-doc-$(TIMESTAMP).tar.xz: kicad-doc/CMakeLists.txt
	(cd kicad-doc && git archive --prefix=kicad-doc-$(TIMESTAMP)/ --format=tar $(DOC_REV)) | $(XZ) > $@

# kicad-walter-libraries is the .zip files we downloaded from Walter's website.
# kicad-walter-libraries-$(TIMESTAMP) is the unzipped files that act as the source for the tar.
kicad-walter-libraries-$(TIMESTAMP).tar.xz: kicad-walter-libraries/robots.txt
	rm -rf kicad-walter-libraries-$(TIMESTAMP)
	for i in `find kicad-walter-libraries -name '*.zip'`; do d=`dirname $$i | sed -e 's:\(kicad-walter-libraries\):\1-$(TIMESTAMP):' -e 's:/packages3d:/modules:'`; mkdir -p "$$d"; unzip -o -d "$$d" "$$i"; done
	for i in `find kicad-walter-libraries-$(TIMESTAMP) -name license.txt`; do mv -i "$$i" "$${i/license/w_license}"; done
	(cd kicad-walter-libraries-$(TIMESTAMP)/library; for i in power.*; do mv $$i w_$$i; done)
	tar -cf - kicad-walter-libraries-$(TIMESTAMP) | $(XZ) > $@

clean:
	-rm -f kicad-$(TIMESTAMP).tar.xz kicad-libraries-$(TIMESTAMP).tar.xz kicad-doc-$(TIMESTAMP).tar.xz kicad-walter-libraries-$(TIMESTAMP).tar.xz
	-rm -rf kicad-source-mirror kicad-library kicad-doc kicad-walter-libraries kicad-walter-libraries-$(TIMESTAMP)
