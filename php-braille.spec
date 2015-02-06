%define modname braille
%define soname %{modname}.so
%define inifile A65_%{modname}.ini

Summary:	Functions to control a braille display (and keyboard), based on libbraille
Name:		php-%{modname}
Version:	0.1.1
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		http://libbraille.org
Source0:	http://php-baustelle.de/%{modname}-%{version}.tgz
Patch0:		braille-0.1.1-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRequires:	libbraille-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Functions to control a braille display (and keyboard), based on libbraille.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS EXPERIMENTAL package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2012.0
+ Revision: 806421
- fix build
- 0.1.1
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-22
+ Revision: 761204
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-21
+ Revision: 696397
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-20
+ Revision: 695370
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-19
+ Revision: 646616
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-18mdv2011.0
+ Revision: 629769
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-17mdv2011.0
+ Revision: 628071
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-16mdv2011.0
+ Revision: 600465
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-15mdv2011.0
+ Revision: 588747
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-14mdv2010.1
+ Revision: 514521
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-13mdv2010.1
+ Revision: 485343
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-12mdv2010.1
+ Revision: 468148
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-11mdv2010.0
+ Revision: 451256
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1.0-10mdv2010.0
+ Revision: 397269
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2010.0
+ Revision: 376976
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2009.1
+ Revision: 346398
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2009.1
+ Revision: 341711
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2009.1
+ Revision: 321706
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2009.1
+ Revision: 310252
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2009.0
+ Revision: 238378
- rebuild

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2008.1
+ Revision: 162213
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2008.1
+ Revision: 107607
- restart apache if needed

* Tue Sep 04 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2008.0
+ Revision: 79450
- Import php-braille



* Tue Sep 04 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2008.0
- initial Mandriva package
