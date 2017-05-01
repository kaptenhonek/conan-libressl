from nxtools import NxConanFile, retrieve
from conans import CMake


class LibreSSLConan(NxConanFile):
    name = "libressl"
    version = "2.5.3"
    license = "OpenBSD"
    url = "https://www.libressl.org/"
    license = "https://github.com/libressl/libressl/blob/master/src/LICENSE"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    description = "LibreSSL is a version of the TLS/crypto stack forked from OpenSSL in 2014, with goals of modernizing the codebase, improving security, and applying best practice development processes."

    def do_source(self):
        retrieve("14e34cc586ec4ce5763f76046dcf366c45104b2cc71d77b63be5505608e68a30",
                [
                    "vendor://openbsd/libressl/libressl-{v}.tar.gz".format(v=self.version),
                    "https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{v}.tar.gz".format(v=self.version)
                ],
                "libressl-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        cmake = CMake(self)
        cmake.configure(defs={
                "CMAKE_INSTALL_PREFIX": self.package_folder,
                "CMAKE_INSTALL_LIBDIR": "lib",
                "BUILD_SHARED": "1" if self.options.shared else "0"
            }, source_dir="libressl-{v}".format(v=self.version))
        cmake.build(target="install")

    def do_package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = [
                    "tls-shared" if self.options.shared else "tls.lib",
                    "ssl-shared" if self.options.shared else "ssl.lib",
                    "crypto-shared" if self.options.shared else "crypto.lib"
                ]
        else:
            self.cpp_info.libs = [
                    "tls.so" if self.options.shared else "tls.a",
                    "ssl.so" if self.options.shared else "ssl.a",
                    "crypto.so" if self.options.shared else "crypto.a"
                ]

