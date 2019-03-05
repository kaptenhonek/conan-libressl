import os

from conans import ConanFile, CMake, tools


class LibreSSLConan(ConanFile):
    name = "libressl"
    version = "2.8.3"
    license = "OpenBSD"
    url = "https://github.com/kaptenhonek/conan-libressl"
    license = "https://github.com/libressl/libressl/blob/master/src/LICENSE"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    description = "LibreSSL is a version of the TLS/crypto stack forked from OpenSSL in 2014, with goals of modernizing the codebase, improving security, and applying best practice development processes."

    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{v}.tar.gz".format(v=self.version)
        
        tools.get(source_url, sha256="9b640b13047182761a99ce3e4f000be9687566e0828b4a72709e9e6a3ef98477")
        os.rename("libressl-%s" % self.version, self._source_subfolder)

        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
            '''if(NOT MSVC)
	add_subdirectory(man)
endif()''',
            "")

    def build(self):
        cmake = CMake(self)
        
        cmake_defs = {
            "CMAKE_INSTALL_PREFIX": "install",
            "BUILD_SHARED": "ON" if self.options.shared else "OFF",
            "LIBRESSL_APPS": "OFF",
            "LIBRESSL_TESTS": "OFF"
        }

        os.mkdir("install")

        cmake.configure(defs=cmake_defs, source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        self.copy(pattern="*", dst="include", src="install/include")
        self.copy(pattern="*.dll", dst="bin", keep_path=False, src="install")
        self.copy(pattern="*.lib", dst="lib", keep_path=False, src="install")
        self.copy(pattern="*.a", dst="lib", keep_path=False, src="install")
        self.copy(pattern="*.so*", dst="lib", keep_path=False, src="install")
        self.copy(pattern="*.dylib", dst="lib", keep_path=False, src="install")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
