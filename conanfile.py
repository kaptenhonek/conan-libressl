from nxtools import NxConanFile
from conans import CMake, tools
from glob import glob


class LibreSSLConan(NxConanFile):
    name = "libressl"
    version = "2.8.3"
    license = "OpenBSD"
    url = "https://github.com/hoxnox/conan-libressl"
    license = "https://github.com/libressl/libressl/blob/master/src/LICENSE"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    description = "LibreSSL is a version of the TLS/crypto stack forked from OpenSSL in 2014, with goals of modernizing the codebase, improving security, and applying best practice development processes."

    def do_source(self):
        self.retrieve("9b640b13047182761a99ce3e4f000be9687566e0828b4a72709e9e6a3ef98477",
                [
                    "vendor://openbsd/libressl/libressl-{v}.tar.gz".format(v=self.version),
                    "https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{v}.tar.gz".format(v=self.version)
                ], "libressl-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        cmake = CMake(self)
        tools.untargz("libressl-{v}.tar.gz".format(v=self.version), "{staging_dir}/src".format(staging_dir=self.staging_dir))
        src_dir = "{staging_dir}/src/libressl-{v}".format(staging_dir=self.staging_dir, v=self.version)
        cmake.build_dir = "{src_dir}/build".format(src_dir=src_dir)
        # for file in sorted(glob("patch/*.patch")):
        #     self.output.info("Applying patch '{file}'".format(file=file))
        #     tools.patch(base_path=src_dir, patch_file=file, strip=0)
        cmake_defs = {"CMAKE_INSTALL_PREFIX": self.staging_dir,
                      "CMAKE_INSTALL_LIBDIR": "lib",
                      "BUILD_SHARED": "1" if self.options["libressl"].shared else "0",
                      "LIBRESSL_APPS": "OFF",
                      "LIBRESSL_TESTS": "OFF"}
        cmake_defs.update(self.cmake_crt_linking_flags())
        cmake.configure(defs=cmake_defs, source_dir=src_dir)
        cmake.build(target="install")

    def do_package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = [
                    "tls-shared" if self.options["libressl"].shared else "tls.lib",
                    "ssl-shared" if self.options["libressl"].shared else "ssl.lib",
                    "crypto-shared" if self.options["libressl"].shared else "crypto.lib"
                ]
        else:
            self.cpp_info.libs = ["tls", "ssl", "crypto"]

