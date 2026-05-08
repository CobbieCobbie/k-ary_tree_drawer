from dataclasses import dataclass


@dataclass
class Vertex:
    id: int
    coordinates: tuple[float, float]
    height: int

    @property
    def x(self) -> float:
        return self.coordinates[0]

    @property
    def y(self) -> float:
        return self.coordinates[1]

    def __repr__(self) -> str:
        return (
            f"Vertex(id={self.id}, "
            f"coordinates=({self.x}, {self.y}), "
            f"height={self.height})"
        )

    # dataclass generates __eq__ based on fields; make it hashable for use as dict key
    def __hash__(self) -> int:
        return hash(self.id)
