Summary:	Jabber User Directory module
Summary(pl):	Modu³ rejestru u¿ytkowników dla systemu Jabber
Name:		jabber-jud
Version:	0.4
Release:	3
License:	distributable
Group:		Applications/Communications
Source0:	http://download.jabber.org/dists/1.4/final/jud-%{version}.tar.gz
# Source0-md5:	a057e8dd5966fa0d26ded03697ba395a
Source1:	jud.xml
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-Makefile.patch
URL:		http://www.jabber.org/
BuildRequires:	jabberd14-devel >= 1.4.3.1-2
%requires_eq	jabberd14
Requires(post):	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is User Directory module for Jabber.

%description -l pl
Modu³ ten umo¿liwia rejestrowanie i przeszukiwanie danych o
u¿ytkownikach systemu Jabber.

%prep
%setup -qn jud-%{version}
%patch0 -p1

%build
%{__make} \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd14,%{_sysconfdir}/jabber} \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install jud.so $RPM_BUILD_ROOT%{_libdir}/jabberd14
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber
ln -s %{_sbindir}/jabberd14 $RPM_BUILD_ROOT%{_sbindir}/jabber-jud
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-jud
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-jud

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in the config file..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/jud.xml
	fi
fi

if [ -r /var/lock/subsys/jabber-jud ]; then
	/etc/rc.d/init.d/jabber-jud restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-jud start\" to start Jabber mu-conference service."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-jud ]; then
		/etc/rc.d/init.d/jabber-jud stop >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/jabberd14/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-jud
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jabber-jud
