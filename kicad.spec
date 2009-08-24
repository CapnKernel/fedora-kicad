Name:           kicad
Version:        2009.07.07
Release:        4.rev1863%{?dist}
Summary:        Electronic schematic diagrams and printed circuit board artwork
Summary(fr):    Saisie de schéma électronique et tracé de circuit imprimé

Group:          Applications/Engineering
License:        GPLv2+
URL:            http://www.lis.inpg.fr/realise_au_lis/kicad/

# Source files created from upstream's SVN repository
Source:         kicad-%{version}.tar.bz2
Source1:        kicad-doc-%{version}.tar.bz2
Source2:        kicad-library-%{version}.tar.bz2
Source3:	kicad-ld.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  wxGTK-devel
BuildRequires:  boost-devel
BuildRequires:  cmake

Requires:       electronics-menu

%description
Kicad is an EDA software to design electronic schematic
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


%package        doc
Summary:        Documentations for kicad
Group:          Applications/Engineering
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif


%description    doc
Documentations and tutorials for kicad in English


%package        doc-de
Summary:        Documentation for Kicad in German
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-de
Documentation and tutorials for Kicad in German


%package        doc-es
Summary:        Documentation for Kicad in Spanish
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-es
Documentation and tutorials for Kicad in Spanish


%package        doc-fr
Summary:        Documentation for Kicad in French
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-fr
Documentation and tutorials for Kicad in French


%package        doc-hu
Summary:        Documentation for Kicad in Hungarian
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-hu
Documentation and tutorials for Kicad in Hungarian


%package        doc-it
Summary:        Documentation for Kicad in Italian
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-it
Documentation and tutorials for Kicad in Italian


%package        doc-pt
Summary:        Documentation for Kicad in Portuguese
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-pt
Documentation and tutorials for Kicad in Portuguese


%package        doc-ru
Summary:        Documentation for Kicad in Russian
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-ru
Documentation and tutorials for Kicad in Russian


%package        doc-zh_CN
Summary:        Documentation for Kicad in Chinese
Group:          Documentation
Requires:       %{name}-doc = %{version}-%{release}
%if 0%{?fedora} >= 11
BuildArch:      noarch
%endif

%description    doc-zh_CN
Documentation and tutorials for Kicad in Chinese


%prep
%setup -q -a 1 -a 2

#kicad-doc.noarch: W: file-not-utf8 /usr/share/doc/kicad/AUTHORS.txt
iconv -f iso8859-1 -t utf-8 AUTHORS.txt > AUTHORS.conv && mv -f AUTHORS.conv AUTHORS.txt


#multilibs
%ifarch x86_64 sparc64 ppc64 amd64
%{__sed} -i "s|KICAD_PLUGINS lib/kicad/plugins|KICAD_PLUGINS lib64/kicad/plugins|" CMakeLists.txt
%{__sed} -i "s|/usr/lib/kicad|/usr/lib64/kicad|" %{SOURCE3}
%endif


%build

#
# Symbols libraries
#
pushd %{name}-library-%{version}/
%cmake -DCMAKE_BUILD_TYPE=Release .
%{__make} %{?_smp_mflags} VERBOSE=1
popd


#
# Core components
#
%cmake -DCMAKE_BUILD_TYPE=Release
%{__make} %{?_smp_mflags} VERBOSE=1


%install
%{__rm} -rf %{buildroot}

%{__make} INSTALL="install -p" DESTDIR=%{buildroot} install


# install localization
%{__rm} -rf %{buildroot}%{_datadir}/%{name}/internat/
install -d %{buildroot}%{_datadir}/locale
cd internat
for dir in ca cs de es fr hu it ko nl pl pt ru sl sv zh_CN
do
  install -d %{buildroot}%{_datadir}/locale/${dir}
  install -m 644 ${dir}/%{name}.mo %{buildroot}%{_datadir}/locale/${dir}/%{name}.mo
done
cd ..


# install desktop
desktop-file-install --vendor=fedora         \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-category Development		     \
  --delete-original                          \
  %{buildroot}%{_datadir}/applications/kicad.desktop
rm -f %{buildroot}%{_datadir}/applications/eeschema.desktop

# Missing requires libraries
%{__cp} -p ./3d-viewer/lib3d-viewer.so %{buildroot}%{_libdir}/%{name}
%{__cp} -p ./bitmaps/libbitmaps.so %{buildroot}%{_libdir}/%{name}
%{__cp} -p ./common/libcommon.so %{buildroot}%{_libdir}/%{name}
%{__cp} -p ./polygon/kbool/src/libkbool.so %{buildroot}%{_libdir}/%{name}
%{__cp} -p ./common/libpcbcommon.so %{buildroot}%{_libdir}/%{name}
%{__cp} -p ./polygon/libpolygon.so %{buildroot}%{_libdir}/%{name}

