
# icons root directory
%global iconsdir %{_datadir}/icons

Name:      unison-sync
Version:   2.52.1
Release:   1%{?dist}

Summary:   Multi-master File synchronization tool

License:   GPLv3+
URL:       http://www.cis.upenn.edu/~bcpierce/unison
Source0:   https://github.com/bcpierce00/unison/archive/v%{version}.tar.gz
Source1:   http://www.cis.upenn.edu/~bcpierce/unison/download/releases/unison-%{version}/unison-manual.html
Source2:   unison.appdata.xml

# can't make this noarch (rpmbuild fails about unpackaged debug files)
# BuildArch:     noarch
ExcludeArch:   sparc64 s390 s390x

BuildRequires: ctags
BuildRequires: libappstream-glib
BuildRequires: ocaml

Requires:   %{name}-ui = %{version}-%{release}

Requires(posttrans): %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/alternatives

%description
Unison is a multi-master file-synchronization tool. It allows two
replicas of a collection of files and directories to be stored on
different hosts (or different locations on the same host), modified
separately, and then brought up to date by propagating the changes
in each replica to the other.

%package gtk

Summary:   Multi-master File synchronization tool - gtk interface

BuildRequires: ocaml-lablgtk-devel
BuildRequires: gtk2-devel
BuildRequires: desktop-file-utils

Requires: %name = %{version}-%{release}

Provides:   %{name}-ui = %{version}-%{release}

%description gtk
This package provides the graphical version of unison with gtk2 interface.


%package text

Summary:   Multi-master File synchronization tool - text interface

Requires: %name = %{version}-%{release}

Provides:   %{name}-ui = %{version}-%{release}

%description text
This package provides the textual version of unison without graphical interface.


%prep
%setup -q -n unison-%{version}

