import tempfile

import kaitaiStructCompile
import kaitaiStructCompile.ICompiler as ICompilerModule
import kaitaiStructCompile.backend.cmdline as clibackend


def compile(ksypath):
    backend = clibackend.init(ICompilerModule,
                              kaitaiStructCompile.KaitaiCompilerException.KaitaiCompilerException,
                              kaitaiStructCompile.utils,
                              kaitaiStructCompile.defaults)

    with tempfile.TemporaryDirectory() as dirname:
        kaitaiStructCompile.compile(ksypath, dirname, backend=backend)


compile('../kaitai_struct_visualizer/squashfs_superblock.ksy')
