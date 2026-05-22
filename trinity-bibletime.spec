%bcond clang 1

# TDE variables
%define tde_pkg bibletime
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity

Name:			trinity-%{tde_pkg}
Version:		14.1.6
Release:		1
Summary:		A bible study tool for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/applications/misc/%{tarball_name}-%{version}.tar.xz

BuildSystem:	  cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DLIB_INSTALL_DIR=%{tde_prefix}/%{_lib}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdebase-devel >= %{version}
BuildRequires:  trinity-tde-cmake >= %{version}

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
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/bin/bibletime
%{tde_prefix}/include/tde/bibletimeinterface.h
%{tde_prefix}/share/applications/tde/bibletime.desktop
%{tde_prefix}/share/apps/bibletime/
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/doc/tde/HTML/en/bibletime/
%lang(de) %dir %{tde_prefix}/share/man/de/
%lang(de) %dir %{tde_prefix}/share/man/de/man1/
%lang(de) %{tde_prefix}/share/man/de/man1/bibletime.1*
%{tde_prefix}/share/man/man1/bibletime.1*

