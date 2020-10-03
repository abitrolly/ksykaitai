#!/usr/bin/bash

wget https://dl.bintray.com/kaitai-io/universal/0.8/kaitai-struct-compiler-0.8.zip 
unzip kaitai-struct-compiler-0.8.zip
rm kaitai-struct-compiler-0.8.zip
mv kaitai-struct-compiler-0.8 kaitai-struct-compiler

wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
tar xzvf OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
mv jdk-11.0.8+10-jre kaitai-struct-compiler/jre
