%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

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

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.6.6.0
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		A bible study tool for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/misc/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:	  cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH="%{tde_libdir}"
BuildOption:    -DCMAKE_NO_BUILTIN_CHRPATH=ON
BuildOption:    -DBIN_INSTALL_DIR=%{tde_bindir}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir}
BuildOption:    -DLIB_INSTALL_DIR=%{tde_libdir}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_datadir}
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	libtool
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

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
 

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"


%install -a
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

