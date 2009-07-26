Name:           primer3
Version:        1.1.4
Release:        7%{?dist}
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
%setup -q -c -n %{name}

cp -p README.txt readme.txt.noutf8

iconv -f ISO-8859-1 -t UTF-8 -o README.txt.tmp README.txt
mv README.txt.tmp README.txt

touch -r readme.txt.noutf8 README.txt
rm readme.txt.noutf8

sed -i -e 's|CFLAGS  = $(CC_OPTS) $(O_OPTS)|CFLAGS  = $(CC_OPTS) $(O_OPTS) $(INIT_CFLAGS)|' src/Makefile

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

%check
pushd src
 %{?_with_tests:make test}
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt COPYING.txt how-to-cite.txt example 
%doc src/gpl-2.0.txt src/release_notes.txt
%{_bindir}/%{name}_core
%{_bindir}/oligotm
%{_bindir}/ntdpal

%changelog
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

