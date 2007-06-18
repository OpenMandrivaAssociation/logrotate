Name:           logrotate
Version:        3.7.5
Release:        %mkrel 3
Summary:        Rotates, compresses, removes and mails system log files
License:        GPL
Group:          File tools
URL:            http://download.fedora.redhat.com/pub/fedora/linux/core/development/source/SRPMS/
# The source for this package was pulled from cvs.
# Use the following commands to generate the tarball:
#  export CVSROOT=:pserver:anonymous@rhlinux.redhat.com:/usr/local/CVS
#  cvs login (hit return)
#  cvs co logrotate
#  cd logrotate
#  make create-archive
Source0:        ftp://ftp.redhat.com/pub/redhat/code/logrotate/%{name}-%{version}.tar.gz
Source1:        logrotate.conf.mdv
Patch0:         logrotate-stop_on_script_errors.patch
Patch1:         logrotate-run_scripts_with_arg0.patch
# ease upgrade regarding #20745
Conflicts:      sysklogd < 1.4.1-12mdk
Conflicts:      syslog-ng < 1.6.9-1mdk 
BuildRequires:  popt-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%{__cp} -a %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

%{__mkdir_p} %{buildroot}%{_sysconfdir}/cron.daily
%{__install} -m 0755 examples/%{name}.cron %{buildroot}%{_sysconfdir}/cron.daily/%{name}

%{__mkdir_p} %{buildroot}%{_var}/lib
/bin/touch %{buildroot}%{_var}/lib/logrotate.status

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}.d

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc CHANGES COPYING examples README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_sysconfdir}/cron.daily/%{name}
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}.d
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0644,root,root) %{_mandir}/man8/%{name}.8*
%attr(0644,root,root) %verify(not size md5 mtime) %config(noreplace) %{_var}/lib/logrotate.status
