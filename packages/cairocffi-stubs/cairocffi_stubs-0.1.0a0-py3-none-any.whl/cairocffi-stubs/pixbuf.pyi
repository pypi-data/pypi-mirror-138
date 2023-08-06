from typing import Any, Callable, Optional, Tuple

from cairocffi.surfaces import ImageSurface


class ImageLoadingError(ValueError):
    ...


class Pixbuf:
    def __init__(self, pointer: Any) -> None:
        ...

    def __getattr__(self, name: str) -> Callable[..., Any]:
        ...


def decode_to_image_surface(
    image_data: bytes,
    width: Optional[int] = ...,
    height: Optional[int] = ...
) -> Tuple[ImageSurface, str]:
    ...
