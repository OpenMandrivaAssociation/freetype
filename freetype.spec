%define major 2
%define libname	%mklibname freetype %{major}
%define develname %mklibname -d freetype %{major}

Summary:	TrueType font rasterizer library
Name:		freetype
Version:	1.3.1
Release:	41
License:	BSD
Group:		System/Libraries
BuildRequires:	libsm-devel libx11-devel libice-devel
BuildRequires:	autoconf2.1 automake1.4
URL:		http://www.freetype.org
Source0:	freetype-%{version}.tar.bz2
# Patch from X-TT sources, to correctly support Dynalab TTF fonts
# very popular in Taiwan
Patch0:		freetype1.3-adw-nocheck.patch
# (gb) Disable byte-code interpreter
Patch2:		freetype-1.3.1-disable-bci.patch
# (nanar) fix gcc33 build, included in cvs version
Patch3:		freetype-1.3.1-gcc33.patch
# (abel) no need to include libintl
Patch4:		freetype-1.3.1-no-intl.patch
Patch5:		freetype-1.3.1-format_not_a_string_literal_and_no_format_arguments.diff

%description
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType is a library, not a
stand-alone application, though some utility applications are included.

%package -n	%{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType is a library, not a
stand-alone application, though some utility applications are included.

%package -n	%{develname}
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package is only needed if you intend to develop or compile applications
which rely on the FreeType library. If you simply want to run existing
applications, you won't need this package.

%prep

%setup -q
%patch0 -p0 -b .adw
%patch2 -p1 -b .disable-bci
%patch3 -p0
%patch4 -p1 -b .no-intl
%patch5 -p0 -b .format_not_a_string_literal_and_no_format_arguments

cp -f /usr/share/automake-1.4/config.guess .
cp -f /usr/share/automake-1.4/config.sub .

autoconf-2.13

%build
%configure2_5x --disable-debug \
	--disable-static \
	--enable-shared \
	--with-locale-dir=%{_datadir}/locale
make

%install
rm -rf %{buildroot}

%makeinstall gnulocaledir=%{buildroot}%{_datadir}/locale

rm -f %{buildroot}%{_bindir}/ft*

%find_lang %{name}

%files -n %{libname} -f %{name}.lang
%doc README announce
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc docs
%{_includedir}/*
%{_libdir}/libttf.so

%changelog
* Sat Dec 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-39
+ Revision: 737455
- drop the static lib and the libtool *.la file
- various fixes

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-38
+ Revision: 664355
- mass rebuild

* Sat Sep 25 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-37mdv2011.0
+ Revision: 580983
- ahh, stupid build system...
- libified the package

* Fri Sep 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-36mdv2011.0
+ Revision: 580932
- ttmkfdir will be a separate package, should obsolete freetype-1

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-35mdv2010.1
+ Revision: 521127
- rebuilt for 2010.1

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 1.3.1-34mdv2010.0
+ Revision: 448403
- buildrequire automake1.4
- fix build on x86_64 by overwriting config.{guess,sub} (from Arnaud Patard)
- use smaller build deps than x11-devel (from Arnaud Patard)

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild
    - Use %%configure2_5x instead of %%configure so that libtoolize isn't run automatically

* Tue Dec 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-30mdv2009.1
+ Revision: 321371
- fix build with -Werror=format-security (P5)

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-29mdv2009.0
+ Revision: 221004
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-28mdv2008.1
+ Revision: 170844
- rebuild

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-27mdv2008.1
+ Revision: 150084
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel
- fix summary-ended-with-dot

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Sep 19 2007 Adam Williamson <awilliamson@mandriva.org> 1.3.1-26mdv2008.0
+ Revision: 91121
- d'oh, call autoconf 2.1 CORRECTLY
- call autoconf 2.1 specifically
- rebuild for 2008. this package is completely wrong (it's a library and should follow the lib policy, and ttmkfdir should be in a separate package as it has no relation to this one) but don't want to risk breaking anything by fixing it now...


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.3.1-25mdv2007.1
+ Revision: 146592
- move big doc in -devel

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.3.1-24mdv2007.1
+ Revision: 115468
- Import freetype

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.3.1-24mdv2007.1
- unpack patches

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.3.1-24mdk
- Rebuild

* Mon May 24 2004 Abel Cheung <deaddog@deaddog.org> 1.3.1-23mdk
- Patch4: No need to link with libintl

* Sat Apr 24 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.1-22mdk
- relink with new libintl

