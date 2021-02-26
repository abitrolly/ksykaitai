#!/usr/bin/env python

import importlib.util
import os
import tempfile

import kaitaiStructCompile
import kaitaiStructCompile.ICompiler as ICompilerModule
import kaitaiStructCompile.backend.cmdline as clibackend


def patch_compiler_location():
    """ ksykaitai ships compiler in a wheel """
    if not os.environ['KAITAI_STRUCT_ROOT']:
        DIR = os.path.abspath(os.path.dirname(__file__))
        COMPILER = DIR + '/kaitai-struct-compiler'
        if os.path.exists(COMPILER):
            os.environ['KAITAI_STRUCT_ROOT'] = COMPILER


def import_by_path(pypath, modname=None):
    """ Returns imported module object """
    if not modname:
        modname = os.path.splitext(os.path.basename(pypath))[0]
    spec = importlib.util.spec_from_file_location(modname, pypath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def compile(ksypath, debug=False):
    """ Returns parser, subclass of KaitaiStruct.
        If `debug` is True, preserve compiled file in `/tmp/ksycompiled.py`
    """
    patch_compiler_location()

    backend = clibackend.init(ICompilerModule,
                              kaitaiStructCompile.KaitaiCompilerException.KaitaiCompilerException,
                              kaitaiStructCompile.utils,
                              kaitaiStructCompile.defaults)

    with tempfile.TemporaryDirectory() as dirname:
        os.environ['JAVA_HOME'] = 'kaitai-struct-compiler/jre'
        kaitaiStructCompile.compile(ksypath, dirname, backend=backend, additionalFlags=['-no-version-check'])
        # module name will be name of .ksy file without extension
        modname = os.path.splitext(os.path.basename(ksypath))[0]
        # name of generated python file, maybe kaitaiStructCompile provides it
        pyfile = f'{dirname}/{modname}.py'
        module = import_by_path(pyfile, modname)
        if debug:
            import shutil
            shutil.copyfile(pyfile, '/tmp/ksycompiled.py')
            print('DEBUG: created /tmp/ksycompiled.py')

    import inspect
    classes = [m[1] for m in inspect.getmembers(module, inspect.isclass)]
    ksyclass = [c for c in classes if c.__module__ == modname][0]

    return ksyclass


if __name__ == '__main__':
    Squashfs = compile('data/squashfs_superblock.ksy', True)
    sfs = Squashfs.from_file('data/yakshaveinc_eternal_amd64.snap')
    #print(dir(sfs))
    #print(dir(sfs.superblock))
    print(f'inodes: {sfs.superblock.inode_count}')
