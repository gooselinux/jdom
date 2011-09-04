# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           jdom
Version:        1.1.1
Release:        1%{?dist}
Epoch:          0
Summary:        Java alternative to DOM and SAX
License:        BSD
URL:            http://www.jdom.org/
Group:          Development/Libraries
# http://www.jdom.org/dist/source/jdom-1.1.1.tar.gz
# All jars have been removed to form RHCLEAN version
Source0:        jdom-1.1.1-RHCLEAN.tar.bz2
Patch0:         %{name}-crosslink.patch
Patch1:         %{name}-%{version}-OSGiManifest.patch
Requires:       xalan-j2 >= 0:2.2.0
BuildRequires:  ant >= 0:1.6
BuildRequires:  xalan-j2 >= 0:2.2.0
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-javadoc
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is a
lightweight and fast, and is optimized for the Java programmer. It's an
alternative to DOM and SAX, although it integrates well with both DOM
and SAX.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath xalan-j2)
sed -e 's|<property name="build.compiler".*||' build.xml > tempf; cp tempf build.xml; rm tempf
ant -Dj2se.apidoc=%{_javadocdir}/java package javadoc-link


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt COMMITTERS.txt LICENSE.txt README.txt TODO.txt
%{_javadir}/%{name}*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}


%changelog
* Tue Mar 16 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:1.1.1-1
- Resolves: #574067
- Rebase to 1.1.1.
- Remove gcj support.
- Fix license to be BSD.

* Tue Feb 02 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:1.0-7.8
- Fix javadoc subpackage to not use post and postun steps using rm

* Fri Jan 08 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:1.0-7.7
- Resolves: #553816
- Fix license of spec file and fix rpmlint warnings.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.0-7.6
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-7.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-6.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Andrew Overholt <overholt@redhat.com> 1.0-5.5
- Add OSGi manifest information

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-5.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-5jpp.3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0-5jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.0-4jpp.2
- Add %%{?dist} as per policy

* Fri Aug 04 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-4jpp.1
- Added missing requirements.
- Remove jaxen requirement, since we don't have it in fc yet.
- Merge with fc spec.

* Tue Apr 11 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-3jpp
- First JPP-1.7 release
- Drop false xalan dependency

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-2jpp
- Add jaxen to Requires and classpath

* Sat Sep 18 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- Upgrade to 1.0 final

* Tue Sep 07 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.rc1.1jpp
- Upgrade to 1.0-rc1

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0-0.b9.4jpp
- Rebuild with ant-1.6.2

* Mon Jul 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.b9.3jpp
- Add non-versioned javadoc dir symlink.
- Crosslink with local J2SE javadocs.

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.0-0.b9.2jpp
- fix URL

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.0-0.b9.1jpp
- b9
- don't use classic compiler

* Thu Mar 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.b8.2jpp
- Adapted to JPackage 1.5.
- Use sed instead of bash 2 extension when symlinking jars during build.

* Wed May 08 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b8.1jpp
- vendor, distribution, group tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b7.6jpp
- versioned dir for javadoc
- requires xalan-j2 >= 2.2.0
- no dependencies for javadoc package
- stricter dependency for demo package
- section macro

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b7.5jpp
- javadoc into javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.0-0.b7.4jpp
- removed packager tag
- new jpp extension
- added xalan 2.2.D13 support

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b7.3jpp
- used original tarball

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b7.2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b7.1mdk
- Requires and BuildRequires xalan-j2
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- added demo package

*  Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.0b6-1mdk
- first Mandrake release
