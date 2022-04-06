#!/usr/bin/bash

set -e
set -x

COMPILER="0.9"
COMPILER_PATH="kaitai-struct-compiler"

echo "Cleaning up $COMPILER_PATH/..."
rm -rf "$COMPILER_PATH"
echo "Dowloading compiler..."
wget --no-verbose --continue https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.9/kaitai-struct-compiler-0.9.zip
unzip kaitai-struct-compiler-$COMPILER.zip
#rm kaitai-struct-compiler-$COMPILER.zip
mv kaitai-struct-compiler-$COMPILER "$COMPILER_PATH"

echo "Downloading JRE for compiler to work..."
wget -q --continue https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
tar xzvf OpenJDK11U-jre_x64_linux_hotspot_11.0.8_10.tar.gz
mv jdk-11.0.8+10-jre "$COMPILER_PATH/jre"

echo "Refreshing Python lib with imports..."
wget -N https://raw.githubusercontent.com/kaitai-io/kaitai_struct_python_runtime/master/kaitaistruct.py

echo "Converting $COMPILER_PATH into Python package"
touch "$COMPILER_PATH"/__init__.py
