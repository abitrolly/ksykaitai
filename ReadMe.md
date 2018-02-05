kaitaiStructCompile.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[wheel](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py/-/jobs/artifacts/master/raw/wheels/kaitaiStructCompile-0.CI-py3-none-any.whl?job=build)
[![PyPi Status](https://img.shields.io/pypi/v/kaitaiStructCompile.py.svg)](https://pypi.python.org/pypi/kaitaiStructCompile.py)
[![GitLab build status](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py/badges/master/pipeline.svg)](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py/commits/master)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/kaitaiStructCompile.py.svg)](https://coveralls.io/r/KOLANICH/kaitaiStructCompile.py)
[![GitLab coverage](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py/badges/master/coverage.svg)](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py/commits/master)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/kaitaiStructCompile.py.svg)](https://libraries.io/github/KOLANICH/kaitaiStructCompile.py)

This is a tool automating compilation [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) ```*.ksy``` files into python ones.


Features
--------

* python bindings to compile KS `.ksy` specs into python source code.
* importer allowing to import `ksy`s. Seamlessly compiles `ksy`s into python sources. Useful for playing in IPython shell.
* `setuptools` plugin to automate compiling `ksy`s into `py` in process of building of your package.

Prerequisites
-------------
* [Kaitai Struct compiler](https://github.com/kaitai-io/kaitai_struct_compiler) must be unpacked somewhere and all its prerequisites like `JRE` or `OpenJDK ` must be installed.
* Path to Kaitai Struct compiler root dir (the one containing `lib`, `bin` and `formats`) must be exposed as `KAITAI_STRUCT_ROOT` environment variable.
* Python 3. [```Python 2``` is dead, I don't take part in raping its corpse.](https://python3statement.org/).
* A backend must be installed.
	* [`kaitaiStructCompile.backend.CLI`](https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.backend.CLI) - the default backend using [`subprocess`](https://docs.python.org/3/library/subprocess.html) to interact with KSC. Installed automatically - it is put into dependencies of this package. The other backends are installed manually. It is highy recommended to use other backends since this one may be insecure because of CLI injections.
	* More backends may be available in future. Currently they are not because of [the issue](https://github.com/kaitai-io/kaitai_struct/issues/466).

Usage
-----

### Importing a ksy

```python
import kaitaiStructCompile.importer
kaitaiStructCompile.importer._importer.searchDirs.append(Path("./dirWithKSYFiles")) # you can add a dir to search for KSY files.
kaitaiStructCompile.importer._importer.flags["readStoresPos"]=True # you can set compiler flags, for more details see the JSON schema
from kaitaiStructCompile.importer.test import Test
Test # kaitaiStructCompile.importer.test.Test
```

### Manual compilation

```python
from kaitaiStructCompile import compile
compile("./ksyFilePath.ksy", "./outputDir", additionalFlags=[
	#you can expose additional params here
])
```



### `setuptools` extension
Since we usually need this in the process of building python libraries using Kaitai Struct definitions, this tool contains an addon to `setuptools` allowing you to just specify the files you need to compile in a declarative way.

Just an add a property `kaitai` into the dict. It is a dict specified and documented with [the JSON Schema](./kaitaiStructCompile/config.schema.json), so read it carefully.

Here a piece from one project with comments follows:

```python
from pathlib import Path
formatsPath=str(Path(__file__).parent / "kaitai_struct_formats") # since the format is in the kaitai_struct_formats repo, we just clone it, but we need its path to show the compiler where the ksy file is. So we put the directory of formats in the current directory.
cfg["kaitai"]={
	"outputDir": "SpecprParser", # the directory we will put the generated file to
	"inputDir": formatsPath, # the directory we take KSYs from
	"formatsRepo": { # we need to get the repo of formats, https://github.com/kaitai-io/kaitai_struct_formats
		"localPath" : formatsPath, # Where the repo will be downloaded and from which location the compiler will use it.
		"update": True # We need the freshest version to be downloaded from GitHub. We don't need the snapshot shipped with compiler!
	},
	"formats":{ # here we declare our targets. The key is the resulting file name. The value is the descriptor.
		"specpr.py": {
			"path":"scientific/spectroscopy/specpr.ksy", # the path of the spec within 
			"postprocess":["permissiveDecoding"] # Enumerate here the names of post-processing steps you need. The default ones are in toolbox file. You can also add the own ones by creating in the main scope the mapping name => function.
		}
	}
}

setup(use_scm_version = True, **cfg)
```
