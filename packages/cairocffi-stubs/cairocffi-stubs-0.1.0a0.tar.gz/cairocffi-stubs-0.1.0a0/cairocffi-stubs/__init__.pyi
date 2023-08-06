from .constants import *
from .context import Context as Context
from .fonts import FontFace as FontFace, FontOptions as FontOptions, ScaledFont as ScaledFont, ToyFontFace as ToyFontFace
from .matrix import Matrix as Matrix
from .patterns import Gradient as Gradient, LinearGradient as LinearGradient, Pattern as Pattern, RadialGradient as RadialGradient, SolidPattern as SolidPattern, SurfacePattern as SurfacePattern
from .surfaces import ImageSurface as ImageSurface, PDFSurface as PDFSurface, PSSurface as PSSurface, RecordingSurface as RecordingSurface, SVGSurface as SVGSurface, Surface as Surface, Win32PrintingSurface as Win32PrintingSurface, Win32Surface as Win32Surface
from .xcb import XCBSurface as XCBSurface
from typing import Any, Iterable, Tuple

VERSION: str
version: str
version_info: Tuple[int, int, int]


def dlopen(
    ffi: Any, library_names: Iterable[str], filenames: Iterable[str]
) -> Any:
    ...


cairo: Any


class CairoError(Exception):
    status: Any

    def __init__(self, message: str, status: Any) -> None:
        ...


Error = CairoError
STATUS_TO_EXCEPTION: Any


def cairo_version() -> int:
    ...


def cairo_version_string() -> str:
    ...


def install_as_pycairo() -> None:
    ...
