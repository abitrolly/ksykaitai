#!/usr/bin/bash

COMPILER="0.9"
COMPILER_PATH="kaitai-struct-compiler"

echo "Cleaning up $COMPILER_PATH..."
rm -rf "$COMPILER_PATH"
echo "Dowloading compiler..."
wget https://dl.bintray.com/kaitai-io/universal/$COMPILER/kaitai-struct-compiler-$COMPILER.zip 
unzip kaitai-struct-compiler-$COMPILER.zip
rm kaitai-struct-compiler-$COMPILER.zip
mv kaitai-struct-compiler-$COMPILER "$COMPILER_PATH"

wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
tar xzvf OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
mv jdk-11.0.8+10-jre kaitai-struct-compiler/jre
