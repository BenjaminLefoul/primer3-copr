Name:           primer3
Version:        2.3.4
Release:        2%{?dist}
Summary:        PCR primer design tool

Group:          Applications/Productivity
License:        BSD and GPLv2+
URL:            http://primer3.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Primer3 is a widely used program for designing PCR primers (PCR = 
"Polymerase Chain Reaction"). PCR is an essential and ubiquitous 
tool in genetics and molecular biology. Primer3 can also design 
hybridization probes and sequencing primers.

PCR is used for many different goals. Consequently, primer3 has 
many different input parameters that you control and that tell 
primer3 exactly what characteristics make good primers for your goals.


%prep
%setup -q  -n %{name}-%{version}

chmod -x src/*
chmod +x src/primer3_config # causes permissions issue if removed
sed -i -e 's|CFLAGS  = $(CC_OPTS) $(O_OPTS)|CFLAGS  = $(CC_OPTS) $(O_OPTS) $(INIT_CFLAGS)|' src/Makefile
sed -i 's/\r//' primer3web_v0_4_0_default_settings.txt

sed -i -e 's|/opt/primer3_config|/etc/primer3_config|' src/release_notes.txt src/thal_main.c src/primer3_boulder_main.c primer3_manual.htm

%build
cd src

export INIT_CFLAGS="%{optflags}" 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 src/%{name}_core $RPM_BUILD_ROOT%{_bindir}/%{name}_core
install -p -m 0755 src/oligotm $RPM_BUILD_ROOT%{_bindir}/oligotm
install -p -m 0755 src/ntdpal $RPM_BUILD_ROOT%{_bindir}/ntdpal

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/primer3_config
cp -r src/primer3_config $RPM_BUILD_ROOT%{_sysconfdir}/


%check
pushd src
 %{?_with_tests:make test}
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#%doc README.txt COPYING.txt how-to-cite.txt example 
%doc COPYING.txt example primer3_manual.htm
%doc *settings.txt
%doc src/gpl-2.0.txt src/release_notes.txt
%{_bindir}/%{name}_core
%{_bindir}/oligotm
%{_bindir}/ntdpal
%{_sysconfdir}/primer3_config

%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3.4-1
- Update to 2.3.4

* Tue Mar 27 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3.2-2
- Include the primer3_config folder RHBZ#821501
- Move primer3_config from /opt/ where upstream wants it to /etc where I want it

* Tue Mar 27 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3.2-1
- Update to release 2.3.2

* Wed Feb 22 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3.0-1
- Update to release 2.3.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 pingou <pingou@pingoured.fr> - 2.2.3-1
- Update to 2.2.3
- Fix permission issue

* Sat Apr 24 2010 pingou <pingou@pingoured.fr> - 2.2.2-pre1
- Build version 2.2.2 beta

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 06 2008 pingou <pingoufc4@yahoo.fr> 1.1.4-5
- Remove headers, not needed

* Tue Aug 12 2008 pingou <pingoufc4@yahoo.fr> 1.1.4-4
- Change the check section to use conditionnality --with tests runs the test
-  defaults does not

* Mon Aug 11 2008 pingou <pingoufc4@yahoo.fr> 1.1.4-3
- Move the export to the build section
- Move the make test to the check section
- Set the binaries perms to 755

* Wed Aug 06 2008 pingou <pingoufc4@yahoo.fr> 1.1.4-2
- Keep the timestamp in the README.txt
- Change the CFLAG for the compilation
- Remove BR perl

* Thu Jul 24 2008 pingou <pingoufc4@yahoo.fr> 1.1.4-1
- First build for Fedora

