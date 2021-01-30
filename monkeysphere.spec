Name: monkeysphere
Summary: Use the OpenPGP web of trust to verify SSH connections
Version: 0.44
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Internet
URL: http://web.monkeysphere.info/

Source: http://archive.monkeysphere.info/debian/pool/%{name}/m/%{name}/%{name}_%{version}.orig.tar.gz

BuildArch: x86_64

Requires(pre): shadow-utils
Requires: gnupg
Requires: openssh-clients
Requires: perl
Requires: libgcrypt
Requires: libbassuan
BuildRequires: gcc
BuildRequires: libgcrypt-devel
BuildRequires: libassuan-devel


%description
SSH key-based authentication is tried-and-true, but it lacks a true
Public Key Infrastructure for key certification, revocation and
expiration.  Monkeysphere is a framework that uses the OpenPGP web of
trust for these PKI functions.  It can be used in both directions: for
users to get validated host keys, and for hosts to authenticate users.


%prep
%setup -q


%build
%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_var}/lib/%{name}/authorized_keys
rm -r %{buildroot}%{_datadir}/%{name}/transitions/
chmod -cR 0644 %{buildroot}%{_mandir}/*/*
chmod -cR 0644 src/transitions/*
chmod -cR 0755 %{buildroot}%{_var}/lib/%{name}/


%clean
rm -rf %{buildroot}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_var}/lib/%{name} -s /sbin/nologin \
    -c "Monkeysphere authentication user" %{name}
exit 0


%files
%defattr(-,root,root,-)
%doc COPYING README Changelog src/transitions/
%doc %{_docdir}/%{name}/Changelog
%doc %{_docdir}/%{name}/examples/crontab
%doc %{_docdir}/%{name}/examples/ssh_config
%doc %{_docdir}/%{name}/examples/sshd_config
%doc %{_docdir}/%{name}/examples/make-x509-certreqs
%doc %{_docdir}/%{name}/examples/monkeysphere-monitor-keys

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-authentication.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-host.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/openpgp2ssh
%{_bindir}/pem2openpgp
%{_bindir}/agent-transfer
%{_bindir}/openpgp2pem
%{_bindir}/openpgp2spki
%{_sbindir}/%{name}-authentication
%{_sbindir}/%{name}-host

%{_datadir}/%{name}/VERSION
%{_datadir}/%{name}/common
%{_datadir}/%{name}/defaultenv
%{_datadir}/%{name}/keytrans
%{_datadir}/%{name}/%{name}-authentication-keys-for-user
%{_datadir}/%{name}/m
%{_datadir}/%{name}/ma
%{_datadir}/%{name}/mh

%{_mandir}/*/*

%attr(-,%{name},%{name}) %dir %{_var}/lib/%{name}
%attr(-,%{name},%{name}) %dir %{_var}/lib/%{name}/authorized_keys


%changelog
* Sat Jan 30 2021 Akos Balla <akos.balla@sirc.hu> - 0.44-1
- Create RPM package for 0.44

* Tue May 03 2011 Bernie Innocenti <bernie@codewiz.org> - 0.35-2
- Fix permissions on manpages
- Remove BuildRoot

* Tue May  3 2011 Michal Nowak <mnowak@redhat.com> - 0.35-1
- 0.35 bump
- guidelines fixes

* Sun Sep 12 2010 Bernie Innocenti <bernie@codewiz.org> - 0.31-2
- Fix problems identified by reviewer

* Sun Sep 12 2010 Bernie Innocenti <bernie@codewiz.org> - 0.31-1
- Update to 0.31

* Thu Apr 01 2010 Bernie Innocenti <bernie@codewiz.org> - 0.28-4
- Add /var/lib/monkeysphere/authorized_keys

* Tue Mar 30 2010 Bernie Innocenti <bernie@codewiz.org> - 0.28-3
- Give a real shell to monkeysphere user.
- Simplify pre/postun macros.

* Tue Mar 30 2010 Bernie Innocenti <bernie@codewiz.org> - 0.28-2
- Create user monkeysphere on installation.

* Tue Mar 30 2010 Bernie Innocenti <bernie@codewiz.org> - 0.28-1
- Update to 0.28.
- Various fixes for Fedora.

* Sat Nov 22 2008 Anonymous Coward <anonymous@example.com> - 0.22
- Initial release.
