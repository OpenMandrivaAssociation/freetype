%define major 2
%define libname	%mklibname freetype %{major}
%define develname %mklibname -d freetype %{major}

Summary:	TrueType font rasterizer library
Name:		freetype
Version:	1.3.1
Release:	39
License:	BSD
Group:		System/Libraries
BuildRequires:	libsm-devel libx11-devel libice-devel
BuildRequires:	autoconf2.1 automake1.4
URL:		http://www.freetype.org
Source0:		freetype-%{version}.tar.bz2
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
Obsoletes:	%{name}
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
Obsoletes:	%{name}-devel
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

%find_lang %name

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname} -f %name.lang
%doc README announce
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc docs
%{_includedir}/*
%{_libdir}/libttf.so
