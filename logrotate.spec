Name:           logrotate
Version:        3.7.7
Release:        %mkrel 1
Summary:        Rotates, compresses, removes and mails system log files
License:        GPL
Group:          File tools
URL:		ftp://ftp.uninett.no/pub/linux/Fedora/development/source/SRPMS
Source0:        %{name}-%{version}.tar.gz
Source1:        logrotate.conf
Source2:        logrotate.cron
Patch0:		logrotate-3.7.7-curdir2.patch
Patch1:		logrotate-3.7.7-toolarge.patch
# ease upgrade regarding #20745
Conflicts:      sysklogd < 1.4.2
Conflicts:      syslog-ng < 1.6.9-1mdk 
BuildRequires:  popt-devel
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
%patch0 -p1 -b .curdir
%patch1 -p1 -b .toolarge

%build
export LDFLAGS="`rpm --eval %%configure|grep LDFLAGS|cut -d\\" -f2|sed -e 's/\$LDFLAGS\ //'`"

%make RPM_OPT_FLAGS="%{optflags}" WITH_SELINUX=no LDFLAGS="$LDFLAGS"
%make test

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
