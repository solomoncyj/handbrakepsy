%global commit0 012a0f15dfab1383899a6a04f7c84a336b578d70
%global date 20200613
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

# Build with "--without ffmpeg" or enable this to use bundled libAV
# instead of system FFMpeg libraries. Unfortunately with FFMpeg UTF-8
# subtitles are not recognized in media source files. :(
# https://trac.ffmpeg.org/ticket/6304
#global _without_ffmpeg 1

%ifarch i686 x86_64
%global _with_asm 1
%global _with_mfx 1
%endif

%global desktop_id fr.handbrake.ghb

Name:           HandBrake
Version:        1.3.3
Release:        14%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        An open-source multiplatform video transcoder
License:        GPLv2+
URL:            http://handbrake.fr/

%if 0%{?tag:1}
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}-source.tar.bz2
Source1:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}-source.tar.bz2.sig
# import from https://handbrake.fr/openpgp.php or https://github.com/HandBrake/HandBrake/wiki/OpenPGP
# gpg2 --export --export-options export-minimal 1629C061B3DDE7EB4AE34B81021DB8B44E4A8645 > gpg-keyring-1629C061B3DDE7EB4AE34B81021DB8B44E4A8645.gpg
Source2:        gpg-keyring-1629C061B3DDE7EB4AE34B81021DB8B44E4A8645.gpg
BuildRequires:  gnupg2
%else
Source0:        https://github.com/%{name}/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

