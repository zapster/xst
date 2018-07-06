Name:             xst
Version:          0.7.1
Release:          1
Summary:          A simple terminal implementation for X
License:          MIT
URL:              https://github.com/neeasade/xst
Source0:          https://github.com/neeasade/xst/archive/v%{version}.tar.gz
Source1:          xst.desktop
Source2:          xst.svg
BuildRequires:    binutils
BuildRequires:    coreutils
BuildRequires:    gcc
BuildRequires:    desktop-file-utils
BuildRequires:    libX11-devel
BuildRequires:    libXext-devel
BuildRequires:    libXft-devel
BuildRequires:    make
BuildRequires:    sed
BuildRequires:    xdg-utils
BuildRequires:    ImageMagick
Requires:         font(liberationmono)
Requires:         ncurses-base

%description
A simple virtual terminal emulator for X which sucks less.

%prep
%setup -q
#sed -e "s!^\(CFLAGS.*$\)!\1 %{optflags}!" \
#    -e "s!^\(LDFLAGS.*$\)!\1 %{?__global_ldflags}!" \
#    -i config.mk
# terminfo entries are provided by ncurses-base
sed -e "/@tic/d" -i Makefile

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
mv %{buildroot}%{_bindir}/{st,%{name}}
mv %{buildroot}%{_mandir}/man1/{st,%{name}}.1
for res in 16 24 32 48 256 ; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  convert %{SOURCE2} -resize ${res}x${res} \
    %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/%{name}.png
done
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*
