Summary:	IPF image support library
Summary(pl.UTF-8):	Biblioteka obsługująca obrazy IPF
Name:		libcapsimage
Version:	5.1
Release:	1
License:	Software Preservation Society (only limited, non-commercial distribution is allowed)
Group:		Libraries
#Source0Download: https://github.com/simonowen/capsimage
Source0:	https://www.kryoflux.com/download/spsdeclib_%{version}_source.zip
# Source0-md5:	27710eb05d4391560addeeb970ea1d45
#Source1Download: http://www.softpres.org/download
Source1:	http://www.softpres.org/_media/files:ipfaccessapi_multi.tgz?id=download&cache=cache&fakefile=/ipfaccessapi_multi.tgz
# Source1-md5:	f33c2ac4273871c1c59d375958e525a3
URL:		http://www.softpres.org/?id=download
BuildRequires:	libstdc++-devel
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CAPS image is a IPF image support library. IPF stands for
Interchangeable Preservation Format, and is the file format used to
preserve content, that is, floppy disk or ROM images (mostly related
to Amiga software).

%description -l pl.UTF-8
CAPS image to biblioteka obsługująca obrazy IPF. IPF to skrót od
Interchangeable Preservation Format (wymienny format zachowujący) i
jest to format plików używany do zachowywania obrazów zawartości
dyskietek lub pamięci ROM (głownie związanych z oprogramowaniem
komputerów Amiga).

%package devel
Summary:	Header files for CAPS image library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CAPS image
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CAPS image library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CAPS image.

%prep
%setup -q -c -a1

unzip -q capsimg_source_linux_macosx.zip
chmod 755 capsimg_source_linux_macosx/CAPSImg/configure

%build
cd capsimg_source_linux_macosx/CAPSImg
%configure

%{__make}

ln -s libcapsimage.so.*.* libcapsimage.so

cd ../../ipfaccessapi_multi/examples
%{__cc} %{rpmldflags} %{rpmcflags} %{rpmcppflags} -o ipfinfo ipfinfo.c -I../include -L../../capsimg_source_linux_macosx/CAPSImg -lcapsimage

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/caps}

%{__make} -C capsimg_source_linux_macosx/CAPSImg install \
	DESTDIR=$RPM_BUILD_ROOT

install ipfaccessapi_multi/examples/ipfinfo $RPM_BUILD_ROOT%{_bindir}
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so.5
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so
cp -p capsimg_source_linux_macosx/{LibIPF/*.h,Core/CommonTypes.h} $RPM_BUILD_ROOT%{_includedir}/caps
cp -p ipfaccessapi_multi/include/caps/capsimage.h $RPM_BUILD_ROOT%{_includedir}/caps

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DONATIONS.txt HISTORY.txt LICENCE.txt RELEASE.txt
%attr(755,root,root) %{_bindir}/ipfinfo
%attr(755,root,root) %{_libdir}/libcapsimage.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcapsimage.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapsimage.so
%{_includedir}/caps