#
# Symbols libraries
#
pushd %{name}-library-%{version}/
%{__make} INSTALL="install -p" DESTDIR=%{buildroot} install
popd

# install ld.conf
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/ld.so.conf.d/kicad.conf

# install template
install -d %{buildroot}%{_datadir}/%{name}/template
install -m 644 template/%{name}.pro %{buildroot}%{_datadir}/%{name}/template


# Preparing for documentation pull-ups
%{__rm} -f  %{name}-doc-%{version}/doc/help/CMakeLists.txt
%{__rm} -f  %{name}-doc-%{version}/doc/help/makefile
%{__rm} -f  %{name}-doc-%{version}/doc/tutorials/CMakeLists.txt

%{__cp} -pr %{name}-doc-%{version}/doc/* %{buildroot}%{_docdir}/%{name}
%{__cp} -pr AUTHORS.txt CHANGELOG* TODO.txt version.txt %{buildroot}%{_docdir}/%{name}


%find_lang %{name}


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]
then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

/sbin/ldconfig

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]
then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc %{_docdir}/%{name}/help/en/kicad.pdf
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/icons/hicolor/*/mimetypes/application-x-kicad-project.*
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/application/x-%{name}-*.desktop
%{_sysconfdir}/ld.so.conf.d/kicad.conf

%files doc
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/help/
%dir %{_docdir}/%{name}/tutorials
%doc %{_docdir}/%{name}/*.txt
%doc %{_docdir}/%{name}/scripts
%doc %{_docdir}/%{name}/contrib
%doc %{_docdir}/%{name}/help/en/docs_src/
%doc %{_docdir}/%{name}/help/en/cvpcb.pdf
%doc %{_docdir}/%{name}/help/en/eeschema.pdf
%doc %{_docdir}/%{name}/help/en/gerbview.pdf
%doc %{_docdir}/%{name}/help/en/pcbnew.pdf
%doc %{_docdir}/%{name}/help/file_formats
%doc %{_docdir}/%{name}/tutorials/en

%files doc-de
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/de
%doc %{_docdir}/%{name}/tutorials/de

%files doc-es
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/es
%doc %{_docdir}/%{name}/tutorials/es

%files doc-fr
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/fr
%doc %{_docdir}/%{name}/tutorials/fr

%files doc-hu
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/tutorials/hu

%files doc-it
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/it

%files doc-pt
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/pt


%files doc-ru
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/help/ru
%doc %{_docdir}/%{name}/tutorials/ru

%files doc-zh_CN
%defattr(-,root,root,-)
#%doc %{_docdir}/%{name}/help/zh_CN
%doc %{_docdir}/%{name}/tutorials/zh_CN


%changelog
* Mon Aug 24 2009 Jon Ciesla <limb@jcomserv.net> - 2009.07.07-4.rev1863
- Multilib path correction, BZ 518916.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.07.07-3.rev1863
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Jon Ciesla <limb@jcomserv.net> - 2009.07.07-2.rev1863
- Dropped eeschema desktop file.
- Moved English kicad.pdf to main rpm.
- Added ls.so.conf file and ldconfig to post, postun to fix libs issue.
- Dropped category Development from desktop file.

* Tue Jul 7 2009 Chitlesh Goorah <chitlesh [AT] fedoraproject DOT org> - 2009.07.07-1.rev1863
- svn rev 1863
- documentation splitted into multiple packages
- libraries are now taken directly from SVN rather than from older releases
- build changed to cmake based

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.07.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2007.07.09-4
- First patch is Patch0 - should fix build in Rawhide.
- Include %%_libdir/kicad directory.
- Drop explicit Requires wxGTK in favour of automatic SONAME dependencies.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2007.07.09-3
- Autorebuild for GCC 4.3

* Mon Oct 15 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.07.09-2
  - Update desktop file

* Thu Oct 04 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.07.09-1
  - New upstream version
  - Merge previous patches
  - Remove X-Fedora, Electronics and Engineering categories
  - Update desktop file

* Mon Aug 27 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-4
  - License tag clarification

* Thu Aug 23 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-3
  - Rebuild

* Wed Feb 14 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-2
  - Fix desktop entry. Fix #228598

* Thu Feb  8 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-1
  - New upstream version

* Thu Feb  8 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.08.28-4
  - Add patch to build with RPM_OPT_FLAGS and remove -s from LDFLAGS
    Contribution of Ville Skyttä <ville[DOT]skytta[AT]iki[DOT]fi>
    Fix #227757
  - Fix typo in french summary

* Thu Dec 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> 2006.08.28-3
  - Rebuild with wxGTK 2.8.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2006.08.28-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.08.28-1
  - New upstream version
  - Use macro style instead of variable style
  - Install missing modules. Fix #206602

* Fri Sep  1 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-6
  - FE6 rebuild

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
