License:        BSD
Vendor:         Otus
Group:          PD01
URL:            http://otus.ru/lessons/3/
Source0:        otus-%{current_datetime}.tar.gz
BuildRoot:      %{_tmppath}/otus-%{current_datetime}
Name:           ip2w
Version:        0.0.1
Release:        1
BuildArch:      noarch
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires: uwsgi
Summary:  simple uwsgi daemon


%description
Git version: %{git_version} (branch: %{git_branch})

%define __etcdir    /usr/local/etc/%{name}
%define __logdir    /var/log/%{name}
%define __bindir    /usr/local/%{name}
%define __systemddir	/usr/lib/systemd/system

%prep
tar xf %{SOURCE0} --strip 1

%install
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}
%{__mkdir} -p %{buildroot}/%{__systemddir}
%{__mkdir} -p %{buildroot}/%{__logdir}
%{__mkdir} -p %{buildroot}/%{__etcdir}
%{__mkdir} -p %{buildroot}/%{__bindir}
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.service %{buildroot}/%{__systemddir}/%{name}.service

%post
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}


%files
%{__logdir}
%{__bindir}
%{__systemddir}
