%define build_subpixel 0
%define build_plf 0
%{?_with_plf: %global build_plf 1}
%{?_with_subpixel: %global build_subpixel 1}

%define release 2
%if %build_plf
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
#%define extrarelsuffix plf
%define build_subpixel 1
%endif

%define major	6
%define libname	%mklibname freetype %{major}
%define develname %mklibname -d freetype %{major}

%define git_url git://git.sv.gnu.org/freetype/freetype2.git

Summary:	A free and portable TrueType font rendering engine
Name:		freetype
Version:	2.4.11
Release:	%{release}%{?extrarelsuffix}
License:	FreeType License/GPL
Group:		System/Libraries
URL:		http://www.freetype.org/
Source0:	http://mirror3.layerjet.com/nongnu/freetype/freetype-%version.tar.gz
Source1:	http://mirror3.layerjet.com/nongnu/freetype/freetype-%version.tar.gz.sig
Source2:	http://mirror3.layerjet.com/nongnu/freetype/freetype-doc-%version.tar.gz
Source3:	http://mirror3.layerjet.com/nongnu/freetype/freetype-doc-%version.tar.gz.sig
Source4:	http://mirror3.layerjet.com/nongnu/freetype/ft2demos-%version.tar.gz
Source5:	http://mirror3.layerjet.com/nongnu/freetype/ft2demos-%version.tar.gz.sig
Patch0:		ft2demos-2.3.12-mathlib.diff
Patch1:		freetype-2.4.2-CVE-2010-3311.patch
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig
BuildRequires:	libx11-devel
Provides:	freetype2 = %EVRD
Obsoletes:	freetype2 < %EVRD

%description
The FreeType2 engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType2 is a library, not a
stand-alone application, though some utility applications are included
%if %{build_plf}

This package is in PLF because this build has subpixel hinting enabled which
is covered by software patents.
%endif

