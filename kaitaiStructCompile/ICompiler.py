import typing, types
from pathlib import Path

from .KaitaiCompilerException import KaitaiCompilerException
from .utils import *


class ICompileResult:
	__slots__ = ("msg", "moduleName", "mainClassName", "sourcePath", "path")

	def __init__(self, moduleName: str, mainClassName: str, msg: str) -> None:
		self.msg = msg
		self.moduleName = moduleName
		self.mainClassName = mainClassName
		self.sourcePath = None

	def getText(self) -> str:
		raise NotImplementedError()

	@property
	def needsSave(self):
		raise NotImplementedError()

	def __repr__(self) -> str:
		return self.__class__.__name__ + "<" + ", ".join((self.moduleName, self.mainClassName)) + ">"


class InMemoryCompileResult(ICompileResult):
	__slots__ = ("text",)

	def __init__(self, moduleName: str, mainClassName: str, msg: str, text: str) -> None:
		super().__init__(moduleName, mainClassName, msg)
		self.text = text

	def getText(self):
		return self.text

	@property
	def needsSave(self):
		return True


class InFileCompileResult(ICompileResult):
	__slots__ = ()

	def __init__(self, moduleName: str, mainClassName: str, msg: str, path):
		super().__init__(moduleName, mainClassName, msg)
		self.path = path

	def getText(self):
		with self.path.open("rt", encoding="utf-8") as f:
			return f.read()

	@property
	def needsSave(self):
		return False

	def __repr__(self) -> str:
		return self.__class__.__name__ + "<" + repr(self.path) + ">"


class PostprocessResult(InMemoryCompileResult):
	__slots__ = ()

	def __init__(self, result, postprocessors: list) -> None:
		super().__init__(moduleName=result.moduleName, mainClassName=result.mainClassName, msg=result.msg, text=result.getText())
		for postprocessor in postprocessors:
			self.text = postprocessor(self.text)


class IPrefsStorage:
	def __init__(self, namespaces=None, destDir: str = None, additionalFlags: typing.Iterable[str] = (), importPath=None, verbose: typing.Optional[typing.Iterable[str]] = None, opaqueTypes: typing.Optional[bool] = None, autoRead: typing.Optional[bool] = None, readStoresPos: typing.Optional[bool] = None, target: str = "python"):
		raise NotImplementedError()


class ICompiler:
	__slots__ = ("progressCallback", "dirs", "namespaces", "importPath")

	def __init__(self, progressCallback=None, dirs=None, namespaces=None, importPath: typing.Optional[Path] = None) -> None:
		if progressCallback is None:

			def progressCallback(x):
				return None
				#progressCallback = print

		self.progressCallback = progressCallback

		if dirs is None or isinstance(dirs, str):
			dirs = KSCDirs(subDirsNames, root=dirs)
		self.dirs = dirs

		self.namespaces = namespaces
		self.importPath = importPath

	def prepareSourceFilePath(self, sourceFilePath):
		sourceFilePath = Path(sourceFilePath).absolute()
		if not sourceFilePath.exists():
			raise KaitaiCompilerException("Source file " + str(sourceFilePath) + " doesn't exist")
		return sourceFilePath

	def compile(self, sourceFilesPaths: typing.Iterable[Path], destDir: Path, additionalFlags: typing.Iterable[str] = None, needInMemory: bool = False, target: str = "python", verbose: typing.Optional[typing.Iterable[str]] = None, opaqueTypes: typing.Optional[bool] = None, autoRead: typing.Optional[bool] = None, readStoresPos: typing.Optional[bool] = None) -> typing.Mapping[str, ICompileResult]:
		if destDir is not None:
			destDir = Path(destDir).absolute()
		else:
			#We don't emit a warning here because `needInMemory` is a hint that we prefer avoiding disk writes
			needInMemory = True

		sourceFilesPaths = [self.prepareSourceFilePath(p) for p in sourceFilesPaths]
		return self.compile_(sourceFilesAbsPaths=sourceFilesPaths, destDir=destDir, additionalFlags=additionalFlags, verbose=verbose, opaqueTypes=opaqueTypes, autoRead=autoRead, readStoresPos=readStoresPos, needInMemory=needInMemory, target=target)

	def compile_(self, sourceFilesAbsPaths: typing.Iterable[Path], destDir: Path, additionalFlags: typing.Iterable[str], needInMemory: bool, target: str, verbose, opaqueTypes, autoRead, readStoresPos) -> typing.Iterable[ICompileResult]:
		raise NotImplementedError()
