Summary:	Rotates, compresses, removes and mails system log files
Name:		logrotate
Version:	3.19.0
Release:	1
License:	GPLv2+
Group:		File tools
Url:		https://github.com/logrotate/logrotate
Source0:	https://github.com/logrotate/logrotate/releases/download/%{version}/logrotate-%{version}.tar.xz
Source1:	rwtab

BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(popt)
BuildRequires:	systemd-rpm-macros
Requires:	zstd

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
%autosetup -p1

autoreconf -fi

%build
%configure \
	--with-acl \
	--with-state-file-path=%{_localstatedir}/lib/logrotate/logrotate.status \
	--with-compress-command="%{_bindir}/zstd" \
	--with-uncompress-command="%{_bindir}/unzstd" \
	--with-compress-extension=".zst"

%make_build

%check
make test

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_localstatedir}/lib/logrotate

install -p -m 644 examples/logrotate.conf %{buildroot}%{_sysconfdir}/
install -p -m 644 examples/{b,w}tmp %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 644 examples/logrotate.{service,timer} %{buildroot}%{_unitdir}/

# Make sure logrotate is able to run on read-only root
mkdir -p %{buildroot}%{_sysconfdir}/rwtab.d
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rwtab.d/logrotate

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.timer
EOF

%pre
# If /var/lib/logrotate/logrotate.status does not exist, create it and copy
# the /var/lib/logrotate.status in it (if it exists). We have to do that in pre
# script, otherwise the /var/lib/logrotate/logrotate.status would not be there,
# because during the update, it is removed/renamed.
if [ ! -d %{_localstatedir}/lib/logrotate/ ] && [ -f %{_localstatedir}/lib/logrotate.status ]; then
    mkdir -p %{_localstatedir}/lib/logrotate
    cp -a %{_localstatedir}/lib/logrotate.status %{_localstatedir}/lib/logrotate
fi

%post
%systemd_post %{name}.timer

%preun
%systemd_preun %{name}.timer

%files
%doc examples README*
%{_sbindir}/logrotate
%{_presetdir}/86-%{name}.preset
%{_unitdir}/logrotate.{service,timer}
%{_mandir}/man8/logrotate.8*
%{_mandir}/man5/logrotate.conf.5*
%config(noreplace) %{_sysconfdir}/logrotate.conf
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/{b,w}tmp
%dir %{_localstatedir}/lib/logrotate
%ghost %verify(not size md5 mtime) %attr(0644, root, root) %{_localstatedir}/lib/logrotate/logrotate.status
%config(noreplace) %{_sysconfdir}/rwtab.d/logrotate