%package -n %{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included
%if %{build_plf}

This package is in PLF because this build has subpixel hinting enabled which
is covered by software patents.
%endif

%package -n %{develname}
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	zlib-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package is only needed if you intend to develop or compile applications
which rely on the FreeType2 library. If you simply want to run existing
applications, you won't need this package.

%package demos
Summary:	A collection of FreeType demos
Group:		File tools

%description demos
The FreeType engine is a free and portable font rendering engine, developed to
provide advanced font support for a variety of platforms and environments. The
demos package includes a set of useful small utilities showing various
capabilities of the FreeType library.

%prep
%setup -q -n freetype-%{version} -a2 -a4

pushd ft2demos-%{version}
%patch0 -p0
popd

%patch1 -p1 -b .CVE-2010-3311

%if %{build_subpixel}
perl -pi -e 's|^/\* #define FT_CONFIG_OPTION_SUBPIXEL_RENDERING \*/| #define FT_CONFIG_OPTION_SUBPIXEL_RENDERING|' include/freetype/config/ftoption.h
%endif

#./autogen.sh --help || :

%build
# some apps crash on ppc without this
%ifarch ppc
export CFLAGS="`echo %{optflags} |sed s/O2/O0/`"
%endif

%configure2_5x	\
		--disable-static

# (tpg) remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool

%make

pushd ft2demos-%{version}
# The purpose of overriding LINK_LIBRARY is getting rid of ****ing
# rpath
%make TOP_DIR=".." X11_LIB="" \
LINK_LIBRARY='$(LIBTOOL) --mode=link $(CCraw) -o $@ $(OBJECTS_LIST) \
                          -version-info $(version_info) \
                           $(LDFLAGS) -no-undefined \
                           # -export-symbols $(EXPORTS_LIST)'
popd

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/freetype-config

%multiarch_includes %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig.h

install -d %{buildroot}%{_bindir}

for ftdemo in ftbench ftdiff ftdump ftgamma ftgrid ftlint ftmulti ftstring ftvalid ftview; do
    builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo %{buildroot}%{_bindir}
done

# cleanup
rm -fr %{buildroot}%{_libdir}/*.{a,la}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc docs/*
%{_bindir}/freetype-config
%{_libdir}/*.so
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_includedir}/ft2build.h
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{multiarch_bindir}/freetype-config
%dir %{multiarch_includedir}/freetype2
%{multiarch_includedir}/freetype2/*

%files demos
%{_bindir}/ftbench
%{_bindir}/ftdiff
%{_bindir}/ftdump
%{_bindir}/ftgamma
%{_bindir}/ftgrid
%{_bindir}/ftlint
%{_bindir}/ftmulti
%{_bindir}/ftstring
%{_bindir}/ftvalid
%{_bindir}/ftview

%changelog
* Fri Jun 15 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.4.10-2mdv2012.0
+ Revision: 805763
- Update to 2.4.10

* Wed May 23 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.4.9-2
+ Revision: 800214
- rebuild to loose rpmlib dep

* Mon Mar 12 2012 Alexander Khrukin <akhrukin@mandriva.org> 2.4.9-1
+ Revision: 784357
- version update 2.4.9
- version update 2.4.9

* Sat Dec 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.8-2
+ Revision: 737459
- drop the static lib, its sub package and the libtool *.la file
- various fixes

* Wed Nov 16 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.8-1
+ Revision: 731028
- 2.4.8

* Thu Oct 20 2011 Andrey Bondrov <abondrov@mandriva.org> 2.4.7-1
+ Revision: 705513
- Security release 2.4.7

* Mon Aug 08 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.4.6-2
+ Revision: 693662
- fix release suffix

* Sat Aug 06 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.4.6-1
+ Revision: 693470
- new version
- drop patch 2

* Tue Jul 26 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.5-2
+ Revision: 691740
- sync with MDVSA-2011:120

* Thu Jun 30 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.4.5-1
+ Revision: 688320
- new version
- drop merged patch 2

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 2.4.4-4
+ Revision: 661898
- fix multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Fri Mar 04 2011 Ð�Ð»ÐµÐºÑ�Ð°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 2.4.4-3
+ Revision: 641823
+ rebuild (emptylog)

* Wed Mar 02 2011 Ð�Ð»ÐµÐºÑ�Ð°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 2.4.4-2
+ Revision: 641211
- add infinality subpixel multipatch for plf

  + Anssi Hannula <anssi@mandriva.org>
    - plf: append "plf" to Release on cooker to make plf build have higher EVR
      again with the rpm5-style mkrel now in use

* Sat Dec 04 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.4.4-1mdv2011.0
+ Revision: 609230
- new version
- drop patches 2,3

* Tue Nov 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-3mdv2011.0
+ Revision: 598016
- P2: security fix for CVE-2010-3814 (upstream)
- P3: security fix for CVE-2010-3855 (upstream)

* Wed Oct 13 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-2mdv2011.0
+ Revision: 585373
- P1: security fix for CVE-2010-3311

* Mon Oct 04 2010 Funda Wang <fwang@mandriva.org> 2.4.3-1mdv2011.0
+ Revision: 582790
- New version 2.4.3

* Fri Aug 06 2010 Funda Wang <fwang@mandriva.org> 2.4.2-1mdv2011.0
+ Revision: 567192
- new version 2.4.2

* Sun Jul 18 2010 Funda Wang <fwang@mandriva.org> 2.4.1-1mdv2011.0
+ Revision: 554830
- update to new version 2.4.1

* Fri Jul 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.0-2mdv2011.0
+ Revision: 554387
- fix deps (whoops!)
- added the ft2demos tools

  + Anssi Hannula <anssi@mandriva.org>
    - fix spelling in description

* Wed Jul 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.0-1mdv2011.0
+ Revision: 553311
- 2.4.0
- the bytecode interpreter is enabled because the patent expired in may

* Mon Feb 15 2010 Frederic Crozat <fcrozat@mandriva.com> 2.3.12-1mdv2010.1
+ Revision: 506123
- Release 2.3.12
- Fix url

* Sat Jan 02 2010 Funda Wang <fwang@mandriva.org> 2.3.11-2mdv2010.1
+ Revision: 484980
- libtoolize is not needed any more

* Mon Oct 12 2009 Frederic Crozat <fcrozat@mandriva.com> 2.3.11-1mdv2010.0
+ Revision: 456723
- Release 2.3.11

* Fri Oct 09 2009 Frederic Crozat <fcrozat@mandriva.com> 2.3.10-1mdv2010.0
+ Revision: 456395
- Release 2.3.10
- Remove patches 0, 1 (merged upstream)

  + Olivier Blin <blino@mandriva.org>
    - fix assembly declaration for armel (from Arnaud Patard)

* Thu Sep 24 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.9-4mdv2010.0
+ Revision: 448177
- added the corrected patch by pcpa for fixing CVE-2009-0946

* Wed Sep 23 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.9-3mdv2010.0
+ Revision: 447643
- P0: security fix for CVE-2009-0946

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.3.9-2mdv2010.0
+ Revision: 424480
- rebuild

  + Frederic Crozat <fcrozat@mandriva.com>
    - add git_url

* Thu Mar 12 2009 Frederic Crozat <fcrozat@mandriva.com> 2.3.9-1mdv2009.1
+ Revision: 354233
- Release 2.3.9

* Wed Jan 14 2009 Frederic Crozat <fcrozat@mandriva.com> 2.3.8-2mdv2009.1
+ Revision: 329473
- Release 2.3.8

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.7-2mdv2009.1
+ Revision: 318825
- rebuild

* Mon Jun 30 2008 Frederic Crozat <fcrozat@mandriva.com> 2.3.7-1mdv2009.0
+ Revision: 230204
- Release 2.3.7

* Tue Jun 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2.3.6-1mdv2009.0
+ Revision: 217357
- Release 2.3.6

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Frederic Crozat <fcrozat@mandriva.com> 2.3.5-2mdv2008.0
+ Revision: 89480
- Force rebuild

* Tue Jul 03 2007 Funda Wang <fwang@mandriva.org> 2.3.5-1mdv2008.0
+ Revision: 47335
- New version

  + Anssi Hannula <anssi@mandriva.org>
    - plf: update reason

* Fri Apr 27 2007 Frederic Crozat <fcrozat@mandriva.com> 2.3.4-1mdv2008.0
+ Revision: 18751
- Release 2.3.4
- Remove patch0, merged upstream
- add build options in package to enable individually subpixel hinting and bytecode interpreter

* Sat Apr 21 2007 Anssi Hannula <anssi@mandriva.org> 2.3.1-4mdv2008.0
+ Revision: 16552
- patch0: fix CVE-2007-1351


* Sun Feb 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.3.1-3mdv2007.0
+ Revision: 122328
- fix buildrequires

* Sun Feb 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.3.1-2mdv2007.1
+ Revision: 122284
- rebuild to fix pkgconfig deps

* Wed Jan 31 2007 Frederic Crozat <fcrozat@mandriva.com> 2.3.1-1mdv2007.1
+ Revision: 115653
- Release 2.3.1

* Wed Jan 17 2007 Frederic Crozat <fcrozat@mandriva.com> 2.3.0-1mdv2007.1
+ Revision: 109964
- Release 2.3.0
- Removes all patches, merged upstream

* Sat Dec 02 2006 Olivier Blin <oblin@mandriva.com> 2.2.1-9mdv2007.1
+ Revision: 89940
- fix overlapping segments (#23258)

* Sat Nov 11 2006 Anssi Hannula <anssi@mandriva.org> 2.2.1-8mdv2007.0
+ Revision: 81091
- plf: really enable full hinting

* Fri Nov 03 2006 Anssi Hannula <anssi@mandriva.org> 2.2.1-7mdv2007.1
+ Revision: 76248
- increase release
- plf: fix reason

  + Oden Eriksson <oeriksson@mandriva.com>
    - bzip2 cleanup
    - rebuild

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-5mdv2007.1
+ Revision: 63443
- bunzip patches
- Import freetype2

* Tue Sep 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-4mdv2007.0
- Patch6 (pterjan): fix crash (fdo bug #6841)

* Sat Jul 22 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-3mdv2007.0
- Patch0 (CVS): fix CVE-2006-3467
- Patch1 (CVS): handles correctly bdf fonts without POINT_SIZE property
- Patch2 (CVS): fix bytecode hint instructions
- Patch3 (CVS): fix handling of some strange PFR fonts
- Patch4 (CVS): speedup small gzip fonts loading
- Patch5 (CVS): fix rogue client crash

* Tue May 30 2006 Götz Waschk <waschk@mandriva.org> 2.2.1-2mdv2007.0
- mkrel

* Tue May 16 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-1mdk
- Release 2.2.1
- Remove patches 0, 1, 2, 3, 5, 6 (merged upstream)

* Wed Nov 16 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-10mdk
- Rebuild to get debug package

* Tue Sep 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-9mdk 
- Patch6 (David Turner): fix anti-aliasing rendering

* Wed Sep 21 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-8mdk 
- Remove patch4, it wasn't fixing the real problem which is in cairo

* Wed Sep 14 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-7mdk 
- Patch5 (CVS): fix disabled kerning

* Wed Aug 31 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-6mdk 
- Patch4 (Owen Taylor): fix font rendering in Cairo

* Thu Aug 25 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-5mdk 
- Patch2 (CVS): fix autofit render setup
- Patch3 (CVS): fix memleak

* Thu Aug 25 2005 Götz Waschk <waschk@mandriva.org> 2.1.10-4mdk
- fix bug 17248

* Thu Aug 04 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-3mdk 
- Patch1 (David Turner): put back internal API used by xorg-x11 (Mdk bug #14636)

* Wed Aug 03 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-2mdk 
- Patch0 (CVS): various fixes (mostly embolding)

* Tue Jul 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.10-1mdk 
- Release 2.1.10
- Remove patches 0, 3, 4, 5, 6, 7 (merged upstream)

* Thu Mar 17 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.9-6mdk 
- Disable patches 1 & 2, they seems to alter CJK (Mdk bug #14725)

* Thu Mar 10 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.9-5mdk 
- Patch1 (CVS): fix ttf hints distortions
- Patch2 (CVS): fix ttf interpreter
- Patch3 (CVS): fix stroker for closed outlines and single points
- Patch4 (CVS): fix cff font load 
- Patch5 (CVS): fix size comparison for BDF files
- Patch6 (CVS): fix size comparison for PCF files
- Patch7 (CVS): fix fractional size handling

* Thu Feb 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.9-4mdk
- nuke lib64 rpaths
- multiarch freetype-config (for --libtool)

* Mon Jan 31 2005 Frederic Lepied <flepied@mandrakesoft.com> 2.1.9-3mdk
- multiarch

* Fri Jul 23 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.1.9-2mdk
- use -O0 on ppc to prevent crashes with new fontconfig installed

* Tue Jul 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.9-1mdk
- Release 2.1.9
- Add check to lower optimizations for old gcc

* Sat Jul 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.8-2mdk
- Enable back optimizations (safe with gcc 3.4.x)

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.8-1mdk
- Release 2.1.8
- Remove patch0 (merged upstream)