%{?_without_ffmpeg:Source10:       https://libav.org/releases/libav-12.tar.gz}

# Build with unpatched libbluray (https://github.com/HandBrake/HandBrake/pull/458)
# can be dropped with libbluray-1.0.0
Patch1:         %{name}-no_clip_id.patch
# Pass strip tool override to gtk/configure
Patch3:         %{name}-nostrip.patch
# Don't link with libva unnecessarily
Patch4:         %{name}-no-libva.patch
# Fix QSV with unpatched system FFmpeg
Patch5:         %{name}-qsv.patch
# Fix build on non-x86 (without nasm)
Patch6:         %{name}-no-nasm.patch
# rhel gettext is too old to support metainfo
# https://github.com/HandBrake/HandBrake/pull/2884
Patch7:         %{name}-no-metainfo.patch
# https://github.com/HandBrake/HandBrake/pull/3537
Patch8:         https://github.com/HandBrake/HandBrake/commit/f28289fb06ab461ea082b4be56d6d1504c0c31c2.patch

BuildRequires:  a52dec-devel >= 0.7.4
BuildRequires:  cmake3
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
%if 0%{?fedora}
BuildRequires:  libappstream-glib
%endif
%{!?_without_ffmpeg:BuildRequires:  ffmpeg-devel >= 3.5}
# Should be >= 2.6:
BuildRequires:  freetype-devel >= 2.4.11
# Should be >= 0.19.7:
BuildRequires:  fribidi-devel >= 0.19.4
BuildRequires:  gcc-c++
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  intltool
BuildRequires:  jansson-devel
BuildRequires:  lame-devel >= 3.98
BuildRequires:  libappindicator-gtk3-devel
# Should be >= 0.13.2:
BuildRequires:  libass-devel >= 0.13.1
BuildRequires:  libbluray-devel >= 0.9.3
BuildRequires:  libdav1d-devel
BuildRequires:  libdrm-devel
BuildRequires:  libdvdnav-devel >= 5.0.1
BuildRequires:  libdvdread-devel >= 5.0.0
# FDK is non-free
%{?_with_fdk:BuildRequires:  fdk-aac-devel >= 0.1.4}
BuildRequires:  libgudev-devel
%if 0%{?_with_mfx:1}
BuildRequires:  libmfx-devel >= 1.23-1
BuildRequires:  libva-devel
%endif
BuildRequires:  libmpeg2-devel >= 0.5.1
BuildRequires:  libnotify-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
# Should be >= 1.5:
BuildRequires:  libvpx-devel >= 1.3
BuildRequires:  make
BuildRequires:  meson
%if 0%{?_with_asm:1}
BuildRequires:  nasm
%endif
%ifnarch %{arm}
BuildRequires:  numactl-devel
%endif
BuildRequires:  nv-codec-headers
BuildRequires:  opus-devel
BuildRequires:  python3
BuildRequires:  speex-devel
BuildRequires:  x264-devel >= 0.148
BuildRequires:  x265-devel >= 1.9
BuildRequires:  xz-devel

Requires:       hicolor-icon-theme
# needed for reading encrypted DVDs
%{?fedora:Recommends:     libdvdcss%{_isa}}
Obsoletes:      HandBrake-cli < %{version}-%{release}
Provides:       HandBrake-cli = %{version}-%{release}
Provides:       handbrake =  %{version}-%{release}

%description
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the command line version of the program.

%package gui
Summary:        An open-source multiplatform video transcoder (GUI)
Provides:       handbrake-gui = %{version}-%{release}
Requires:       hicolor-icon-theme
# needed for reading encrypted DVDs
%{?fedora:Recommends:     libdvdcss%{_isa}}
# needed for live preview
%{?fedora:Recommends:     gstreamer1-plugins-good%{_isa}}

%description gui
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the main program with a graphical interface.

%prep
%if 0%{?tag:1}
gpgv2 --keyring %{S:2} %{S:1} %{S:0}
%endif
%setup -q %{!?tag:-n %{name}-%{commit0}}
%if 0%{?rhel}
%patch1 -p1
%endif
%patch3 -p1
%if 0%{!?_with_mfx}
%patch4 -p1
%else
%patch5 -p1
%endif
%patch6 -p1
%if 0%{?rhel}
%patch7 -p1
%endif
%if 0%{fedora} > 33
%patch8 -p1
%endif
mkdir -p download
%{?_without_ffmpeg:cp -p %{SOURCE10} download}

# Use system libraries in place of bundled ones
for module in a52dec %{?_with_fdk:fdk-aac} %{!?_without_ffmpeg:ffmpeg} libdav1d libdvdnav libdvdread libbluray %{?_with_mfx:libmfx} nvenc libvpx x265; do
    sed -i -e "/MODULES += contrib\/$module/d" make/include/main.defs
done

# Fix desktop file
sed -i -e 's/%{desktop_id}.svg/%{desktop_id}/g' gtk/src/%{desktop_id}.desktop

%build
echo "HASH=%{commit0}" > version.txt
echo "SHORTHASH=%{shortcommit0}" >> version.txt
echo "DATE=$(date "+%Y-%m-%d %T" -d %{date})" >> version.txt
%if 0%{?tag:1}
echo "TAG=%{tag}" >> version.txt
echo "TAG_HASH=%{commit0}" >> version.txt
%endif

# This makes build stop if any download is attempted
export http_proxy=http://127.0.0.1

# By default the project is built with optimizations for speed and no debug.
# Override configure settings by passing RPM_OPT_FLAGS and disabling preset
# debug options.
echo "GCC.args.O.speed = %{optflags} -I%{_includedir}/ffmpeg -ldl -lx265 %{?_with_fdk:-lfdk-aac} %{?_with_mfx:-lmfx}" > custom.defs
echo "GCC.args.g.none = " >> custom.defs

# Not an autotools configure script.
./configure \
    --build build \
    --prefix=%{_prefix} \
    --debug=std \
    --strip=%{_bindir}/echo \
    --verbose \
    --disable-df-fetch \
    --disable-df-verify \
    --disable-gtk-update-checks \
    %{?_with_asm:--enable-asm} \
    --enable-x265 \
%ifarch %{arm}
    --disable-numa \
%endif
    %{?_with_fdk:--enable-fdk-aac} \
    %{?_with_mfx:--enable-qsv}

%make_build -C build V=1

%install
%make_install -C build

# Desktop file, icons and AppStream metadata from FlatPak build (more complete)
rm -f %{buildroot}/%{_datadir}/applications/ghb.desktop \
    %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/hb-icon.svg

install -D -p -m 644 gtk/src/%{desktop_id}.desktop \
    %{buildroot}/%{_datadir}/applications/%{desktop_id}.desktop
install -D -p -m 644 gtk/src/%{desktop_id}.svg \
    %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/%{desktop_id}.svg

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{desktop_id}.desktop

%if 0%{?fedora}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml
%endif

%find_lang ghb

%if 0%{?rhel} && 0%{?rhel} <= 7
%post gui
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%files -f ghb.lang gui
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/ghb
%if 0%{?fedora}
%{_metainfodir}/%{desktop_id}.metainfo.xml
%endif
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{desktop_id}.svg

%files
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/HandBrakeCLI

%changelog
* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Sérgio Basto <sergio@serjux.com> - 1.3.3-13
- Mass rebuild for x264-0.163

* Sun May 30 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.3.0-12
- fix audio encoders when linking to FFmpeg 4.4 (rfbz#6006)

* Wed Apr 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-11
- Rebuild for new x265

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-9
- Rebuilt for new ffmpeg snapshot

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-8
- Actually do the dav1d rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.3.3-7
- Rebuild for dav1d SONAME bump

* Fri Nov 27 2020 Sérgio Basto <sergio@serjux.com> - 1.3.3-6
- Mass rebuild for x264-0.161

* Wed Oct 21 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-5
- Rebuild for new libdvdread

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Sérgio Basto <sergio@serjux.com> - 1.3.3-3
- Mass rebuild for x264

* Wed Jul 01 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-2
- Rebuilt

* Sun Jun 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-1
- New upstream version

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-3
- Rebuild for new x265 version

* Sun May 24 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-2
- Rebuild for dav1d SONAME bump

* Tue May 05 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-1
- New upstream version

* Fri Mar 06 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.1-1
- New upstream version
- Update source URL
- Run scriptlets on el7 only

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-7
- Rebuild for x265

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-6
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 1.3.0-4
- Mass rebuild for x264

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-3
- Rebuild for new x265

* Wed Nov 27 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.3.0-2
- update commit hash and date for 1.3.0 release

* Thu Nov 21 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 1.3.0-1
- New upstream version (fixes compilation with Pango 1.44+)
- New dependencies: libdav1d, libdrm, libva, numactl
- dropped dependencies: yasm
- fixes rfbz#5426
- fix build on non-x86 (without nasm)

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.2.2-7
- rebuild for libdvdread ABI bump

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.2-6
- Rebuild for new ffmpeg version

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-5
- Rebuilt for x265

* Fri May 03 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.2-4
- Rebuild for new gstreamer1 version

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 1.2.2-3
- Mass rebuild for x264

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.2.2-1
- Update to 1.2.2

* Sun Jan 20 2019 Dominik Mierzejewski <rpm@greysector.net> - 1.2.0-1
- Update to 1.2.0
- Drop upstreamed subtitle handling patch
- Make libbluray patch EL-only, all current Fedoras have >1.0.0
- new dependencies: speex, xz
- enable asm parts on x86

* Sun Nov 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-1
- Rebuild for new x265
- Update to 1.1.2

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 1.1.0-4
- Mass rebuild for x264 and/or x265
- Add BuildRequires: gcc-c++

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-2
- Rebuild for new libass version

* Mon Apr 09 2018 Dominik Mierzejewski <rpm@greysector.net> - 1.1.0-1
- Update to 1.1.0
- Update source and signature URLs
- Drop obsolete patches
- Bump FFmpeg version requirement to 3.5+ due to AV_PKT_FLAG_DISPOSABLE API use

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.7-14
- Rebuilt for new ffmpeg snapshot

* Wed Feb 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-13
- Rebuilt for new x265
- Fix scriptlets

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-12
- Rebuilt for new libvpx

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-11
- Rebuilt for ffmpeg-3.5 git

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 1.0.7-10
- Mass rebuild for x264 and x265

* Fri Dec 29 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-9
- Fix SubRip subtitle issue when built with FFmpeg

* Fri Dec 01 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-8
- Rebuild against new libmfx (rhbz#1471768)

* Wed Nov 01 2017 Sérgio Basto <sergio@serjux.com> - 1.0.7-7
- Rebuild for x265 update

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-4
- update commit id to match 1.0.7 release
- drop redundant Provides/Obsoletes
- switch to a source URL that works with spectool/curl
- add GPG signature and verify it in prep

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-3
- Rebuild for ffmpeg and x265 update

* Wed Apr 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.7-2
- Remove webkitgtk3 build requirement, it's actually used only when the update
  checks are enabled in the gui (not needed in our case and removed in fc27).

* Wed Apr 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.7-1
- Update to latest 1.0.7.

* Thu Mar 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-4
- Fix ppc64le build

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar 18 2017 Xavier Bachelot <xavier@bachelot.org> - 1.0.3-2
- Don't apply clip_id patch for releases shipping with libbluray 1.0.0.

* Wed Mar 08 2017 Xavier Bachelot <xavier@bachelot.org> - 1.0.3-1
- Update to 1.0.3.
- Use Recommends: only for Fedora.
- Fix debuginfo sub-package.

* Sat Jan 28 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.2-1
- update to 1.0.2
- avoid unnecessary libva dependency

* Fri Jan 20 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.1-1
- Update to 1.0.1.
- Use make_build macro.
- Fix BRs and drop redundant ones.
- libva is required to build with QSV.
- Provide lowercase name provides.
- Restore support for building with bundled libav.

* Fri Dec 02 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.0-33.20161201git8a9f21c
- Update to latest sources.
- Soft dependency on gstreamer1-plugins-good for live preview.
- Change hard dependency on libdvdcss to soft.
- libmfx is x86-only.
- Move -cli to the main package.
- Drop support for building with libav.

* Thu Dec 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0-32.20161129gitfac5e0e
- Update to latest snapshot.
- Add patches from Dominik Mierzejewski:
  * Allow use of unpatched libbluray.
  * Use system OpenCL headers.
  * Do not strip binaries.

* Fri Nov 18 2016 Simone Caronni <negativo17@gmail.com> - 1.0-31.20161116gitb9c5daa
- Update to latest snapshot.
- Use Flatpak desktop file, icon and AppStream metadata (more complete).

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-30.20161006git88807bb
- Fix date.
- Rebuild for fdk-aac update.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-29.20160929git88807bb
- Require x265 hotfix.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-28.20160929gitd398531
- Rebuild for x265 update.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-27.20160929gitd398531
- Update to latest snapshot.
- Update package release according to package guidelines.
- Enable Intel Quick Sync Video encoding by default (libmfx package in main
  repositories).
- Add AppData support for Fedora (metadata from upstream).
- Do not run update-desktop-database on Fedora 25+ as per packaging guidelines.

* Fri Aug 05 2016 Simone Caronni <negativo17@gmail.com> - 1.0-26.6b5d91a
- Update to latest sources.

* Thu Jul 14 2016 Simone Caronni <negativo17@gmail.com> - 1.0-25.56c7ee7
- Update to latest snapshot.

* Fri Jul 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-24.0fc54d0
- Update to latest sources.

* Sun Jul 03 2016 Simone Caronni <negativo17@gmail.com> - 1.0-23.b1a4f0d
- Update to latest sources.

* Sun Jun 19 2016 Simone Caronni <negativo17@gmail.com> - 1.0-22.221bfe7
- Update to latest sources, bump build requirements.

* Tue May 24 2016 Simone Caronni <negativo17@gmail.com> - 1.0-21.879a512
- Update to latest sources.

* Wed Apr 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0-20.8be786a
- Update to latest sources.
- Update build requirements of x264/x265 to match upstream.

* Thu Mar 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-19.a447656
- Bugfixes.

* Tue Mar 29 2016 Simone Caronni <negativo17@gmail.com> - 1.0-18.113e2a5
- Update to latest snapshot for various fixes.

* Wed Mar 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-17.12f7be2
- Update to latest sources.

* Fri Feb 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0-16.0da688d
- Update to latest snapshot.

* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-15.ba5eb77
- Update to latest snapshot.

* Fri Jan 22 2016 Simone Caronni <negativo17@gmail.com> - 1.0-14.08e7b54
- Update to latest sources, contains normalization fix.
- Make Intel QuickSync encoder suppport conditional at build time.

* Sat Jan 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-13.ed8c11e
- Update to latest sources.

* Fri Jan 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-12.ee1167e
- Update to latest sources.

* Wed Dec 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-11.1e56395
- Update sources. Intel Quick Sync hardware support can be built using the same
  library as FFMpeg. No frontend support yet.

* Mon Dec 21 2015 Simone Caronni <negativo17@gmail.com> - 1.0-10.57a9f48
- Update sources.

* Fri Dec 11 2015 Simone Caronni <negativo17@gmail.com> - 1.0-9.3443f6a
- Update to latest sources.

* Sun Dec 06 2015 Simone Caronni <negativo17@gmail.com> - 1.0-8.ca69335
- Update to latest sources.

* Tue Dec 01 2015 Simone Caronni <negativo17@gmail.com> - 1.0-7.46e641c
- Switch back to bundled libav 11 to fix subtitle detection.
- Make bundling libav conditional.

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com> - 1.0-6.46e641c
- Update to latest sources.

* Mon Nov 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-5.6c731e1
- Update ffmpeg patch.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.0-4.6c731e1
- Update to latest upstream.
- Add license macro.

* Sat Nov 14 2015 Simone Caronni <negativo17@gmail.com> - 1.0-3.6d66bd5
- Use system libfdk-aac.

* Tue Nov 10 2015 Simone Caronni <negativo17@gmail.com> - 1.0-2.6d66bd5
- Update snapshot.
- Use packaging guidelines for GitHub snapshots.
- Update fdk-aac bundle.
- Update build requirements.

* Wed Oct 28 2015 Simone Caronni <negativo17@gmail.com> - 1.0-1
- Update to master branch.
- Use system x265.

* Fri Oct 23 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-3
- Udpate patches from 0.10.x branch.
- Use system ffmpeg libraries in place of bundled libav.

* Mon Sep 28 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-2
- Update latest patches from the 0.10.x branch.

* Thu Jun 11 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-1
- Update to 0.10.2.
- Use handbrake.fr URL for source 0.

* Mon Mar 09 2015 Simone Caronni <negativo17@gmail.com> - 0.10.1-1
- Update to 0.10.1.

* Mon Jan 26 2015 Simone Caronni <negativo17@gmail.com> - 0.10.0-12
- Fix huge icons problem.

* Wed Nov 26 2014 Simone Caronni <negativo17@gmail.com> - 0.10.0-11
- Update to 0.10.0 official release.

* Wed Nov 05 2014 Simone Caronni <negativo17@gmail.com> - 0.10-10.svn6507
- Update to SVN revision 6507.

* Mon Nov 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-9.svn6502
- Update to SVN revision 6502.

* Fri Oct 24 2014 Simone Caronni <negativo17@gmail.com> - 0.10-8.svn6461
- Update to SVN revision 6461.

* Fri Oct 10 2014 Simone Caronni <negativo17@gmail.com> - 0.10-7.svn6439
- Update to SVN revision 6439.

* Fri Oct 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-6.svn6422
- Update to SVN revision 6430.

* Sun Sep 28 2014 Simone Caronni <negativo17@gmail.com> - 0.10-5.svn6422
- Update to SVN revision 6422.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-4.svn6404
- Update to SVN revision 6404.
- Update libdvdread and libdvdnav requirements.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-3.svn6394
- Update to SVN revision 6394.

* Mon Sep 01 2014 Simone Caronni <negativo17@gmail.com> - 0.10-2.svn6386
- Update to svn revision 6386; new x265 presets.
- Update x265 libraries.

* Sat Aug 23 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-17.svn6304
- Update to svn revision 6351. HandBrake version is now 0.10:
  https://trac.handbrake.fr/milestone/HandBrake%200.10
- Lame and x264 libraries are now linked by default.
- Remove mkv, mpeg2dec and libmkv as they are no longer used.
- LibAV is now enabled by default.
- Add libappindicator-gtk3 build requirement.

* Sun Aug 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-16.svn6304
- Update to 6304 snapshot.

* Wed Aug 06 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-15.svn6268
- Update to latest snapshot.

* Wed Jul 30 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-14.svn6244
- Updated to latest snapshot.
- Enable avformat muxer, replaces libmkv and mp4v2 support.
- Requires libdvdnav >= 5.0.0 to fix crashes.
- Remove ExclusiveArch.

* Sat Jul 05 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-13.svn6227
- Updated to SVN snapshot.
- Remove RHEL 6 conditionals.

* Tue Mar 25 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-12
- Backport DVD changes from trunk (should fix libdvdnav crashes with specific
  DVD titles).
- Use system ffpmeg 2 libraries in place of bundled libav.

* Mon Mar 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-11
- Fix crash on Fedora.

* Fri Mar 14 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-10
- Use system libdvdnav/libdvdread.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-9
- Use system libraries for libbluray, lame, mpeg2dec, a52dec (patch), libmkv
  (patch), x264 (faac, fdk-aac, libav, libdvdnav, libdvdread and mp4v2 are still
  bundled).
- Use Fedora compiler options.
- Use GStreamer 1.x on Fedora and RHEL/CentOS 7.
- Add fdk-aac support.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-8
- Scriptlets need to run for gui subpackage and not base package. Thanks to
  Peter Oliver.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-7
- Add requirement on libdvdcss, fix hicolor-icon-theme requirement.

* Fri Jul 26 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-6
- Enable building CLI only on CentOS/RHEL 6.
- Disable GTK update checks (updates come only packaged).

* Tue Jul 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-5
- Enable command line interface only for CentOS/RHEL 6.

* Thu May 30 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-4
- Updated x264 to r2282-1db4621 (stable branch) to fix Fedora 19 crash issues.

* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-3
- Update to 0.9.9.
- Separate GUI and CLI packages.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-2.5449svn
- Updated.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-1.5433svn
- First build.
