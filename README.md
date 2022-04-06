The library that automates compilation of [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct)
parsers from  `*.ksy` files and importing them in Python.

```python
import ksykaitai

Gif = ksykaitai.compile('gif.ksy')
g = Gif.from_file('some.gif')
```

`ksykaitai` module calls command line
[`Kaitai Struct Compiler`](https://github.com/kaitai-io/kaitai_struct_compiler)
and follows the "best data science practices" of packing huge runtime
binaries into, well, binary wheels. And because the compiler needs JRE,
the project packs the JRE into the wheel as well.


### Credits and copyright

The awesome production of genius engineering effort builds upon the CLI
interface [work by KOLANICH](https://github.com/kaitaiStructCompile/kaitaiStructCompile.py),
who will most likely give a lot of curses
towards these 50Mb of monstrousity after dealing with bits and bytes in
the neat way that `kaitai.io` provides. Despite of that, he is really
quick and helpful with issues on the way. Please give him a hug. :D

While the code of `ksykaitai` and underlying KOLANICH lib is free of
copyright, the Kaitai Compiler itself is not. That probably doesn't
affect the generated code, but you may want to open an issue in Kaitai
project to be 100% sure.


### Versioning

`0.9k1` consists of two parts - `0.9` is the version of compiler shipped,
and `1` is the version of the `ksykaitai` itself.


### Releasing

Releasing was supposed to be based on `git tag`. The version had to be
extracted from it by `setuptools_vcs` to build the wheel and upload it to
PyPI. But I found [no way to detect tag push](https://github.com/yakshaveinc/linux/pull/44)
in GitHub Actions. Uploading is (meant to be) done by CI automatically,
but for now that's a three step manual action.

   1. run `./prepare.sh` to download the compiler and Java JRE
   2. run `./release.sh` to create the wheel named from latest tag
   3. upload the wheel to PyPI


### Packaging data into Python wheels

The wheel is built on insane amount of burned braincells from hacks and
experiments that were necessary to find out the way to get compiler data
inside a wheel. Unfortunately I wasn't doing notices over these months,
and now it is probably impossible to recover what actually worked and
what not. I had to patch `pip` and `setuptools` to get debug data and
understand what's going on inside. I tried `flit` and `poetry` with no
success. In the end I believe I am using https://github.com/pypa/build
and some `setuptools` magic with `setup.cfg` and `pyproject.toml` and
`MANIFEST.in` to do the job. You can try to tear them apart bit by bit
to see where the process breaks, to figure out which parts are really
needed to do the trick for you own data science.


Roadmap
-------
* [x] commit all source dependencies to repo
* [x] download compiler with binary dependencies (Java JRE)
* [x] pack [Kaitai Struct compiler](https://github.com/kaitai-io/kaitai_struct_compiler) into a wheel
  * [ ] use https://github.com/dgiagio/warp to pack the compiler as a single binary together with headless Java `JRE`
  * [ ] reduce size of JRE to absolute minimum
    * [ ] or use Scala Native to build the compiler
      * [ ] which needs native Scala parser for YAML
* [x] figure out the binary path after the wheel installation
* [ ] add to https://github.com/kaitai-io/awesome-kaitai
* [ ] somehow mark the wheel as being Linux only (because of JRE)
* [ ] import contributed formats without explicitly referencing files (wrap the code below)


The code below is for enlightment and may not work at all. Just thought
you should know. It probably hold a very useful bits of data for future
development.

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
