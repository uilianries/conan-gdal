import os
from conans import ConanFile, CMake

class GdalTestConan(ConanFile):
    """ GDAL Conan package test """

    requires = "gdal/2.3.2@microdrones/stable"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualenv"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if self.settings.os == "Windows":
            self.run("activate && %s %s" % (os.sep.join([".", "bin", "helloworld"]), "conan"))
        else:
            self.run(os.sep.join([".", "bin", "helloworld"]))
