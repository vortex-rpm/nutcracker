Summary:	fast and lightweight proxy for memcached and redis protocol
Name:		nutcracker
Version:	0.4.1
Release:	1.vortex%{?dist}
Vendor:		Vortex RPM
License:	Apache License 2.0
Group:		Applications/System
URL:		https://github.com/twitter/twemproxy
Source0:	%{name}-%{version}.tar.gz
BuildRequires:  autoconf, automake, libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and
lightweight proxy for memcached and redis protocol. It was primarily
built to reduce the connection count on the backend caching servers.
This, together with protocol pipelining and sharding enables you to
horizontally scale your distributed caching architecture.

%prep
%setup -q -n %{name}-%{version}
%if 0%{?rhel} >= 6
sed -i 's/2.64/2.63/g' configure.ac
%endif
autoreconf -fvi

%build

%install
rm -rf %{buildroot}
%{__install} -p -D -m 0755 scripts/%{name}.init %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 conf/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} >= 6
/usr/sbin/nutcracker
%else
/usr/bin/nutcracker
%endif
%{_initrddir}/%{name}
%{_mandir}/man8/nutcracker.8.gz
%config(noreplace)%{_sysconfdir}/%{name}/%{name}.yml
%doc LICENSE ChangeLog README.md NOTICE

%changelog
* Fri Apr 29 2016 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 0.4.1-1.vortex
- Initial packaging based on tarballed spec.
