%define major 6
%define libname %mklibname freetype %{major}
%define devname %mklibname -d freetype %{major}
%global optflags %{optflags} -O3
%define git_url git://git.sv.gnu.org/freetype/freetype2.git
%bcond_without harfbuzz

Summary:	A free and portable TrueType font rendering engine
Name:		freetype
Version:	2.10.2
%define docver %(echo %version |cut -d. -f1-3)
Release:	1
License:	FreeType License/GPLv2
Group:		System/Libraries
Url:		http://www.freetype.org/
Source0:	http://downloads.sourceforge.net/freetype/%{name}-%{version}.tar.xz
Source1:	http://downloads.sourceforge.net/freetype/%{name}-doc-%{version}.tar.xz
Source2:	http://downloads.sourceforge.net/freetype/ft2demos-%{version}.tar.xz
Patch1:		freetype-2.4.2-CVE-2010-3311.patch
Patch2:		0001-Enable-table-validation-modules.patch
Patch3:		0002-Enable-infinality-subpixel-hinting.patch
# Enable subpixel rendering (ClearType)
Patch4:		freetype-2.3.0-enable-spr.patch

BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libpng)
%if %{with harfbuzz}
BuildRequires:	pkgconfig(harfbuzz)
%endif
BuildRequires:	pkgconfig(graphite2)

%description
The FreeType2 engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType2 is a library, not a
stand-alone application, though some utility applications are included

%package -n %{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included

%package -n %{devname}
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
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
%autosetup -p1 -a1 -a2

enable() {
    if [ "$#" = "1" ]; then
	KEY=FT_CONFIG_OPTION_${1}
    else
	KEY=${1}_CONFIG_OPTION_${2}
    fi
    sed -i -e "s|^/\* #define ${KEY} \*/|#define ${KEY}|" include/freetype/config/ftoption.h devel/ftoption.h builds/unix/ftoption.h
}
disable() {
    if [ "$#" = "1" ]; then
	KEY=FT_CONFIG_OPTION_${1}
    else
	KEY=${1}_CONFIG_OPTION_${2}
    fi
    sed -i -e "s|^#define ${KEY}\$|/* #define ${KEY} */|" include/freetype/config/ftoption.h devel/ftoption.h builds/unix/ftoption.h
}

./autogen.sh
%configure \
	--enable-freetype-config \
%if %{with harfbuzz}
	--with-harfbuzz=yes \
%else
	--with-harfbuzz=no \
%endif
	--with-zlib=yes \
	--with-bzip2=yes \
	--with-png=yes

enable SUBPIXEL_RENDERING
enable PCF LONG_FAMILY_NAMES
disable CFF OLD_ENGINE

sed -i -e 's,^/\* #define FT_EXPORT_DEF(x).*,#define FT_EXPORT_DEF(x) __attribute__((visibility("default"))) x,' include/freetype/config/ftoption.h devel/ftoption.h builds/unix/ftoption.h

%build
%make_build

cd ft2demos-%{version}
# The purpose of overriding LINK_LIBRARY is getting rid of ****ing
# rpath
%make TOP_DIR=".." X11_LIB="" \
LINK_LIBRARY='$(LIBTOOL) --mode=link $(CCraw) -o $@ $(OBJECTS_LIST) \
                          -version-info $(version_info) \
                           $(LDFLAGS) -no-undefined \
                           # -export-symbols $(EXPORTS_LIST)'
cd -

%install
%make_install

install -d %{buildroot}%{_bindir}

for ftdemo in ftbench ftdiff ftdump ftgamma ftgrid ftlint ftmulti ftstring ftvalid ftview; do
    builds/unix/libtool --mode=install install -m 755 ft2demos-%{docver}/bin/$ftdemo %{buildroot}%{_bindir}
done

# compatibility symlink
ln -sf freetype2 %{buildroot}%{_includedir}/freetype

%files -n %{libname}
%{_libdir}/libfreetype.so.%{major}*

%files -n %{devname}
%doc docs/*
%{_bindir}/freetype-config
%{_libdir}/*.so
%{_includedir}/freetype
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_mandir}/man1/freetype-config.1*

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
