Summary:	TrueType font rasterizer library
Name:		freetype
Version:	1.3.1
Release:	%mkrel 36
License:	BSD
Group:		System/Libraries
BuildRequires:	libsm-devel libx11-devel libice-devel
BuildRequires:	autoconf2.1 automake1.4
URL:		http://www.freetype.org
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		freetype-%{version}.tar.bz2
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

%package devel
Summary:	Header files and static library for development with FreeType
Group:		Development/C
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
	--enable-static \
	--enable-shared \
	--with-locale-dir=%{_datadir}/locale
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

rm -f $RPM_BUILD_ROOT%{_bindir}/ft*

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

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
