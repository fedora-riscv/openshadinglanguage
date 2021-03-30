# Required for the plugin directory name, see https://github.com/OpenImageIO/oiio/issues/2583
%global oiio_major_minor_ver %(rpm -q --queryformat='%%{version}' OpenImageIO-devel | cut -d . -f 1-2)
#%%global prerelease -RC1

# Force out of source tree build
%undefine __cmake_in_source_build

Name:           openshadinglanguage
Version:        1.11.10.0
Release:        9%{?dist}
Summary:        Advanced shading language for production GI renderers

License:        BSD
URL:            https://github.com/imageworks/OpenShadingLanguage
Source:         %{url}/archive/Release-%{version}%{?prerelease}.tar.gz

BuildRequires:  bison
BuildRequires:  boost-devel >= 1.55
BuildRequires:  clang-devel
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  llvm-devel
BuildRequires:  partio-devel
BuildRequires:  pkgconfig(IlmBase)
BuildRequires:  pkgconfig(OpenImageIO) >= 2.0
%if 0%{?fedora} < 32
BuildRequires:  pugixml-devel
BuildRequires:  pkgconfig(OpenEXR)
%else
BuildRequires:  pkgconfig(pugixml)
%endif

BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(zlib)

# 64 bit only
ExclusiveArch:  x86_64 aarch64 ppc64le s390x

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

%package        -n python3-%{name}
Summary:        %{summary}
License:        BSD
BuildRequires:  cmake(pybind11)
BuildRequires:    pkgconfig(python3)

%description    -n python3-%{name}
%{_description}

%prep
%autosetup -n OpenShadingLanguage-Release-%{version}%{?prerelease}
# Use python3 binary instead of unversioned python
sed -i -e "s/COMMAND python/COMMAND python3/" $(find . -iname CMakeLists.txt)

%build
%cmake \
   -DCMAKE_CXX_STANDARD=14 \
   -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name} \
   -DCMAKE_SKIP_RPATH=TRUE \
   -DCMAKE_SKIP_INSTALL_RPATH=YES \
   -DOSL_BUILD_MATERIALX:BOOL=ON \
   -DOSL_SHADER_INSTALL_DIR:PATH=%{_datadir}/%{name}/shaders/ \
   -Dpartio_DIR=%{_prefix} \
   -DPARTIO_INCLUDE_DIR=%{_includedir} \
   -DPARTIO_LIBRARIES=%{_libdir} \
   -DPYTHON_VERSION=%{python3_version} \
   -DSTOP_ON_WARNING=OFF
%cmake_build

%install
%cmake_install

# Move the OpenImageIO plugin into its default search path
mkdir %{buildroot}%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}
mv %{buildroot}%{_libdir}/osl.imageio.so %{buildroot}%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/

%files
%license LICENSE.md
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
%license LICENSE.md
%dir %{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/
%{_libdir}/OpenImageIO-%{oiio_major_minor_ver}/osl.imageio.so
   
%files libs
%license LICENSE.md
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

%files -n python3-%{name}
%{python3_sitearch}/oslquery.so

%changelog
* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.11.10.0-9
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Jonathan Wakely <jwakely@redhat.com> - 1.11.10.0-7
- Rebuilt for Boost 1.75

* Fri Jan 22 2021 Tom Stellard <tstellar@redhat.com> - 1.11.10.0-6
- Rebuild for clang-11.1.0

* Mon Jan  4 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.10.0-5
- Rebuild for OpenImageIO-2.2.10.0

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 1.11.10.0-4
- Rebuild for OpenEXR 2.5.3.

* Tue Dec 08 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.10.0-3
- Rebuild for Partio 1.14.0

* Fri Dec 04 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.10.0-2
- Rebuild for Partio 1.13.2

* Wed Dec 02 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.10.0-1
- Update to 1.11.10.0

* Thu Oct 01 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.9.0-1
- Update to 1.11.9.0

* Thu Oct 01 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.8.0-1
- Update to 1.11.8.0

* Sun Sep 13 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.7.3-2
- Rebuild for Partio 1.13.0

* Sat Sep 05 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.7.3-1
- Update to 1.11.7.3

* Fri Sep 04 2020 Richard Shaw <hobbes1069@gmail.com> - 1.11.7.1-0.2
- Rebuild for OpenImageIO 2.2.

* Fri Aug 21 2020 Simone Caronni <negativo17@gmail.com> - 1.11.7.1-0.2
- Update to 1.11.7.1-RC1.

* Thu Aug 06 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.7.0-0.1
- Update to 1.11.7.0-beta1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.6.0-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.6.0-4
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
