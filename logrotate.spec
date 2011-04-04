Summary:	Rotates, compresses, removes and mails system log files
Name:		logrotate
Version:	3.7.9
Release:	%mkrel 2
License:	GPL
Group:		File tools
URL:		https://fedorahosted.org/logrotate/
Source0:	https://fedorahosted.org/releases/l/o/logrotate/%{name}-%{version}.tar.gz
Source1:	logrotate.conf
Source2:	logrotate.cron
Patch1:		logrotate-3.7.8-man-authors.patch
Patch2:		logrotate-3.7.9-man-size.patch
Patch3:		logrotate-3.7.9-man-page.patch
Patch4:		logrotate-3.7.9-config.patch
Patch5:		logrotate-3.7.9-acl.patch
Patch6:		logrotate-3.7.9-tabooext.patch
Patch7:		logrotate-3.7.9-shred.patch
Patch8:		logrotate-3.7.9-statefile.patch
Patch9:		logrotate-3.7.9-atomic-create.patch 
Patch100:	logrotate-3.7.9-fix-format-errrors.patch
Patch101:	logrotate-3.7.9-third_arg_fix.diff
# ease upgrade regarding #20745
Conflicts:	sysklogd < 1.4.2
Conflicts:	syslog-ng < 1.6.9-1mdk 
BuildRequires:	popt-devel
BuildRequires:	acl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch1 -p2
%patch2
%patch3 -p1
%patch4
%patch5 -p2
%patch6 -p1
%patch7
%patch8
%patch9 -p1

%patch100 -p0
%patch101 -p0

%build
%make RPM_OPT_FLAGS="%{optflags}" WITH_SELINUX=no WITH_ACL=yes LDFLAGS="%{ldflags}"
#make test

%install
%{__rm} -rf %{buildroot}

%{make} PREFIX=%{buildroot} MANDIR=%{_mandir} install

%{__mkdir_p} %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

%{__mkdir_p} %{buildroot}%{_sysconfdir}/cron.daily
%{__install} -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.daily/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}.d

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 = 1 ]; then
    # installation
    /bin/touch %{_var}/lib/logrotate.status
fi

%files
%defattr(-,root,root)
%doc CHANGES COPYING examples README*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/cron.daily/%{name}
%{_sysconfdir}/%{name}.d
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%{_mandir}/man5/%{name}.conf.5*
