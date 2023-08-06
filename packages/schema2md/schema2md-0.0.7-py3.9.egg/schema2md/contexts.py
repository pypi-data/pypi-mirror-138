import sys
from dataclasses import dataclass
from typing import Optional, TextIO

from pyrsistent import pmap, pvector
from pyrsistent.typing import PMap, PVector

from schema2md.declarations import REQUIRED_KEY, JObj
from schema2md.reference import Reference
from schema2md.tab import Tab


class Context:
    def __init__(
        self,
        globalc: "Context.GlobalC",
        localc: "Optional[Context.LocalC]" = None,
    ) -> None:
        self.globalc = globalc
        self.localc = localc or self.LocalC.default()

    @dataclass
    class GlobalC:
        schema: JObj
        output_stream: TextIO

    @dataclass
    class LocalC:
        tab: Tab
        keyspath: PVector[str]
        objectpath: PVector[JObj]
        reference_history: PMap[Reference, str]

        @staticmethod
        def clone_from(other: "Context.LocalC") -> "Context.LocalC":
            return Context.LocalC(
                tab=other.tab,
                keyspath=other.keyspath,
                objectpath=other.objectpath,
                reference_history=other.reference_history,
            )

        def update(self, **kwargs) -> "Context.LocalC":
            new_local = Context.LocalC.clone_from(self)
            for (k, v) in kwargs.items():
                assert k in new_local.__dict__
                setattr(new_local, k, v)
            return new_local

        @staticmethod
        def default() -> "Context.LocalC":
            return Context.LocalC(
                tab=Tab(base_size=2),
                keyspath=pvector(["root"]),
                objectpath=pvector([{}]),
                reference_history=pmap({Reference("#"): "root"}),
            )

    @staticmethod
    def default(root: JObj, output_stream: TextIO = sys.stdout) -> "Context":
        return Context(
            globalc=Context.GlobalC(schema=root, output_stream=output_stream)
        )

    def write(self, line: str) -> None:
        for l in filter(len, line.rstrip().split("\n")):
            self.globalc.output_stream.write(f"{self.localc.tab}{l}\n")

    def write_empty(self) -> None:
        self.globalc.output_stream.write("\n")

    def resolve_global_reference(self, ref: Reference) -> JObj:
        curr = self.globalc.schema
        for k in ref.non_root_sections:
            curr = curr[k]  # type: ignore
        return curr

    def mark_local_reference_as_seen(self, ref: Reference) -> "Context":
        curr_keyspath = ".".join(self.localc.keyspath)
        new_history = self.localc.reference_history.set(ref, curr_keyspath)
        return Context(
            globalc=self.globalc,
            localc=self.localc.update(reference_history=new_history),
        )

    def indent(self, n: int = 1) -> "Context":
        tab = self.localc.tab
        return Context(globalc=self.globalc, localc=self.localc.update(tab=tab + n))

    def append_to_keyspath(self, key: str) -> "Context":
        keyspath = self.localc.keyspath
        return Context(
            globalc=self.globalc,
            localc=self.localc.update(keyspath=keyspath.append(key)),
        )

    def append_to_objectpath(self, o: JObj) -> "Context":
        objectpath = self.localc.objectpath
        return Context(
            globalc=self.globalc,
            localc=self.localc.update(objectpath=objectpath.append(o)),
        )

    @property
    def current_key(self) -> str:
        return self.localc.keyspath[-1]

    @property
    def parent_obj(self) -> JObj:
        return self.localc.objectpath[-1]

    @property
    def keyspath(self) -> PVector[str]:
        return self.localc.keyspath

    @property
    def keyspath_excluding_root(self) -> str:
        return ".".join(self.keyspath[1:])

    @property
    def is_required(self) -> bool:
        return self.current_key in self.parent_obj.get(REQUIRED_KEY, [])  # type: ignore
