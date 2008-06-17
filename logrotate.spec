Name:           logrotate
Version:        3.7.5
Release:        %mkrel 9
Summary:        Rotates, compresses, removes and mails system log files
License:        GPL
Group:          File tools
URL:            http://download.fedora.redhat.com/pub/fedora/linux/core/development/source/SRPMS/
Source0:        %{name}-%{version}.tar.gz
Source1:        logrotate.conf
Source2:        logrotate.cron
Patch0:         logrotate-stop_on_script_errors.patch
Patch1:         logrotate-run_scripts_with_arg0.patch
# ease upgrade regarding #20745
Conflicts:      sysklogd < 1.4.2
Conflicts:      syslog-ng < 1.6.9-1mdk 
BuildRequires:  popt-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

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
%patch0 -p1 -b .stop_on_script_errors
%patch1 -p1 -b .run_scripts_with_arg0

%build
%{make} RPM_OPT_FLAGS="%{optflags}" WITH_SELINUX=no
%{make} test

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
