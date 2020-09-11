This tool automates compilation of [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) ```*.ksy``` and loading them into Python.

### WORK IN PROGRESS (doesn't work as shown below) and grossly insecure (don't use for public service)

```
import ksykaitai
Gif = ksykaitai.compile('git.ksy')
g = Gif.from_file('some.gif')
```

Roadmap
-------
* [ ] pack [Kaitai Struct compiler](https://github.com/kaitai-io/kaitai_struct_compiler) into a wheel
  * [ ] use https://github.com/dgiagio/warp to pack the compiler as a single binary together with headless Java `JRE`
* [ ] figure out the binary path after the wheel installation
* [ ] wrap the code below

Importing a ksy

```python
import kaitaiStructCompile.importer
kaitaiStructCompile.importer._importer.searchDirs.append(Path("./dirWithKSYFiles")) # you can add a dir to search for KSY files.
kaitaiStructCompile.importer._importer.flags["readStoresPos"]=True # you can set compiler flags, for more details see the JSON schema
from kaitaiStructCompile.importer.test import Test
Test # kaitaiStructCompile.importer.test.Test
```

Manual compilation

```python
from kaitaiStructCompile import compile
compile("./ksyFilePath.ksy", "./outputDir", additionalFlags=[
	#you can expose additional params here
])
```
