# TODO: IPP (on bcond)
#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	sse2		# SSE2 instructions without detection (detected SSE2/AVX parts are always enabled)

%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif

Summary:	C-Blosc2: a fast, compressed and persistent data store library for C
Summary(pl.UTF-8):	C-Blosc2: biblioteka szybkiego, skompresowanego i trwałego przechowywania danych dla C
Name:		c-blosc2
Version:	2.8.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/Blosc/c-blosc2/releases
Source0:	https://github.com/Blosc/c-blosc2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	814350965b8ae30e74787a6b4743b113
Patch0:		%{name}-sse2.patch
URL:		https://www.blosc.org/
BuildRequires:	cmake >= 3.16.3
BuildRequires:	lz4-devel
BuildRequires:	zlib-devel
# FIXME: zlib-ng-devel preffered
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blosc is a high performance compressor optimized for binary data. It
has been designed to transmit data to the processor cache faster than
the traditional, non-compressed, direct memory fetch approach via a
memcpy() OS call. Blosc main goal is not just to reduce the size of
large datasets on-disk or in-memory, but also to accelerate
memory-bound computations.

C-Blosc2 is the new major version of C-Blosc and is backward
compatible with both the C-Blosc1 API and its in-memory format.
However, the reverse thing is generally not true for the format;
buffers generated with C-Blosc2 are not format-compatible with
C-Blosc1 (i.e. forward compatibility is not supported).

%description -l pl.UTF-8
Blosc to wysoko wydajny kompresor zoptymalizowany dla danych
binarnych. Został zaprojektowany do przesyłania danych do pamięci
podręcznej procesora szybciej, niż tradycyjne pobieranie danych
nieskompresowanych poprzez wywołanie memcpy(). Głównym celem Blosc
jest nie tylko zmniejszenie rozmiaru danych na dysku lub w pamięci,
ale także przyspieszenie obliczeń w pamięci.

C-Blosc2 to nowa główna wersja C-Blosc. Jest zgodna wstecznie z API
C-Blosc1, jak i formatem w pamięci. Jednak w drugą stronę to nie
zachodzi: bufory wygenerowane przez C-Blosc2 nie mają formatu
zgodnego z C-Blosc1 (zgodność formatu nie jest obsługiwana).

%package devel
Summary:	Header files for blosc2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki blosc2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for blosc2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki blosc2.

%package static
Summary:	Static blosc2 library
Summary(pl.UTF-8):	Statyczna biblioteka blosc2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static blosc2 library.

%description static -l pl.UTF-8
Statyczna biblioteka blosc2.

%prep
%setup -q
%patch0 -p1

%build
%cmake -B build \
	%{!?with_static_libs:-DBUILD_STATIC=OFF} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DDEACTIVATE_IPP=ON \
	-DPREFER_EXTERNAL_LZ4=ON \
	-DPREFER_EXTERNAL_ZLIB=ON \
	-DPREFER_EXTERNAL_ZSTD=ON \
	%{?with_sse2:-DREQUIRE_SSE2=ON}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE.md FAQ.md LICENSE.txt README.rst README_B2ND_METALAYER.rst README_CFRAME_FORMAT.rst README_CHUNK_FORMAT.rst README_SFRAME_FORMAT.rst README_THREADED.rst RELEASE_NOTES.md ROADMAP.rst THANKS.rst TODO-refactorization.txt
%attr(755,root,root) %{_libdir}/libblosc2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblosc2.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblosc2.so
%{_includedir}/b2nd.h
%{_includedir}/blosc2.h
%{_includedir}/blosc2
%{_pkgconfigdir}/blosc2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libblosc2.a
%endif
