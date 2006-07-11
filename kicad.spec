Name: 		kicad
Version:	2006.06.26
Release:	5%{?dist}
Summary: 	Electronic schematic diagrams and printed circuit board artwork
Summary(fr): 	Saisie de schéma électronique et tracé de cicrcuit imprimé

Group: 		Applications/Engineering
License: 	GPL
Url: 		http://www.lis.inpg.fr/realise_au_lis/kicad/
Source:		ftp://iut-tice.ujf-grenoble.fr/cao/sources/kicad-sources-2006-06-26.zip
Source1:	http://linuxelectronique.free.fr/download/kicad-src-extras-2006-06-26.tar.bz2
Source2:	%{name}.desktop
Patch:		%{name}-%{version}.destdir.diff
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	wxGTK
BuildRequires:	desktop-file-utils, wxGTK-devel

%description
Kicad is an open source (GPL) software for the creation of electronic schematic
diagrams and printed circuit board artwork up to 16 layers.
Kicad is a set of four softwares and a project manager:
- Eeschema: schematic entry
- Pcbnew: board editor
- Gerbview: GERBER viewer (photoplotter documents)
- Cvpcb: footprint selector for components used in the circuit design
- Kicad: project manager

%description -l fr
Kicad est un logiciel open source (GPL) pour la création de schémas
électroniques et le tracé de circuits imprimés jusqu'à 16 couches.
Kicad est un ensemble de quatres logiciels et un gestionnaire de projet :
- Eeschema : saisie de schémas
- Pcbnew : éditeur de circuits imprimés
- Gerbview : visualisateur GERBER (documents pour phototraçage)
- Cvpcb : sélecteur d'empreintes pour les composants utilisés dans le circuit
- Kicad : gestionnaire de projet.

