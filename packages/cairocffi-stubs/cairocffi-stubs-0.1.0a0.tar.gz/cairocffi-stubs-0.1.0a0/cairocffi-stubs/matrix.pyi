from typing import Iterable, Optional, Tuple


class Matrix:
    def __init__(
        self,
        xx: float = ...,
        yx: float = ...,
        xy: float = ...,
        yy: float = ...,
        x0: float = ...,
        y0: float = ...,
    ) -> None:
        ...

    @classmethod
    def init_rotate(cls, radians: float) -> Matrix:
        ...

    def as_tuple(self) -> Tuple[float, float, float, float, float, float]:
        ...

    def copy(self) -> Matrix:
        ...

    def __getitem__(self, index: int) -> float:
        ...

    def __iter__(self) -> Iterable[float]:
        ...

    def __eq__(self, other: Matrix) -> bool:
        ...

    def __ne__(self, other: Matrix) -> bool:
        ...

    def multiply(self, other: Matrix) -> Matrix:
        ...

    def __mul__(self, other: Matrix) -> Matrix:
        ...

    def translate(self, tx: float, ty: float) -> None:
        ...

    def scale(self, sx: float, sy: Optional[float] = ...) -> None:
        ...

    def rotate(self, radians: float) -> None:
        ...

    def invert(self) -> None:
        ...

    def inverted(self) -> Matrix:
        ...

    def transform_point(self, x: float, y: float) -> Tuple[float, float]:
        ...

    def transform_distance(self, dx: float, dy: float) -> Tuple[float, float]:
        ...

    xx: float
    yx: float
    xy: float
    yy: float
    x0: float
    y0: float
