%define build_subpixel 0
%define build_plf 0
%{?_with_plf: %global build_plf 1}
%{?_with_subpixel: %global build_subpixel 1}

%if %build_plf
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
#%define extrarelsuffix plf
%define build_subpixel 1
%endif

%define major	6
%define libname	%mklibname freetype %{major}
%define devname %mklibname -d freetype %{major}

%define git_url git://git.sv.gnu.org/freetype/freetype2.git

Summary:	A free and portable TrueType font rendering engine
Name:		freetype
Version:	2.4.12
Release:	2%{?extrarelsuffix}
License:	FreeType License/GPLv2
Group:		System/Libraries
Url:		http://www.freetype.org/
Source0:	http://mirrors.zerg.biz/nongnu/freetype/%{name}-%{version}.tar.gz
Source1:	http://mirrors.zerg.biz/nongnu/freetype/%{name}-%{version}.tar.gz.sig
Source2:	http://mirrors.zerg.biz/nongnu/freetype/%{name}-doc-%{version}.tar.gz
Source3:	http://mirrors.zerg.biz/nongnu/freetype/%{name}-doc-%{version}.tar.gz.sig
Source4:	http://mirrors.zerg.biz/nongnu/freetype/ft2demos-%{version}.tar.gz
Source5:	http://mirrors.zerg.biz/nongnu/freetype/ft2demos-%{version}.tar.gz.sig
Patch0:		ft2demos-2.3.12-mathlib.diff
Patch1:		freetype-2.4.2-CVE-2010-3311.patch
Patch2:		freetype-2.4.12-enable-adobe-cff-engine.patch

BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)

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
%setup -qn freetype-%{version} -a2 -a4

pushd ft2demos-%{version}
%patch0 -p0
popd

%patch1 -p1 -b .CVE-2010-3311
%patch2 -p1 -b .cff~

%if %{build_subpixel}
sed -i -e 's|^/\* #define FT_CONFIG_OPTION_SUBPIXEL_RENDERING \*/| #define FT_CONFIG_OPTION_SUBPIXEL_RENDERING|' include/freetype/config/ftoption.h
%endif

#./autogen.sh --help || :

%build
# some apps crash on ppc without this
%ifarch ppc
export CFLAGS="`echo %{optflags} |sed s/O2/O0/`"
%endif

%configure2_5x \
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

%files -n %{libname}
%{_libdir}/libfreetype.so.%{major}*

%files -n %{devname}
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

