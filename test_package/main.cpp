#include <iostream>

#include "gdal.h"

int main(int argc, char *argv[]) {
    const char* request = "GDAL_VERSION_NUM";
    const char* info = GDALVersionInfo(request);
    std::cout << "\u001b[32m✔ TEST GDAL conan package (" << info << ")\u001b[0m" << std::endl;
    return 0;
}