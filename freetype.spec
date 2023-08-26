# wine and several of its dependencies use freetype
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 6
%define libname %mklibname freetype %{major}
%define devname %mklibname -d freetype %{major}
%define lib32name %mklib32name freetype %{major}
%define dev32name %mklib32name -d freetype %{major}
%ifarch x86_64
# Workaround for x86_64 (not znver1) specific clang breakage at build time
# https://abf.openmandriva.org/build_lists/289816
%global optflags %{optflags} -O1
%else
%global optflags %{optflags} -O3
%endif
%define git_url git://git.sv.gnu.org/freetype/freetype2.git
%bcond_without harfbuzz
%bcond_without rsvg

Summary:	A free and portable TrueType font rendering engine
Name:		freetype
Version:	2.13.2
%define docver %(echo %version |cut -d. -f1-3)
Release:	1
License:	FreeType License/GPLv2
Group:		System/Libraries
Url:		http://www.freetype.org/
Source0:	http://downloads.sourceforge.net/freetype/%{name}-%{version}.tar.xz
Source1:	http://downloads.sourceforge.net/freetype/%{name}-doc-%{version}.tar.xz
Source2:	http://downloads.sourceforge.net/freetype/ft2demos-%{version}.tar.xz
Patch0:		freetype-2.11-autogen.patch
Patch2:		0001-Enable-table-validation-modules.patch
# Enable subpixel rendering (ClearType)
Patch4:		freetype-2.3.0-enable-spr.patch

BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libbrotlidec)
%if %{with rsvg}
BuildRequires:	pkgconfig(librsvg-2.0)
%endif
%if %{with harfbuzz}
BuildRequires:	pkgconfig(harfbuzz)
%endif
BuildRequires:	pkgconfig(graphite2)
%if %{with compat32}
BuildRequires:	devel(libX11)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libpng16)
%endif

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared libraries for a free and portable TrueType font rendering engine (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included

%package -n %{dev32name}
Summary:	Header files and static library for development with FreeType2 (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	devel(libbz2)

%description -n %{dev32name}
This package is only needed if you intend to develop or compile applications
which rely on the FreeType2 library. If you simply want to run existing
applications, you won't need this package.
%endif

%prep
%autosetup -p1 -a1 -a2
ln -s ft2demos-%{version} ft2demos

enable() {
    if [ "$#" = "1" ]; then
	KEY=FT_CONFIG_OPTION_${1}
    else
	KEY=${1}_CONFIG_OPTION_${2}
    fi
    sed -i -e "s|^/\* #define ${KEY} \*/|#define ${KEY}|" ftoption.h ../include/freetype/config/ftoption.h ../devel/ftoption.h
}
disable() {
    if [ "$#" = "1" ]; then
	KEY=FT_CONFIG_OPTION_${1}
    else
	KEY=${1}_CONFIG_OPTION_${2}
    fi
    sed -i -e "s|^#define ${KEY}\$|/* #define ${KEY} */|" ftoption.h ../include/freetype/config/ftoption.h ../devel/ftoption.h
}

./autogen.sh

export CONFIGURE_TOP="$(pwd)"
touch configure.ac

%if %{with compat32}
mkdir -p build32/lib
cd build32
# FIXME Enable harfbuzz even in 32-bit mode
# once it is built
%configure32 \
	--enable-freetype-config \
	--with-harfbuzz=no \
	--with-zlib=yes \
	--with-bzip2=yes \
	--with-png=yes

enable SUBPIXEL_RENDERING
enable PCF LONG_FAMILY_NAMES
disable CFF OLD_ENGINE
enable SYSTEM_ZLIB

sed -i -e 's,^/\* #define FT_EXPORT_DEF(x).*,#define FT_EXPORT_DEF(x) __attribute__((visibility("default"))) x,' ftoption.h ../include/freetype/config/ftoption.h ../devel/ftoption.h
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-freetype-config \
%if %{with harfbuzz}
	--with-harfbuzz=yes \
%else
	--with-harfbuzz=no \
%endif
	--with-brotli=yes \
%if %{with rsvg}
	--with-librsvg=yes \
%else
	--with-librsvg=no \
%endif
	--with-zlib=yes \
	--with-bzip2=yes \
	--with-png=yes

enable SUBPIXEL_RENDERING
enable PCF LONG_FAMILY_NAMES
disable CFF OLD_ENGINE
enable SYSTEM_ZLIB

sed -i -e 's,^/\* #define FT_EXPORT_DEF(x).*,#define FT_EXPORT_DEF(x) __attribute__((visibility("default"))) x,' ftoption.h ../include/freetype/config/ftoption.h ../devel/ftoption.h

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build
%make_build -C build FT2DEMOS=1 TOP_DIR_2=$(realpath ./ft2demos)

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

install -d %{buildroot}%{_bindir}

for ftdemo in ftbench ftdiff ftdump ftgamma ftgrid ftlint ftmulti ftstring ftvalid ftview; do
    build/libtool --mode=install install -m 755 ft2demos-%{docver}/bin/$ftdemo %{buildroot}%{_bindir}
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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libfreetype.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
