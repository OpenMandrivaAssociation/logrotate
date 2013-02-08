Summary:	Rotates, compresses, removes and mails system log files
Name:		logrotate
Version:	3.7.9
Release:	7
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
Patch10:	logrotate-3.7.9-address-parsing.patch
Patch11:	logrotate-3.7.9-support-no-acls.patch
Patch100:	logrotate-3.7.9-fix-format-errrors.patch
Patch101:	logrotate-3.7.9-third_arg_fix.diff
# ease upgrade regarding #20745
Conflicts:	sysklogd < 1.4.2
Conflicts:	syslog-ng < 1.6.9-1mdk 
BuildRequires:	popt-devel
BuildRequires:	acl-devel
Requires(post):	coreutils

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
%patch10
%patch11

%patch100 -p0
%patch101 -p0

%build
%make RPM_OPT_FLAGS="%{optflags} -Dasprintf=asprintf" WITH_SELINUX=no WITH_ACL=yes LDFLAGS="%{ldflags}"
#make test

%install
%{make} PREFIX=%{buildroot} MANDIR=%{_mandir} install

mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.daily/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}.d

%post
if [ $1 = 1 ]; then
    # installation
    /bin/touch %{_var}/lib/logrotate.status
fi

%files
%doc CHANGES COPYING examples README*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/cron.daily/%{name}
%{_sysconfdir}/%{name}.d
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%{_mandir}/man5/%{name}.conf.5*


%changelog
* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 3.7.9-4mdv2011.0
+ Revision: 686244
- fix build (pcpa)
- sync with logrotate-3.7.9-11.fc16.src.rpm
- mass rebuild
- get rid of ^M's in the redhat patches

* Mon Apr 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3.7.9-2
+ Revision: 650202
- fix build
- sync with fedora (fixes CVE-2011-1154,1155,1098)

* Sat Aug 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.9-1mdv2011.0
+ Revision: 569590
- new version

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - revert last commit, such changes must be discussed with the maintainer first
      and should never happen so late in the release cycle

* Wed Jun 09 2010 Raphaël Gertz <rapsys@mandriva.org> 3.7.8-5mdv2010.1
+ Revision: 547299
- Add ccp config merge

* Mon Apr 12 2010 Eugeni Dodonov <eugeni@mandriva.com> 3.7.8-4mdv2010.1
+ Revision: 533703
- Do not create initial files as root (#57807).

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.7.8-3mdv2010.1
+ Revision: 520147
- rebuilt for 2010.1

  + Eugeni Dodonov <eugeni@mandriva.com>
    - Improve initial config according to #57807.

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.7.8-2mdv2010.0
+ Revision: 426003
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.8-1mdv2009.1
+ Revision: 354879
- new version

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 3.7.7-1mdv2009.1
+ Revision: 316246
- 3.7.7 (fedora sync)
- use LDFLAGS from the %%configure macro

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 3.7.5-9mdv2009.0
+ Revision: 223126
- rebuild

* Mon Mar 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.5-8mdv2008.1
+ Revision: 189740
- more verbose error message in logs (fix #36904)

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 3.7.5-7mdv2008.1
+ Revision: 152866
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jul 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.5-5mdv2008.0
+ Revision: 53701
- don't rotate lastlog (fix #15160)

* Thu Jun 28 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.5-4mdv2008.0
+ Revision: 45557
- minor spec and config file edits for consistency with sysklogd
- bump conflict on sysklogd to help upgrade

* Mon Jun 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.7.5-3mdv2008.0
+ Revision: 40897
- don't ship data file, but create it with empty content on %%post
- spec cleanup
- don't ship syslog logrotate configuration


* Sat Mar 31 2007 Gustavo De Nardin <gustavodn@mandriva.com> 3.7.5-2mdv2007.1
+ Revision: 150121
- added patch logrotate-stop_on_script_errors.patch: makes logrotate stop
  processing logs when scripts exit with error, fixes #29979
- added patch logrotate-run_scripts_with_arg0.patch: runs scripts passing a simple
  fixed $0 for error messages and such

* Thu Mar 08 2007 David Walluck <walluck@mandriva.org> 3.7.5-1mdv2007.1
+ Revision: 134942
- 3.7.5

  + Warly <warly@mandriva.com>
    - fix permission on /etc/logrotate.d/syslog
    - uncompresse extra sources; fix bug 12557

* Mon Nov 20 2006 Oden Eriksson <oeriksson@mandriva.com> 3.7.3-4mdv2007.1
+ Revision: 85708
- Import logrotate

* Tue May 23 2006 Pixel <pixel@mandriva.com> 3.7.3-4mdk
- use the proper package name for the conflict on sysklogd

* Mon Jan 30 2006 Michael Scherer <misc@mandriva.org> 3.7.3-3mdk
- use the proper version for the conflict, thanks blino for spotting this

* Fri Jan 27 2006 Michael Scherer <misc@mandriva.org> 3.7.3-2mdk
- add a syslog logrotate config files, to close #20745

* Thu Dec 29 2005 Oden Eriksson <oeriksson@mandriva.com> 3.7.3-1mdk
- sync with fedora (3.7.3-2.1)
- spec file massage
- drop upstream patches, reorder patches, rediff P0
- run the test suite

* Mon Mar 14 2005 Frederic Lepied <flepied@mandrakesoft.com> 3.7.1-2mdk
- sync with 3.7.1-7
- fix snort log rotating problem (bug #13731)

* Fri Dec 03 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.7.1-1mdk
- 3.7.1

* Thu May 13 2004 Michael Scherer <misc@mandrake.org> 3.7-1mdk
- New release 3.7

