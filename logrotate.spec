Summary:	Rotates, compresses, removes and mails system log files
Name:		logrotate
Version:	3.8.7
Release:	5
License:	GPLv2+
Group:		File tools
Url:		https://fedorahosted.org/logrotate/
Source0:	https://fedorahosted.org/releases/l/o/logrotate/%{name}-%{version}.tar.gz
Source1:	logrotate.conf
Source2:	logrotate.cron
BuildRequires:	acl-devel
BuildRequires:	pkgconfig(popt)
# ease upgrade regarding #20745
Conflicts:	sysklogd < 1.4.2

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%setup -q

%build
%make RPM_OPT_FLAGS="%{optflags} -Dasprintf=asprintf" WITH_SELINUX=no WITH_ACL=yes LDFLAGS="%{ldflags}"

%check
make test

%install
make PREFIX=%{buildroot} MANDIR=%{_mandir} install

install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -m755 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/cron.daily/%{name}
install -d -m755 %{buildroot}%{_sysconfdir}/%{name}.d

install -d %{buildroot}%{_localstatedir}/lib
touch %{buildroot}%{_localstatedir}/lib/logrotate.status

%files
%doc CHANGES examples README*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/cron.daily/%{name}
%{_sysconfdir}/%{name}.d
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%{_mandir}/man5/%{name}.conf.5*
%verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/logrotate.status
