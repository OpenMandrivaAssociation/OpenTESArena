%bcond_without music
Name:           OpenTESArena
Version:        0.15.0
Release:        1
Summary:        Open-source re-implementation of The Elder Scrolls: Arena
License:        MIT
Group:          Amusements/Games/Action/Arcade
URL:            https://github.com/afritz1/OpenTESArena
Source0:        https://codeload.github.com/afritz1/OpenTESArena/tar.gz/refs/tags/opentesarena-%{version}#/%{name}-opentesarena-%{version}.tar.gz
#Source1:        %{name}.desktop
Source2:        %{name}-downloader
# PATCH-FEATURE-SUSE use-timidity.patch -- If build with midi support use timidity provided GUS patches
#Patch0:         use-timidity-0.14.0.patch
# PATCH-FEATURE-UPSTREAM custom-paths.patch -- Allow installing data and config into custom paths
#Patch1:         custom-paths-0.14.0.patch
# Does not build on TW without this
#Patch2:         tumbleweed_build.patch
BuildRequires:  cmake
BuildRequires:  hicolor-icon-theme
BuildRequires:  icoutils
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(sdl2)
%if %{with music}
BuildRequires:  pkgconfig(wildmidi)
Recommends:     timidity
%endif

%description
This open-source project aims to be a modern engine re-implementation for
"The Elder Scrolls: Arena" from 1994 by Bethesda Softworks.
It is written in C++17 and uses SDL2, WildMIDI for music, and OpenAL Soft for sound and mixing.

%prep
%setup -q -n %{name}-opentesarena-%{version}
%if %{with music}
%patch -P 0 -p 1
%endif
%patch -P 1 -p 1
%if 0%{?suse_version} > 1600
%patch -P 2 -p 1
%endif

%build
%cmake \
  -DOPENTESARENA_OPTIONSDIR=%{_sysconfdir}/%{name} \
  -DOPENTESARENA_DATADIR=%{_datadir}/%{name}
%make_build

%install
# Install binary
install -D -m 755 build/TESArena %{buildroot}%{_bindir}/%{name}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-downloader
# Install data
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -Rav data/* %{buildroot}%{_datadir}/%{name}
# Install system baseconfig
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -Rav options/* %{buildroot}%{_sysconfdir}/%{name}
# Fix data path in baseconfig
sed -i 's|ArenaPath=data|ArenaPath=%{_datadir}/%{name}|' %{buildroot}%{_sysconfdir}/%{name}/options-default.txt
# Install icons and .desktop file
for s in 32 48 64 ; do
    install -m755 -d %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/
    icotool -p0 -w ${s} -o %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png -x icon.ico
done

%post
echo "
To run %{name} you will need the original data files.
Either download and extract them manually (remember to set the path in %{_sysconfdir}/%{name}/options-default.txt).
Or run %{name}-downloader
"

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}*
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
