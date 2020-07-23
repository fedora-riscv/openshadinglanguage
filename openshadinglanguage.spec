# Required for the plugin directory name, see https://github.com/OpenImageIO/oiio/issues/2583
%global oiio_major_minor_ver %(rpm -q --queryformat='%%{version}' OpenImageIO-devel | cut -d . -f 1-2)
%global prerelease -dev

Name:           openshadinglanguage
Version:        1.11.6.0
Release:        4%{?dist}
Summary:        Advanced shading language for production GI renderers

License:        BSD
URL:            https://github.com/imageworks/OpenShadingLanguage
Source:         %{url}/archive/Release-%{version}%{?prerelease}.tar.gz

BuildRequires:	bison
BuildRequires:  boost-devel >= 1.55
BuildRequires:  clang-devel
BuildRequires:  cmake
BuildRequires:	flex
BuildRequires:  gcc-c++
BuildRequires:  llvm-devel
#BuildRequires:	meson
BuildRequires:  partio-devel
BuildRequires:  pkgconfig(IlmBase)
BuildRequires:  pkgconfig(OpenImageIO) >= 2.0
%if 0%{?fedora} < 32
BuildRequires:  pugixml-devel
BuildRequires:  pkgconfig(OpenEXR)
%else
BuildRequires:  pkgconfig(pugixml)
%endif
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(Qt5)
# Compression
BuildRequires:  pkgconfig(zlib)

# Build failed on armhfp
ExcludeArch:    armhfp

%description
Open Shading Language (OSL) is a small but rich language for programmable
shading in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.

%package doc
Summary:        Documentation for OpenShadingLanguage
License:        CC-BY
BuildArch:      noarch
Requires:       %{name} = %{version}

%description doc
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.
This package contains documentation.

%package MaterialX-shaders-source
Summary:        MaterialX shader nodes
License:        BSD
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-common-headers

%description MaterialX-shaders-source
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.

This package contains the code for the MaterialX shader nodes.

%package example-shaders-source
Summary:        OSL shader examples
License:        BSD
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-common-headers

%description example-shaders-source
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.

This package contains some OSL example shaders.

%package common-headers
Summary:        OSL standard library and auxiliary headers
License:        BSD
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description common-headers
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.

This package contains the OSL standard library headers, as well
as some additional headers useful for writing shaders.

%package -n OpenImageIO-plugin-osl
Summary:        OpenImageIO input plugin
License:        BSD

%description -n OpenImageIO-plugin-osl
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.

This is a plugin to access OSL from OpenImageIO.

%package        libs
Summary:        OpenShadingLanguage's libraries
License:        BSD

%description    libs
Open Shading Language (OSL) is a language for programmable shading
in advanced renderers and other applications, ideal for describing
materials, lights, displacement, and pattern generation.


%package        devel
Summary:        Development files for %{name}
License:        BSD
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n OpenShadingLanguage-Release-%{version}%{?prerelease}
# Use python3 binary instead of unversioned python
sed -i -e "s/COMMAND python/COMMAND python3/" $(find . -iname CMakeLists.txt)

%build
%cmake \
   -B build \
   -DCMAKE_CXX_STANDARD=14 \
   -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name} \
   -DCMAKE_SKIP_RPATH=TRUE \
   -DCMAKE_SKIP_INSTALL_RPATH=YES \
   -DENABLERTTI=ON \
   -DOSL_BUILD_MATERIALX:BOOL=ON \
   -DOSL_SHADER_INSTALL_DIR:PATH=%{_datadir}/%{name}/shaders/ \
   -DSTOP_ON_WARNING=OFF \
   -DUSE_BOOST_WAVE=ON 
   
%make_build -C build

%install
%make_install -C build

# Move the OpenImageIO plugin into its default search path
mkdir %{buildroot}%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}
mv %{buildroot}%{_libdir}/osl.imageio.so %{buildroot}%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/

%files
%license LICENSE
%doc CHANGES.md CONTRIBUTING.md README.md
%{_bindir}/oslc
%{_bindir}/oslinfo
%{_bindir}/osltoy
%{_bindir}/testrender
%{_bindir}/testshade
%{_bindir}/testshade_dso

%files doc
%doc %{_docdir}/%{name}/

%files MaterialX-shaders-source
%{_datadir}/%{name}/shaders/MaterialX

%files example-shaders-source
%{_datadir}/%{name}/shaders/*.osl
%{_datadir}/%{name}/shaders/*.oso

%files common-headers
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/shaders
%{_datadir}/%{name}/shaders/*.h

%files -n OpenImageIO-plugin-osl
%license LICENSE
%dir %{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/
%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/osl.imageio.so
   
%files libs
%license LICENSE
%{_libdir}/libosl*.so.1*
%if 0%{?fedora} < 32
%{_libdir}/osl*.so.1*
%endif
%{_libdir}/libtestshade.so.1*

%files devel
%{_includedir}/OSL/
%{_libdir}/libosl*.so
%{_libdir}/libtestshade.so
%{_libdir}/cmake/
%{_libdir}/pkgconfig/

%changelog
* Wed Jul 22 2020 Luya Tshimbalanga <luya@fedoraproject,org> - 1.11.6.0-4
- Set library condition for Fedora 31 

* Mon Jul 20 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.6.0-3
- Enable partio

* Fri Jul 17 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.6.0-2
- Fix spec based on review (#1856589)

* Sun Jul 12 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.6.0-1
- Snapshot release
- Use OpenSUSE spec

* Mon Feb 17 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.10.9-1
- Initial build
