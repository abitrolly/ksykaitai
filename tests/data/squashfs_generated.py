# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class SquashfsSuperblock(KaitaiStruct):
    """SquashFS is a compressed filesystem in a file, that can be read-only
    accessed from low memory devices. It is popular for booting LiveCDs and
    packing self-contained binaries. SquashFS format is used by Ubuntu .snap
    packages. SquashFS is natively supported by Linux Kernel.
    
    .. seealso::
       Source - https://github.com/AgentD/squashfs-tools-ng/blob/master/doc/format.txt
    """

    class Compressor(Enum):
        gzip = 1
        lzo = 2
        lzma = 3
        xz = 4
        lz4 = 5
        zstd = 6
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.superblock = self._root.Superblock(self._io, self, self._root)

    class Flags(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nfs_export_table = self._io.read_bits_int(1) != 0
            self.data_deduplicated = self._io.read_bits_int(1) != 0
            self.fragments_always_generated = self._io.read_bits_int(1) != 0
            self.fragments_not_used = self._io.read_bits_int(1) != 0
            self.fragments_uncompresed = self._io.read_bits_int(1) != 0
            self._unnamed5 = self._io.read_bits_int(1) != 0
            self.data_blocks_uncompresed = self._io.read_bits_int(1) != 0
            self.inodes_uncompresed = self._io.read_bits_int(1) != 0
            self._unnamed8 = self._io.read_bits_int(4)
            self.id_table_uncompresed = self._io.read_bits_int(1) != 0
            self.compressor_options_present = self._io.read_bits_int(1) != 0
            self.xattrs_absent = self._io.read_bits_int(1) != 0
            self.xattrs_uncompressed = self._io.read_bits_int(1) != 0


    class Superblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x68\x73\x71\x73")
            self.inode_count = self._io.read_u4le()
            self.mod_time = self._io.read_u4le()
            self.block_size = self._io.read_u4le()
            self.frag_count = self._io.read_u4le()
            self.compressor = self._root.Compressor(self._io.read_u2le())
            self.block_log = self._io.read_u2le()
            self.flags = self._root.Flags(self._io, self, self._root)
            self.id_count = self._io.read_u2le()
            self.version_major = self._io.ensure_fixed_contents(b"\x04\x00")
            self.version_minor = self._io.ensure_fixed_contents(b"\x00\x00")
            self.root_inode_ref = self._io.read_u8le()
            self.bytes_used = self._io.read_u8le()
            self.id_table_start = self._io.read_u8le()
            self.xattr_id_table_start = self._io.read_u8le()
            self.inode_table_start = self._io.read_u8le()
            self.directory_table_start = self._io.read_u8le()
            self.fragment_table_start = self._io.read_u8le()
            self.export_table_start = self._io.read_u8le()



