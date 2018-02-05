import warnings
from collections import OrderedDict
from pathlib import Path
from pkg_resources import EntryPoint

from . import ICompiler as ICompilerModule
from . import defaults, utils
from .KaitaiCompilerException import KaitaiCompilerException

defaultPriority = 0


class BackendDescriptor:
	__slots__ = ("entryPoint", "name", "prio", "issues")

	def __init__(self, entryPoint: EntryPoint, name: str, prio: int = defaultPriority, issues: set = None) -> None:
		self.entryPoint = entryPoint
		self.name = name
		self.prio = prio
		if issues:
			issues = set(issues)
		self.issues = issues

	@property
	def broken(self) -> bool:
		return self.prio < 0


def recognizeBackends(b: EntryPoint) -> BackendDescriptor:
	if hasattr(b.__class__, "__slots__") and "metadata" in b.__class__.__slots__:
		metadata = b.metadata
	else:
		encoded = b.name.split("@", 1)
		b.name = encoded[0]
		if len(encoded) > 1:
			try:
				metadata = utils.json.loads(encoded[1])
			except BaseException:
				warnings.warn("Entry point " + repr(b) + " is invalid. The value after @ must be must be a valid JSON!.")
				return BackendDescriptor(b, b.name, prio=-1)  # broken, so not using
		else:
			metadata = None

	if metadata is not None:
		if isinstance(metadata, int):
			return BackendDescriptor(b, b.name, prio=metadata)  # it is priority
		elif isinstance(metadata, dict):
			return BackendDescriptor(b, b.name, **metadata)
		else:
			warnings.warn("Entry point " + repr(b) + " is invalid. The value after @ must be must be eithera dict, or a number!.")
			return BackendDescriptor(b, b.name, prio=-1)  # broken, so not using
	else:
		return BackendDescriptor(b, b.name)


def discoverBackends() -> OrderedDict:
	import pkg_resources

	pts = pkg_resources.iter_entry_points(group="kaitai_struct_compile")
	backendsList = sorted(filter(lambda b: not b.broken, map(recognizeBackends, pts)), key=lambda b: b.prio, reverse=True)
	return OrderedDict(((b.name, b) for b in backendsList))


discoveredBackends = discoverBackends()


def selectBackend(tolerableIssues=None, backendsPresent=None, forcedBackend=None) -> None:
	if backendsPresent is None:
		backendsPresent = discoveredBackends
	if tolerableIssues is None:
		tolerableIssues = utils.getTolerableIssuesFromEnv()

	if forcedBackend is None:
		forcedBackend = utils.getForcedBackendFromEnv()

	if forcedBackend:
		backendsPresent = {forcedBackend: backendsPresent[forcedBackend]}

	for b in backendsPresent.values():
		if b.issues:
			if b.issues - tolerableIssues:
				continue

		try:
			init = b.entryPoint.load()
			return init(ICompilerModule, KaitaiCompilerException, utils, defaults)
		except Exception as ex:
			warnings.warn(repr(ex) + " when loading backend " + b.entryPoint.name)
			pass


ChosenBackend = selectBackend()
