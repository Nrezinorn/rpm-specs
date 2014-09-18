# No Debug pacakge
%define debug_package %{nil}

Name:  modsecurity-asl-rules		
Version: 1.0	
Release: 0%{?dist}
Summary: ASL Mod Security Rules
License: GPLv2
Source0: %{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)
#Requires: mod_security >= 2.7.9
Requires: mod_security >= 2.7.9, httpd

%description
Rulesets Provided by ASL

%prep
%setup -q -c 

%build

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/etc/httpd/
%{__mv} modsecurity.d %{buildroot}/etc/httpd/
%{__mkdir_p} %{buildroot}/etc/asl/
touch %{buildroot}/etc/asl/whitelist
touch %{buildroot}/etc/asl/custom-domain-blocks
%{__mkdir_p} %{buildroot}/var/asl
%{__mkdir_p} %{buildroot}/var/asl/tmp
%{__mkdir_p} %{buildroot}/var/asl/data
%{__mkdir_p} %{buildroot}/var/asl/data/msa
%{__mkdir_p} %{buildroot}/var/asl/data/audit
%{__mkdir_p} %{buildroot}/var/asl/data/suspicious


# Short circuit file lists to exclude a single file <3 
# this lops off the 2 top folders:  /etc/httpd and /etc/httpd/modsecurity.d
# ..there shouldn't ever be more..just a note if this ever fails.
find %{buildroot}/etc/httpd/ -print > ./filelist.txt
#scrub buildroot out of filelist
sed -i 's#%{buildroot}##' ./filelist.txt
# remove top dirs
sed -i -e '1,2d' ./filelist.txt
# Script tortix file from list
sed -i '/tortix_waf.conf/d' ./filelist.txt

%clean
rm -rf %{buildroot}

%files -f filelist.txt
%defattr(0770,root,apache,0770)
%dir /etc/asl
%dir /etc/httpd/modsecurity.d
%config(noreplace) /etc/asl/whitelist
%config(noreplace) /etc/asl/custom-domain-blocks
%dir /var/asl
%attr(770,apache,apache) /var/asl/tmp
%dir /var/asl/data
%attr(770,apache,apache) /var/asl/data/msa
%attr(770,apache,apache) /var/asl/data/audit
%attr(770,apache,apache) /var/asl/data/suspicious
%config(noreplace) /etc/httpd/modsecurity.d/tortix_waf.conf

%changelog
* Fri Sep 12 2014 - James Gorz <nrezinorn@gmail.com> - 1.0
- Initial build
