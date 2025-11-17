#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# Required for PCLinuxOS: removes the ldflag '--no-undefined'
%if 0%{?pclinuxos}
%define _disable_ld_no_undefined 1
%endif

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg bibletime
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.6.6.0
Release:		%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		A bible study tool for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/misc/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	libtool
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# BOOST support
BuildRequires:   boost-devel

# Requires: clucene
BuildRequires:  pkgconfig(libclucene-core)

# Requires: sword
BuildRequires:	pkgconfig(sword)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

%description
BibleTime is a free and easy to use bible study tool for UNIX systems.
It requires a working TDE environment and the SWORD library.
BibleTime provides easy handling of digitized texts (Bibles, commentaries
and lexicons) and powerful features to work with these texts (search in
texts, write own notes, save, print etc.).
 
##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

# Warning: GCC visibility causes FTBFS [Bug #1285]
%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR=$RPM_BUILD_ROOT -C build

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/bibletime
%{tde_tdeincludedir}/bibletimeinterface.h
%{tde_tdeappdir}/bibletime.desktop
%{tde_datadir}/apps/bibletime/
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_tdedocdir}/HTML/en/bibletime/
%lang(de) %dir %{tde_mandir}/de/
%lang(de) %dir %{tde_mandir}/de/man1/
%lang(de) %{tde_mandir}/de/man1/bibletime.1*
%{tde_mandir}/man1/bibletime.1*

