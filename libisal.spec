#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Optimized low-level functions library for storage systems
Summary(pl.UTF-8):	Biblioteka zoptymalizowanych funkcji niskopoziomowych do systemów przechowywania danych
Name:		libisal
Version:	2.31.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/isa-l/releases
Source0:	https://github.com/intel/isa-l/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5403379f5f8f8113a412f32d17471566
Patch0:		isa-l-x86.patch
Patch1:		x32.patch
URL:		https://github.com/01org/isa-l
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2
%ifarch %{ix86} %{x8664} x32
# nasm or yasm, whichever has higher "feature number" (max=10 for AVX512+)
BuildRequires:	nasm >= 2.13
BuildRequires:	yasm >= 1.2.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ISA-L is a collection of optimized low-level functions targeting
storage applications. ISA-L includes:
 - Erasure codes - fast block Reed-Solomon type erasure codes for any
   encode/decode matrix in GF(2^8).
 - CRC - Fast implementations of cyclic redundancy check. Six
   different polynomials supported.
 - iscsi32, ieee32, t10dif, ecma64, iso64, jones64.
 - RAID - calculate and operate on XOR and P+Q parity found in common
   RAID implementations.
 - Compression - Fast deflate-compatible data compression.
 - De-compression - Fast inflate-compatible data compression.

%description -l pl.UTF-8
ISA-L to zbiór zoptymalizowanych funkcji niskopoziomowych,
przeznaczonych do zastosowań związanych z przechowywaniem danych.
Biblioteka zawiera:
- kody korekcyjne (erasure codes) - szybkie kody korekcyjne typu
  Reeda-Solomona dla dowolnej macierzy kodowania/dekodowania w GF(2^8)
- CRC - szybkie implementacje cyklicznej kontroli nadmiarowej;
  obsługiwane jest sześć różnych wielomianów
- iscsi32, ieee32, t10dif, ecma64, iso64, jones64
- RAID - obliczanie i operacje na parzystości XOR oraz P+Q, używanych
  w popularnych implementacjach RAID
- kompresja - szybka kompresja danych zgodna z metodą deflate
- dekompresja - szybka kompresja danych zgodna z metodą inflate

%package devel
Summary:	Header files for ISA-L library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ISA-L
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ISA-L library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ISA-L.

%package static
Summary:	Static ISA-L library
Summary(pl.UTF-8):	Statyczna biblioteka ISA-L
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ISA-L library.

%description static -l pl.UTF-8
Statyczna biblioteka ISA-L.

%prep
%setup -q -n isa-l-%{version}
%patch0 -p1
%ifarch x32
%patch1 -p1
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make} \
%ifarch %{ix86}
	yasm_args="-f elf32" \
%endif
%ifarch x32
	yasm_args="-f elfx32"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies, obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md Release_notes.txt
%attr(755,root,root) %{_bindir}/igzip
%attr(755,root,root) %{_libdir}/libisal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libisal.so.2
%{_mandir}/man1/igzip.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisal.so
%{_includedir}/isa-l
%{_includedir}/isa-l.h
%{_pkgconfigdir}/libisal.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libisal.a
%endif
