# disable debug
%define debug_package %{nil}

Name:	umurmur	
Version: 0.2.20	
Release: 0%{?dist}
Summary: Minimalistic Mumble server	

Group:	Applications/Internet	
License: Custom
URL:	https://github.com/umurmur/umurmur	
Source0: umurmur-%{version}.tar.gz
Source1: umurmur.systemd
#Source2: umurmur.init
BuildRequires:	automake libtool protobuf-c-devel openssl-devel libconfig-devel
Requires: protobuf-c openssl
Requires(pre): shadow-utils

%description
Minimalistic Mumble server

%prep
%setup -q


%build
./autogen.sh
%configure --with-ssl=openssl
# patch file?
sed -i '/CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_ON);/d' src/ssli_openssl.c # https://github.com/umurmur/umurmur/issues/176

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# configs
%{__mkdir_p} %{buildroot}/etc/%{name}
%{__cp} umurmur.conf.example  %{buildroot}/etc/umurmur.conf

# /var/run stuff
%{__mkdir_p} %{buildroot}/var/run/%{name}

# needed on el7+ using systemd
%{__mkdir_p} %{buildroot}/etc/tmpfiles.d
echo "d /run/umurmur 775 umurmur umurmur" > %{buildroot}/etc/tmpfiles.d/%{name}.conf
%{__mkdir_p} %{buildroot}/etc/systemd/system/
%{__cp} %{SOURCE1} %{buildroot}/etc/systemd/system/umurmurd.service

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
    -c "umurmur service accounts" %{name}
exit 0

%post
# needed on el7+ using systemd
/bin/systemd-tmpfiles --create /etc/tmpfiles.d/umurmur.conf
/bin/systemctl daemon-reload

%files 
%doc
%dir /etc/umurmur
%config(noreplace) /etc/umurmur.conf
# needed on el7+ using systemd
%dir /etc/tmpfiles.d
/etc/tmpfiles.d/%{name}.conf
/etc/systemd/system/umurmurd.service
%{_bindir}/umurmurd
/var/run/%{name}

%changelog
* Fri May 26 2023 Jim Gorz <nrezinorn@gmail.com> - 0.2.20
- Latest Release on el7+

* Sun Dec 13 2015 Jim Gorz <nrezinorn@gmail.com> - 0.2.16a
- Latest Source Build
