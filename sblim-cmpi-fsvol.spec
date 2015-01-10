Summary:	SBLIM CMPI FSVOL instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe FSVOL dla SBLIM CMPI
Name:		sblim-cmpi-fsvol
Version:	1.5.1
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	18bbf88b4607091526106f2bb33a384a
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI File System and Storage Volume providers.

%description -l pl.UTF-8
Dostawcy informacji z systemu plików i wolumenów dyskowych dla SBLIM
CMPI.

%package libs
Summary:	SBLIM FSVOL instrumentation library
Summary(pl.UTF-8):	Biblioteka pomiarowa SBLIM FSVOL
Group:		Libraries

%description libs
SBLIM FSVOL instrumentation library.

%description libs -l pl.UTF-8
Biblioteka pomiarowa SBLIM FSVOL.

%package devel
Summary:	Header files for SBLIM FSVOL instrumentation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pomiarowej SBLIM FSVOL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for SBLIM FSVOL instrumentation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pomiarowej SBLIM FSVOL.

%package static
Summary:	Static SBLIM FSVOL instrumentation library
Summary(pl.UTF-8):	Statyczna biblioteka pomiarowa SBLIM FSVOL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SBLIM FSVOL instrumentation library.

%description static -l pl.UTF-8
Statyczna biblioteka pomiarowa SBLIM FSVOL.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.{la,a}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_Fsvol.registration \
	-m %{_datadir}/%{name}/Linux_Fsvol.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_Fsvol.registration \
		-m %{_datadir}/%{name}/Linux_Fsvol.mof >/dev/null
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README README.TEST
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_BlockStorageStatisticalDataProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_BootOSFromFSProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_HostedFileSystemProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_LocalFileSystemProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_NFSProvider.so
%dir %{_datadir}/sblim-cmpi-fsvol
%{_datadir}/sblim-cmpi-fsvol/Linux_Fsvol.mof
%{_datadir}/sblim-cmpi-fsvol/Linux_Fsvol.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-fsvol/provider-register.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmpiOSBase_CommonFsvol.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmpiOSBase_CommonFsvol.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmpiOSBase_CommonFsvol.so
%{_libdir}/libcmpiOSBase_CommonFsvol.la
# XXX: shared dir
%dir %{_includedir}/sblim
%{_includedir}/sblim/OSBase_CommonFsvol.h
%{_includedir}/sblim/cmpiOSBase_CommonFsvol.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcmpiOSBase_CommonFsvol.a
