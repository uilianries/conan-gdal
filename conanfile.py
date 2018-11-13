import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration


class GdalConan(ConanFile):
    name = "gdal"
    version = "2.3.2"
    url = "https://bitbucket.org/microdrones/conan-gdal/"
    homepage = "http://github.com/OSGeo/gdal"
    description = "GDAL is an open source X/MIT licensed translator library for raster " \
                  "and vector geospatial data formats. "
    settings = "os", "compiler", "build_type", "arch"
    license = "X/MIT"
    require = (
        "geos/3.7.0@novolog/stable"
    )
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_folder = os.path.join("gdal-%s" % version, "gdal")
    _autotools = None

    def configure(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("Recipe only supports Linux for now.")

    def source(self):
        archive_name = "v%s.tar.gz" % self.version
        src_url = "%s/archive/%s" % (self.homepage, archive_name)
        tools.get(src_url)

    def _configure_autotools(self):
        if not self._autotools:
            args = [
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
                    "--without-xml2",
                    "--enable-static=%s" % ("no" if self.options.shared else "yes"),
                    "--enable-shared=%s" % ("yes" if self.options.shared else "no"),
                    "--with-pic=%s" % ("yes" if self.options.fPIC else "no")
                ]
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        with tools.chdir(self._source_folder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        with tools.chdir(self._source_folder):
            self.copy("LICENSE.TXT", dst="licenses")
            autotools = self._configure_autotools()
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