%prep
%setup -q -n kicad-dev -a 1
%{__cp} -a kicad-src-extras/* .
%{__rm} -rf kicad-src-extras

# Convert MSDOS EOL to Unix EOL before applying patches

for f in 3d-viewer/{3d_struct.h,3d_viewer.h} \
eeschema/libcmp.h \
include/{pcbstruct.h,wxstruct.h} \
kicad/kicad.h \
pcbnew/{autorout.h,class_cotation.h,class_equipot.h,class_mire.h,class_module.h,class_pcb_text.h,class_text_mod.h,class_track.h,track.cpp}
do
  %{__sed} -i -e 's/\r$//' $f
done

%patch0 -p1

%build

# These files are not scripts
for f in {copyright,gpl,licendoc,readme,version}.txt
do
  %{__chmod} -x $f
done

# Convert MSDOS EOL to Unix EOL
for f in {author,contrib,copyright,doc_conv_orcad*,gpl,licendoc,readme}.txt
do
  %{__sed} -i -e 's/\r$//' $f
done

for f in help/fr/{contents.hhc,kicad.hhp,cvpcb/cvpcb.pdf,cvpcb/cvpcb-fr.html,eeschema/eeschema.html,eeschema/eeschema.pdf,file_formats/file_formats.html,gerbview/gerbview.html,kicad/kicad.html,pcbnew/pcbnew.html}
do
  %{__sed} -i -e 's/\r$//' $f
done

for f in help/en/{contents.hhc,kicad.hhp,cvpcb/cvpcb-en.html,eeschema/eeschema.html,file_formats/file_formats.html,gerbview/gerbview.html,kicad/kicad.html,pcbnew/pcbnew.html}
do
  %{__sed} -i -e 's/\r$//' $f
done

for f in help/es/{contents.hhc,kicad.hhp,cvpcb/cvpcb-es.html,eeschema/eeschema-es.html,file_formats/file_formats-es.html,gerbview/gerbview.html,kicad/kicad-es.html,pcbnew/pcbnew-es.html}
do
  %{__sed} -i -e 's/\r$//' $f
done

for f in help/pt/{contents.hhc,kicad.hhp,cvpcb/cvpcb-pt.html,eeschema/eeschema-pt.html,file_formats/file_formats.html,gerbview/gerbview.html,kicad/kicad-pt.html,kicad/kicad_pt_BR.html,pcbnew/pcbnew.html}
do
  %{__sed} -i -e 's/\r$//' $f
done

for f in help/ru/{contents.hhc,kicad.hhp,eeschema/eeschema_ru.html}
do
  %{__sed} -i -e 's/\r$//' $f
done

make -f makefile.gtk %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

# install demos files
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/demos
for dir in electric interf_u microwave pic_programmer pspice sonde_xilinx test_xil_95108 video
do
  install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/demos/${dir}
  for f in demos/${dir}/*
  do
    install -m 644 ${f} $RPM_BUILD_ROOT%{_datadir}/%{name}/${f}
  done
done

# install help files
install -d $RPM_BUILD_ROOT%%{_docdir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/
for dir in en es fr pt
do
  install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}
  for subdir in cvpcb eeschema file_formats gerbview kicad pcbnew
  do
    install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/${subdir}
    cd help
    install -m 644 ${dir}/kicad.hhp $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/kicad.hhp
    install -m 644 ${dir}/contents.hhc $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/contents.hhc
    for f in ${dir}/${subdir}/*
    do
      install -m 644 ${f} $RPM_BUILD_ROOT%{_docdir}/%{name}/${f}
    done
    cd ..
  done
done

# install ru help files
install -d $RPM_BUILD_ROOT%%{_docdir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/
for dir in ru
do
  install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}
  for subdir in eeschema pcbnew
  do
    install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/${subdir}
    cd help
    install -m 644 ${dir}/kicad.hhp $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/kicad.hhp
    install -m 644 ${dir}/contents.hhc $RPM_BUILD_ROOT%{_docdir}/%{name}/${dir}/contents.hhc
    for f in ${dir}/${subdir}/*
    do
      install -m 644 ${f} $RPM_BUILD_ROOT%{_docdir}/%{name}/${f}
    done
    cd ..
  done
done

# install librairies
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/library
for f in library/*
do
  install -m 644 ${f} $RPM_BUILD_ROOT%{_datadir}/%{name}/${f}
done

# install localization
install -d $RPM_BUILD_ROOT%{_datadir}/locale
cd locale
for dir in es fr hu it ko pl pt sl
do
  install -d $RPM_BUILD_ROOT%{_datadir}/locale/${dir}
  install -m 644 ${dir}/%{name}.mo $RPM_BUILD_ROOT%{_datadir}/locale/${dir}/%{name}.mo
done
cd ..

# install modules
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/modules/packages3d
for dir in conn_DBxx connectors conn_europe device dil discret divers pga pin_array smd support
do
  install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/modules/packages3d/${dir}
  for f in modules/packages3d/${dir}/*
  do
    install -m 644 ${f} $RPM_BUILD_ROOT%{_datadir}/%{name}/${f}
  done
done

# install template
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/template
install -m 644 template/%{name}.pro $RPM_BUILD_ROOT%{_datadir}/%{name}/template

# install binaries
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins
make -f makefile.gtk install DESTDIR=$RPM_BUILD_ROOT

# install desktop
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category "Engineering" \
  --add-category "Electronics" \
  --add-category "X-Fedora" \
  %{SOURCE2}

# install icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 644 kicad_icon.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/kicad_icon.png

%find_lang %{name}

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]
then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]
then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc author.txt contrib.txt copyright.txt doc_conv_orcad_to_kicad_spanish.txt
%doc doc_conv_orcad_to_kicad.txt gpl.txt licendoc.txt lisezmoi.txt news.txt
%doc readme.txt version.txt
%{_bindir}/*
%{_libdir}/%{name}/
%{_libdir}/%{name}/plugins/
%{_datadir}/%{name}/
%{_docdir}/%{name}/
%{_datadir}/applications/*
%{_datadir}/pixmaps/kicad_icon.png

%changelog
* Mon Jul 10 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-5
  - Removing backup files is no more needed.

* Mon Jul 10 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-4
  - Remove BR libGLU-devel that is no more needed (bug #197501 is closed)
  - Fix files permissions.

* Mon Jul  3 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-3
  - s/mesa-libGLU-devel/libGLU-devel/

* Mon Jul  3 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-2
  - BR mesa-libGLU-devel

* Wed Jun 28 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-1
  - New upstream version

* Tue Jun 13 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.04.24-5
  - Change name
  - Use %%{_docdir} instead of %%{_datadir}/doc
  - Use %%find_lang
  - Update desktop database
  - Convert MSDOS EOL to Unix EOL
  - Remove BR utrac

* Mon Jun 12 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-4
  - Patch to suppress extra qualification compile time error on FC5
  - BR utrac to convert MSDOS files before applying patch
    This will be remove for the next upstream version.

* Tue May 23 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-3
  - Install help in /usr/share/doc/kicad/ as the path is hardcoded
    in gestfich.cpp
  - Add desktop file

* Mon May 22 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-2
  - Add a second tarball that contains many things that are not included in
    the upstream source tarball such components and footprints librairies,
    help, localisation, etc.

* Sun May 21 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-1
  - Initial Fedora RPM
