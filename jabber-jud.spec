Summary:	Jabber User Directory module
Summary(pl):	Modu³ rejestru u¿ytkowników dla systemu Jabber
Name:		jabber-jud
Version:	0.4
Release:	1
License:	distributable
Group:		Applications/Communications
Group(de):	Applikationen/Kommunikation
Group(pl):	Aplikacje/Komunikacja
Source0:	http://download.jabber.org/dists/1.4/final/jud-%{version}.tar.gz
Source1:	jud.xml
Patch0:		%{name}-Makefile.patch
URL:		http://www.jabber.org/
BuildRequires:	jabber-devel
Requires:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is User Directory module for Jabber. 

%description -l pl
Modu³ ten umo¿liwia rejestrowanie i przeszukiwanie danych o u¿ytkownikach
systemu Jabber.

%prep
%setup -qn jud-%{version}
%patch0 -p1

%build
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{_sysconfdir}}/jabberd
install jud.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabberd

gzip -9nf README 

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -r /var/lock/subsys/jabberd ]; then
	if [ -r /var/lock/subsys/jabber-jud ]; then
        	/etc/rc.d/init.d/jabberd restart jud >&2
	else
        	echo "Run \"/etc/rc.d/init.d/jabberd start jud\" to start JUD."
	fi
else
        echo "Run \"/etc/rc.d/init.d/jabberd start\" to start Jabber server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-jud ]; then
		/etc/rc.d/init.d/jabberd stop jud >&2
	fi
fi


%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/jabberd/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabberd/*