cat > %{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=unison-gtk
Name=Unison File Synchronizer (version %{version})
GenericName=File Synchronizer
Comment=Multi-master File synchronization tool
Terminal=false
Icon=%{name}
StartupNotify=true
Categories=Utility;
EOF

#additional documentation
cp -a %{SOURCE1} .


%build
# MAKEFLAGS=-j<N> breaks the build.
unset MAKEFLAGS

# we compile 2 versions: gtk2 ui and text ui
make NATIVE=true UISTYLE=gtk2 THREADS=true
mv src/unison src/unison-gtk

make NATIVE=true UISTYLE=text THREADS=true
mv src/unison src/unison-text


%install
mkdir -p %{buildroot}%{_bindir}

cp -a src/unison-gtk %{buildroot}%{_bindir}/unison-gtk
cp -a src/unison-text %{buildroot}%{_bindir}/unison-text
cp -a src/unison-fsmonitor %{buildroot}%{_bindir}/unison-fsmonitor

# Install the various icons according to the "Icon Theme Specification"
# https://specifications.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html
for size in 16 24 32 48 256; do
    format="${size}x${size}"
    install -d %{buildroot}%{iconsdir}/hicolor/${format}/apps
    install icons/U.${format}x16m.png \
            %{buildroot}%{iconsdir}/hicolor/${format}/apps/%{name}.png
done

install -d %{buildroot}%{iconsdir}/hicolor/scalable/apps
install icons/U.svg \
        %{buildroot}%{iconsdir}/hicolor/scalable/apps/%{name}.svg

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/metainfo
cp %{SOURCE2} %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%post gtk
# https://fedoraproject.org/wiki/EPEL:Packaging#Icon_Cache
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans gtk
# https://fedoraproject.org/wiki/EPEL:Packaging#Icon_Cache
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
# https://fedoraproject.org/wiki/EPEL:Packaging#Icon_Cache
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%files
%doc README.md NEWS.md src/README unison-manual.html
%license src/COPYING
%{_bindir}/unison-fsmonitor


%files gtk
%{_bindir}/unison-gtk
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{iconsdir}/*


%files text
%{_bindir}/unison-text


%changelog
* Mon May 30 2022 Håkon Løvdal <kode@denkule.no> - 2.52.1-1
- Update to version 2.52.1.
- Rename package and drop all the mess with embedding version number into
  package name (this should no longer be important after version 2.52.0 which
  finally uses a compiler independent marshalling format).

* Fri Jan 25 2019 Christian Affolter <c.affolter@purplehaze.ch> - 2.51.2-2
- Include unison-fsmonitor (the Unison filesystem monitor)

* Tue Jan 15 2019 Christian Affolter <c.affolter@purplehaze.ch - 2.51.2-1
- Update to latest stable upstream release
- Change upstream download source URL to GitHub
- Install icons from upstream tarball in different sizes and formats

* Mon Feb 12 2018 David Personette <dperson@gmail.com> - 2.48.15v4-2
- Apply suggested changes from bug #1544239

* Sat Feb 10 2018 David Personette <dperson@gmail.com> - 2.48.15v4-1
- Update to latest stable upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.128-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.128-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40.128-7
- Small fix for compiling against OCaml 4.04 (RHBZ#1392152).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.128-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 2.40.128-5
- Rebuild for OCaml 4.04.0.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.128-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 2.40.128-3
- Use global instead of define.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Richard W.M. Jones <rjones@redhat.com> - 2.40.128-1
- New upstream version 2.40.128 (RHBZ#1178444).
- Remove missing documentation patch, now included upstream.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.102-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.102-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 2.40.102-6
- own alternatives target

* Mon Sep 09 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.102-5
- ship 2 versions of unison: text only and gtk2 user interface
- move binaries into subpackages
- enable dependency generator

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Richard W.M. Jones <rjones@redhat.com> - 2.40.102-2
- Rebuild for OCaml 4.00.1.

* Thu Nov 15 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.102-1
- 2.40.102
- fixes incompatibility between unison ocaml3 and ocaml4 builds

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Gregor Tätzner <brummbq@fedoraproject.com> - 2.40.63-6
- Patch built-in documentation.

* Sat Jan 21 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-5
- Add unison-manual.html.

* Fri Jan 13 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-4
- Remove ocaml minimum version.
- Add Requires and provides scripts.

* Tue Sep 27 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-3
- Remove vendor tag.

* Sun Sep 04 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-2
- Remove xorg-x11-font-utils Requirement.
- Enable THREADS=true.

* Tue Aug 30 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-1
- Version bump.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.57-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.57-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 8 2009 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-11
- Add Requires: xorg-x11-fonts-misc

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.27.57-10
- Rebuild for OCaml 3.11.0+rc1.

* Sat May 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.27.57-9
- Rebuild with OCaml 3.10.2-2 (fixes bz 441685, 445545).

* Sun Mar 30 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-8
- Don't use alternatives for desktop and icon files, to avoid duplicate
  menu entries.

* Wed Mar 19 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-7
- Fix license to match correct interpretation of source & GPL
- Remove Excludes for ppc64, since ocaml is available there now, in devel

* Sat Mar 15 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-6
- Rename package unison2.27 -> unison227 to match Fedora naming rules
- Automatically calculate ver_priority using the shell; easier maintenance

* Sat Mar 1 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-5
- Use Provides/Obsoletes to provide upgrade path, per:
  http://fedoraproject.org/wiki/Packaging/NamingGuidelines

* Thu Feb 28 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-4
- Explicitly conflict with existing unison package

* Fri Feb 22 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-3
- Derived unison2.27 package from unison2.13 package

* Mon Feb  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.27.57-2
- exclude arch ppc64

* Mon Feb  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.27.57-1
- new release 2.27.57

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-3
- Rebuild for FE6

* Tue Feb 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-2
- Rebuild for Fedora Extras 5

* Thu Sep  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-1
- New Version 2.13.16

* Sun Jul 31 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.12.0-0
- New Version 2.12.0

* Fri May 27 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.10.2-7
- Bump and rebuild with new ocaml and new lablgtk

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.10.2-6
- rebuild on all arches

* Mon May 16 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.10.2-5
- Patch: http://groups.yahoo.com/group/unison-users/message/3200

* Thu Apr 7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.10.2-2
- BR gtk2-devel
- Added NEWS and README docs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.10.2-1
- New Version 2.10.2

* Wed Apr 28 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.74-0.fdr.1
- New Version 2.9.74
- Added icon

* Tue Jan 13 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.72-0.fdr.1
- New Version 2.9.72

* Tue Dec  9 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.70-0.fdr.2
- Changed Summary
- Added .desktop file

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.70-0.fdr.1
- First Fedora release
