License:        BSD
Vendor:         Otus
Group:          PD01
URL:            http://otus.ru/lessons/11/
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
Requires: python3 nginx uwsgi uwsgi-plugin-python36 uwsgi-logger-syslog uwsgi-plugin-common
Summary:  simple uwsgi daemon


%description
Git version: %{git_version} (branch: %{git_branch})

%define __etcdir    /usr/local/etc/%{name}
%define __logdir    /var/log/%{name}
%define __bindir    /usr/local/bin/%{name}
%define __systemddir	/usr/lib/systemd/system
%define __tmpfilesdir    /etc/tmpfiles.d
%define __rsyslog_conf_dir /etc/rsyslog.d
%define __nginx_conf_link /etc/nginx/default.d/ip2w.conf

%prep
tar xf %{SOURCE0} --strip 1

%install
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}
%{__mkdir} -p %{buildroot}/%{__systemddir}
%{__mkdir} -p %{buildroot}/%{__logdir}
%{__mkdir} -p %{buildroot}/%{__etcdir}
%{__mkdir} -p %{buildroot}/%{__bindir}
%{__mkdir} -p %{buildroot}/%{__tmpfilesdir}
%{__mkdir} -p %{buildroot}/%{__rsyslog_conf_dir}
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.systemd.service %{buildroot}/%{__systemddir}/%{name}.service
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.uwsgi.ini %{buildroot}/%{__etcdir}/uwsgi.ini
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.rsyslog.conf %{buildroot}/%{__rsyslog_conf_dir}/%{name}.conf
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.tmpfiles %{buildroot}/%{__tmpfilesdir}/%{name}.conf
%{__install} -pD -m 644 %{_builddir}/configs/%{name}.nginx.conf %{buildroot}/%{__etcdir}/nginx.conf
%{__install} -pD -m 644 %{_builddir}/src/app.py %{buildroot}/%{__bindir}/app.py

%post
%systemd_post %{name}.service
systemctl daemon-reload
systemd-tmpfiles --create
ln -sf %{__etcdir}/nginx.conf %{__nginx_conf_link}
nginx -t
id %{name} || useradd  %{name}
usermod nginx -aG %{name}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service
rm -f %{__nginx_conf_link}

%clean
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}


%files
%{__etcdir}
%{__logdir}
%{__bindir}
%{__systemddir}
%{__tmpfilesdir}
%{__rsyslog_conf_dir}
