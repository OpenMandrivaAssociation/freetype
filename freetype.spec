%define version 1.3.1
%define release %mkrel 26

Summary:	Free TrueType font rasterizer library.
Name:		freetype
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
BuildRequires:	XFree86-devel
BuildRequires:	autoconf2.1
URL:		http://www.freetype.org
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		freetype-%{version}.tar.bz2
Source1:	ttmkfdir.tar.bz2
# Patch from X-TT sources, to correctly support Dynalab TTF fonts
# very popular in Taiwan
Patch:		freetype1.3-adw-nocheck.patch
Patch1:		freetype-1.3.1-compile-self.patch
# (gb) Disable byte-code interpreter
Patch2:		freetype-1.3.1-disable-bci.patch
# (nanar) fix gcc33 build, included in cvs version
Patch3:		freetype-1.3.1-gcc33.patch
# (abel) no need to include libintl
Patch4:		freetype-1.3.1-no-intl.patch

%package devel
Summary:	Header files and static library for development with FreeType.
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%package tools
Summary:	Tools to manipulate TTF fonts
Group:		System/Fonts/True type
Requires:	%{name} = %{version}-%{release}

%description
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType is a library, not a
stand-alone application, though some utility applications are included.

%description devel
This package is only needed if you intend to develop or
compile applications which rely on the FreeType library.
If you simply want to run existing applications, you won't
need this package.

%description tools
Tools to manipulate TTF fonts.

%prep
%setup -q -a 1

%patch -p0 -b .adw
%patch1 -p0
%patch2 -p1 -b .disable-bci
%patch3 -p0
%patch4 -p1 -b .no-intl

autoconf

%build
%configure --disable-debug \
	--enable-static \
	--enable-shared \
	--with-locale-dir=%{_datadir}/locale
make
make -C ttmkfdir-1.1

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale
make -C ttmkfdir-1.1 install
ln -sf %{_sbindir}/ttmkfdir $RPM_BUILD_ROOT%{_bindir}/ttmkfdir
rm -f $RPM_BUILD_ROOT%{_bindir}/ft*
%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root,-)
%{_libdir}/libttf.so.*
%doc README announce

%files devel
%defattr(-,root,root,-)
%doc docs
%{_includedir}/*
%{_libdir}/libttf.so
%{_libdir}/libttf.la
%{_libdir}/libttf.a

%files tools
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*

