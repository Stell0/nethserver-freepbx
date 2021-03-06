Name: nethserver-freepbx
Version: 14.0.7
Release: 1%{?dist}
Summary: NethServer configuration for FreePBX
License: GPL
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: freepbx
Requires: nethserver-rh-php56-php-fpm
Requires: rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires: rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires: rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd
Requires: nethserver-mysql
Requires: nethserver-unixODBC

%description
nethserver-freepbx is the FreePBX configuration package for NethServer

%prep
%setup -q

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/httpd-fpbx

%post
%systemd_post httpd-admin.service asterisk.service

%preun
%systemd_preun httpd-admin.service asterisk.service

%postun
%systemd_postun


%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%dir %{_nseventsdir}/%{name}-update

%attr(0644,root,root) %config %{_sysconfdir}/httpd/fpbx-conf/httpd.conf
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd-fpbx
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-fpbx/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-fpbx/error_log
%config(noreplace) /etc/asterisk/acl.conf
%config(noreplace) /etc/asterisk/pjproject.conf
%config(noreplace) /etc/sysconfig/httpd-fpbx
%config /etc/dahdi/system.conf

%changelog
* Mon Jan 29 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.7-1
- nethserver-freepbx: LDAP users can't login to amp interface - Bug NethServer/dev#5369

* Thu Jan 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.6-1
- PBX: Asterisk logs aren't rotated - Bug NethServer/dev#5411
- PBX: /run/systemd/sessions is filled by sessions files in closing state - Bug NethServer/dev#5412

* Tue Jan 23 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.5-1
- FreePBX doesn't apply modifications to trusted networks - Bug NethServer/dev#5410

* Tue Jan 09 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.4-1
- nethserver-freepbx: backup restore fails - Bug NethServer/dev#5402

* Fri Nov 17 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.3-1
- Make sure Aterisk home directory exists - NethServer/nethserver-freepbx#35

* Wed Oct 25 2017 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.2-1
- Configure voicemail ODBC storage NethServer/dev#5363

* Fri Oct 20 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.1-1
- FreePBX user syncing fails on 7.4 with AD user provider - Bug NethServer/dev#5361

* Thu Aug 31 2017 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.0-1
- nethserver-freepbx first release

* Fri Jul 26 2016 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 0.0.1
- First implementation
