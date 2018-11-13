import os
import sys
from conans import ConanFile, AutoToolsBuildEnvironment, VisualStudioBuildEnvironment, tools


class GdalConan(ConanFile):
    name = "gdal"
    version = "2.3.2"
    url = "https://bitbucket.org/microdrones/conan-gdal/"
    description = "GDAL is an open source X/MIT licensed translator library for raster " \
                  "and vector geospatial data formats. "
    settings = "os", "compiler", "build_type", "arch"
    license = "X/MIT"
    exports = ["FindGDAL.cmake"]
    require = (
        "geos/3.7.0@novolog/stable"
    )
    source_dir = "gdal-%s/gdal" % version
    source_folder = "gdal-%s/gdal" % version
    archive_name = "v%s.tar.gz" % version
    src_url = "http://github.com/OSGeo/gdal/archive/%s" % archive_name
    generators = "cmake"

    def source(self):
        tools.download(self.src_url, self.archive_name)
        tools.unzip(self.archive_name)
        os.unlink(self.archive_name)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        with tools.environment_append(autotools.vars):
            args = [
                "--prefix=%s" % self.build_folder,
                "--disable-static",
                "--enable-shared",
                "--with-geos",
                "--with-threads",
                "--with-libtiff=internal",
                "--with-geotiff=internal",
                "--without-hide",
                "--without-libz",
                "--without-bsb",
                "--without-cfitsio",
                "--without-cryptopp",
                "--without-curl",
                "--without-dwgdirect",
                "--without-ecw",
                "--without-expat",
                "--without-fme",
                "--without-freexl",
                "--without-gif",
                "--without-gif",
                "--without-gnm",
                "--without-grass",
                "--without-grib",
                "--without-hdf4",
                "--without-hdf5",
                "--without-idb",
                "--without-ingres",
                "--without-jasper",
                "--without-jp2mrsid",
                "--without-jpeg",
                "--without-kakadu",
                "--without-libgrass",
                "--without-libkml",
                "--without-libtool",
                "--without-mrf",
                "--without-mrsid",
                "--without-mysql",
                "--without-netcdf",
                "--without-odbc",
                "--without-ogdi",
                "--without-openjpeg",
                "--without-pcidsk",
                "--without-pcraster",
                "--without-pcre",
                "--without-perl",
                "--without-pg",
                "--without-php",
                "--without-png",
                "--without-python",
                "--without-qhull",
                "--without-sde",
                "--without-sqlite3",
                "--without-webp",
                "--without-xerces",
                "--without-xml2"
            ]

            self.run("cd %s && ./configure %s" % (self.source_dir, " ".join(args)))
            self.run("cd %s && make -j%s" % (self.source_dir, tools.cpu_count()))
            self.run("cd %s && make install" % self.source_dir)

    def package(self):
        include_folder = os.path.join(self.build_folder, "include")
        lib_folder = os.path.join(self.build_folder, "lib")

        self.copy("FindGDAL.cmake", ".", ".")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*", dst="lib", src=lib_folder)

        data_folder = os.path.join(self.build_folder, "share", "gdal")
        self.copy(pattern="*", dst="data", src=data_folder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["gdal"]
