
import importlib.util
import tempfile

import kaitaiStructCompile
import kaitaiStructCompile.ICompiler as ICompilerModule
import kaitaiStructCompile.backend.cmdline as clibackend


def importbypath(pypath):
    modname = 'squashfs_superblock'
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
        kaitaiStructCompile.compile(ksypath, dirname, backend=backend)
        pyfile = f'{dirname}/squashfs_superblock.py'
        return importbypath(pyfile)

    #dirname = tempfile.mkdtemp()
    #kaitaiStructCompile.compile(ksypath, dirname, backend=backend)


module = compile('data/squashfs_superblock.ksy')
print(dir(module))
Squashfs = module.SquashfsSuperblock.from_file('data/yakshaveinc_eternal_amd64.snap')
print(dir(Squashfs))
print(dir(Squashfs.superblock))
print(f'inodes: {Squashfs.superblock.inode_count}')
