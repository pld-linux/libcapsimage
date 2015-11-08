Summary:	IPF image support library
Summary(pl.UTF-8):	Biblioteka obsługująca obrazy IPF
Name:		libcapsimage
Version:	4.2
Release:	1
License:	Software Preservation Society (only limited, non-commercial distribution is allowed)
Group:		Libraries
# http://www.softpres.org/_media/files:ipflib42_linux-i686.tar.gz?id=download
Source0:	ipflib42_linux-i686.tar.gz
# Source0-md5:	420ae4e6112abf8654a36dc90fa671b8
# http://www.softpres.org/_media/files:ipflib42_linux-x86_64.tar.gz?id=download
Source1:	ipflib42_linux-x86_64.tar.gz
# Source1-md5:	a0868374efa8ed88ec32e82b133b70b6
# http://www.softpres.org/_media/files:ipflib42_linux-powerpc.tar.gz?id=download
Source2:	ipflib42_linux-powerpc.tar.gz
# Source2-md5:	eddd4b47262b38169314939abe2045fc
URL:		http://www.softpres.org/?id=download
BuildRequires:	libstdc++-devel
ExclusiveArch:	%{ix86} %{x8664} ppc
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
%setup -q -c -T
%ifarch %{ix86}
%{__tar} xz --strip-components=1 -f %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} xz --strip-components=1 -f %{SOURCE1}
%endif
%ifarch ppc
%{__tar} xz --strip-components=1 -f %{SOURCE2}
%endif

ln -s libcapsimage.so.*.* libcapsimage.so
%{__rm} examples/ipfinfo

%build
cd examples
%{__cc} %{rpmldflags} %{rpmcflags} %{rpmcppflags} -o ipfinfo ipfinfo.c -I../include -L.. -lcapsimage

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/caps}

install examples/ipfinfo $RPM_BUILD_ROOT%{_bindir}
install libcapsimage.so.*.* $RPM_BUILD_ROOT%{_libdir}
ln -s libcapsimage.so.*.* $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so.4
ln -s libcapsimage.so.*.* $RPM_BUILD_ROOT%{_libdir}/libcapsimage.so
cp -p include/caps/*.h $RPM_BUILD_ROOT%{_includedir}/caps

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc HISTORY LICENSE README
%attr(755,root,root) %{_bindir}/ipfinfo
%attr(755,root,root) %{_libdir}/libcapsimage.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcapsimage.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapsimage.so
%{_includedir}/caps
