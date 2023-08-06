from typing import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Reference:
    ref: str

    @property
    def sections(self) -> Sequence[str]:
        return self.ref.split("/")

    @property
    def non_root_sections(self) -> Sequence[str]:
        return self.sections[1:]

    @property
    def key(self) -> str:
        sections = self.sections
        return sections[-1] if len(sections) > 1 else "root"

    def __hash__(self) -> int:
        return hash(self.ref)

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Reference):
            return self.ref == obj.ref
        return False
