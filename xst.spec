Name:             xst
Version:          0.7.1
Release:          git
Summary:          A simple terminal implementation for X
License:          MIT
URL:              https://github.com/neeasade/xst
Source0:          https://github.com/neeasade/xst/archive/v%{version}.tar.gz
Source1:          xst.desktop
BuildRequires:    binutils
BuildRequires:    coreutils
BuildRequires:    gcc
BuildRequires:    desktop-file-utils
BuildRequires:    libX11-devel
BuildRequires:    libXext-devel
BuildRequires:    libXft-devel
BuildRequires:    make
BuildRequires:    sed
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
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/applications/%{name}.desktop
