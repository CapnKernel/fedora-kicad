TIMESTAMP:=2014.03.13
MAIN_REV:=d00fae58
LIB_REV:=742f6843
DOC_REV:=80fc0ae7

XZ:=$(shell type -p pxz || type -p xz)

# repos: kicad-source-mirror/README.txt kicad-library/README.md kicad-doc/CMakeLists.txt kicad-walter-libraries/robots.txt
repos: kicad-source-mirror/README.txt kicad-library/README.md kicad-doc/CMakeLists.txt

kicad-source-mirror/README.txt:
	git clone https://github.com/KiCad/kicad-source-mirror.git

kicad-library/README.md:
	git clone https://github.com/KiCad/kicad-library.git

kicad-doc/CMakeLists.txt:
	git clone https://github.com/blairbonnett-mirrors/kicad-doc

# kicad-walter-libraries/robots.txt:
# mkdir -p kicad-walter
# cd kicad-walter
# wget -r -l 1 -A zip http://smisioto.no-ip.org/elettronica/kicad/kicad-en.htm
# cd smisioto.no-ip.org/kicad_libs/library
# for i in *.zip ; do
#   unzip -o $i
#   rm -f $i
# done
# mv -f power.dcm w_power.dcm
# mv -f power.lib w_power.lib
# mv -f license.txt w_license.txt
# cd ../modules
# mv -f ../packages3d/* ./
# for i in *.zip ; do
#   unzip -o $i
#   rm -f $i
# done
# mv -f license.txt w_license.txt
# cd ..
# rmdir packages3d
# cd ..
# mv -f kicad_libs kicad-walter-libraries-$(TIMESTAMP)

update: kicad-source-mirror/README.txt kicad-library/README.md kicad-doc/CMakeLists.txt
	git -C kicad-source-mirror pull
	git -C kicad-library pull
	git -C kicad-library pull

# tars: kicad-$(TIMESTAMP).tar.xz kicad-libraries-$(TIMESTAMP).tar.xz kicad-doc-$(TIMESTAMP).tar.xz kicad-walter-libraries-$(TIMESTAMP).tar.xz
tars: kicad-$(TIMESTAMP).tar.xz kicad-libraries-$(TIMESTAMP).tar.xz kicad-doc-$(TIMESTAMP).tar.xz

kicad-$(TIMESTAMP).tar.xz: kicad-source-mirror/README.txt
	(cd kicad-source-mirror && git archive --format=tar $(MAIN_REV)) | $(XZ) > $@

kicad-libraries-$(TIMESTAMP).tar.xz: kicad-library/README.md
	(cd kicad-library && git archive --format=tar $(LIB_REV)) | $(XZ) > $@

kicad-doc-$(TIMESTAMP).tar.xz: kicad-doc/CMakeLists.txt
	(cd kicad-doc && git archive --format=tar $(DOC_REV)) | $(XZ) > $@

kicad-walter-libraries-$(TIMESTAMP).tar.xz: kicad-walter-libraries/robots.txt
	(cd kicad-walter-libraries && git archive --format=tar $(DOC_REV)) | $(XZ) > $@

clean:
	-rm -f kicad-$(TIMESTAMP).tar.xz kicad-libraries-$(TIMESTAMP).tar.xz kicad-doc-$(TIMESTAMP).tar.xz kicad-walter-libraries-$(TIMESTAMP).tar.xz
	-rm -rf kicad-source-mirror kicad-library kicad-doc kicad-walter-libraries
