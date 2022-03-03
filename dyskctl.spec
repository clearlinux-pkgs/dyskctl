Name     : dyskctl
Version  : fcc6361a8f6fb2689ae555eaec6fc8455ab289a2
Release  : 30
URL      : https://github.com/khenidak/dysk/archive/fcc6361a8f6fb2689ae555eaec6fc8455ab289a2.tar.gz
Source0  : https://github.com/khenidak/dysk/archive/fcc6361a8f6fb2689ae555eaec6fc8455ab289a2.tar.gz
Source1  : http://localhost/dysk-extra-files.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : AGPL-3.0 Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 GPL-3.0 LGPL-3.0 MIT MPL-2.0-no-copyleft-exception
BuildRequires : go

%description
Attach Azure disks in < 1 second. Attach as many as you want. Attach them where
ever you want. dysk mounts Azure disks as Linux block devices directly on VMs
without dependency on the host.

%package extra
License:        AGPL-3.0 Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 GPL-3.0 LGPL-3.0 MIT MPL-2.0-no-copyleft-exception
Summary:        dyskctl extra files
Group    : Development/Tools

%description extra
Dyskctl extra files

%prep
%setup -q -n dysk-%{version}

%build
echo "dysk" > dysk.conf
export GOPATH=$HOME/go AUTO_GOPATH=1 GO111MODULE="auto"
mkdir -p $HOME/go/src/github.com/khenidak/
ln -s $HOME/build/BUILD/dysk-%{version} $HOME/go/src/github.com/khenidak/dysk
pushd $HOME/go/src/github.com/khenidak/dysk
tar xvzf %{SOURCE1}

# Remove dependency on dep
sed -E -i 's/^\s+(\$Q\s+)?dep\b.*$//g' dyskctl/Makefile

# Pre-create vendor paths
mkdir -p dyskctl/vendor/github.com/khenidak/dysk/dyskctl
mkdir -p dyskctl/vendor/github.com/khenidak/dysk/pkg

make  %{?_smp_mflags} build-cli GOFLAGS='-buildmode=pie -v'
popd

%install
# /builddir/build/BUILD/dysk-fcc6361a8f6fb2689ae555eaec6fc8455ab289a2/dyskctl/dyskctl
rm -rf %{buildroot}
install -d -p %{buildroot}/usr/lib/modules-load.d
install -p -m 644 dysk.conf %{buildroot}/usr/lib/modules-load.d
install -d -p %{buildroot}/usr/bin
install -p -m 755 dyskctl/dyskctl %{buildroot}/usr/bin

%files
%defattr(-,root,root,-)
/usr/bin/dyskctl

%files extra
%dir /usr/lib/modules-load.d
/usr/lib/modules-load.d/dysk.conf
