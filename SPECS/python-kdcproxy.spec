%global realname kdcproxy

%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

%if 0%{?fedora} || 0%{?rhel} <= 7
%global with_python2 1
%else
%global with_python2 0
%endif

Name:           python-%{realname}
Version:        0.4
Release:        5%{?dist}
Summary:        MS-KKDCP (kerberos proxy) WSGI module

License:        MIT
URL:            https://github.com/npmccallum/%{realname}
Source0:        https://github.com/npmccallum/%{realname}/archive/%{realname}-%{version}.tar.gz

Patch0: Make-webtest-an-optional-dependency.patch
Patch1: Correct-addrs-sorting-to-be-by-TCP-UDP.patch
Patch2: Always-buffer-TCP-data-in-__handle_recv.patch

BuildArch:      noarch
BuildRequires:  git

%if 0%{?with_python2} > 0
BuildRequires:  python2-devel
BuildRequires:  python2-pytest
BuildRequires:  python2-coverage
BuildRequires:  python2-asn1crypto
BuildRequires:  python2-dns
BuildRequires:  python2-mock
%endif

%if 0%{?with_python3} > 0
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-coverage
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-dns
BuildRequires:  python3-mock
%endif


%description
This package contains a Python WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.

%if 0%{?with_python2} > 0
%package -n python2-%{realname}
Summary:        MS-KKDCP (kerberos proxy) WSGI module
Requires:       python2-dns
Requires:       python2-asn1crypto

%{?python_provide:%python_provide python2-%{realname}}

%description -n python2-%{realname}
This package contains a Python 2.x WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.
%endif

%if 0%{?with_python3} > 0
%package -n python3-%{realname}
Summary:        MS-KKDCP (kerberos proxy) WSGI module
Requires:       python3-dns
Requires:       python3-asn1crypto

%{?python_provide:%python_provide python3-%{realname}}

%description -n python3-%{realname}
This package contains a Python 3.x WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.
%endif

%prep
%autosetup -S git -n %{realname}-%{version}


%build
%if 0%{?with_python2} > 0
%py2_build
%endif
%if 0%{?with_python3} > 0
%py3_build
%endif

%install
%if 0%{?with_python2} > 0
%py2_install
%endif
%if 0%{?with_python3} > 0
%py3_install
%endif

%check
%if 0%{?with_python2} > 0
KDCPROXY_ASN1MOD=asn1crypto %{__python2} -m pytest
%endif
%if 0%{?with_python3} > 0
KDCPROXY_ASN1MOD=asn1crypto %{__python3} -m pytest
%endif

%if 0%{?with_python2} > 0
%files -n python2-%{realname}
%doc README
%license COPYING
%{python2_sitelib}/%{realname}/
%{python2_sitelib}/%{realname}-%{version}-*.egg-info
%endif

%if 0%{?with_python3} > 0
%files -n python3-%{realname}
%doc README
%license COPYING
%{python3_sitelib}/%{realname}/
%{python3_sitelib}/%{realname}-%{version}-*.egg-info
%endif

%changelog
* Fri Oct 25 2019 Robbie Harwood <rharwood@redhat.com> - 0.4-5
- Always buffer TCP data in __handle_recv()
- Resolves: #1747144

* Fri Oct 25 2019 Robbie Harwood <rharwood@redhat.com> - 0.4-4
- Correct addrs sorting to be by TCP/UDP
- Resolves: #1732898

* Mon Nov 19 2018 Thomas Woerner <twoerner@redhat.com> - 0.4-3
- Bump release to be able to add python-kdcpoxy to the idm module
  Resolves: RHBZ#1639332

* Thu Aug 09 2018 Robbie Harwood <rharwood@redhat.com> - 0.4-2
- Update dependencies in test suite

* Thu Aug 09 2018 Robbie Harwood <rharwood@redhat.com> - 0.4-1
- New upstream release - 0.4
- Port to autosetup

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-13
- Rebuilt for Python 3.7

* Thu Mar 22 2018 Troy Dawson <tdawson@redhat.com> - 0.3.2-12
- Update conditionals.
- Make preperations for non-python2 builds

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.2-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 05 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.3.2-9
- Ignore test results

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.3.2-6
- Fix failing tests
- Modernize the SPEC file

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-5
- Rebuild for Python 3.6
- BR /usr/bin/tox instead of python-tox
- Use %%{python3_version_nodots} instead of hardcoded 35

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug 03 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2
- Fixes CVE-2015-5159

* Wed Jul 22 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3-1
- Update to 0.3
- Run tests in Fedora (not RHEL due to python-tox)

* Fri Oct 24 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Thu Oct 23 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2-1
- Update to 0.2
- Fix EPEL7 build

* Tue Jan 21 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.1.1-1
- Initial package
