from dataclasses import dataclass


@dataclass(frozen=True)
class Tab:
    n: int = 0
    base_size: int = 2

    def __add__(self, other: int) -> "Tab":
        return Tab(self.n + other, self.base_size)

    def __repr__(self) -> str:
        return " " * (self.base_size * self.n)
