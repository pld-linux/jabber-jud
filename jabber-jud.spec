Summary:	Jabber User Directory module
Summary(pl):	Modu³ rejestru u¿ytkowników dla systemu Jabber
Name:		jabber-jud
Version:	0.4
Release:	1
License:	distributable
Group:		Applications/Communications
Group(de):	Applikationen/Kommunikation
Group(pl):	Aplikacje/Komunikacja
Source0:	http://download.jabber.org/distd/1.4/final/jud-%{version}.tar.gz
Patch0:		%{name}-Makefile.patch
URL:		http://www.jabber.org/
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

install -d $RPM_BUILD_ROOT%{_libdir}/jabber
install jud.so $RPM_BUILD_ROOT%{_libdir}/jabber

gzip -9nf README 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/jabber/*
