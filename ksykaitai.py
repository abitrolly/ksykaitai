#!/usr/bin/env python

import importlib.util
import os
import tempfile

import kaitaiStructCompile
import kaitaiStructCompile.ICompiler as ICompilerModule
import kaitaiStructCompile.backend.cmdline as clibackend


def importbypath(pypath, modname=None):
    """ Returns imported module object """
    if not modname:
        modname = os.path.splitext(os.path.basename(pypath))[0]
    spec = importlib.util.spec_from_file_location(modname, pypath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def compile(ksypath):
    backend = clibackend.init(ICompilerModule,
                              kaitaiStructCompile.KaitaiCompilerException.KaitaiCompilerException,
                              kaitaiStructCompile.utils,
                              kaitaiStructCompile.defaults)

    with tempfile.TemporaryDirectory() as dirname:
        os.environ['JAVA_HOME'] = 'kaitai-struct-compiler/jre'
        kaitaiStructCompile.compile(ksypath, dirname, backend=backend, additionalFlags=['-no-version-check'])
        pyfile = f'{dirname}/squashfs_superblock.py'
        module = importbypath(pyfile)

    return module


module = compile('data/squashfs_superblock.ksy')
print(dir(module))
Squashfs = module.SquashfsSuperblock.from_file('data/yakshaveinc_eternal_amd64.snap')
print(dir(Squashfs))
print(dir(Squashfs.superblock))
print(f'inodes: {Squashfs.superblock.inode_count}')
