#!/usr/bin/bash

COMPILER="0.9"
COMPILER_PATH="kaitai-struct-compiler"

echo "Cleaning up $COMPILER_PATH/..."
rm -rf "$COMPILER_PATH"
echo "Dowloading compiler..."
wget --continue https://dl.bintray.com/kaitai-io/universal/$COMPILER/kaitai-struct-compiler-$COMPILER.zip
unzip kaitai-struct-compiler-$COMPILER.zip
#rm kaitai-struct-compiler-$COMPILER.zip
mv kaitai-struct-compiler-$COMPILER "$COMPILER_PATH"

echo "Downloading JRE for compiler to work..."
wget --continue https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
tar xzvf OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
mv jdk-11.0.8+10-jre "$COMPILER_PATH/jre"

echo "Refreshing Python lib with imports..."
wget -N https://raw.githubusercontent.com/kaitai-io/kaitai_struct_python_runtime/master/kaitaistruct.py
