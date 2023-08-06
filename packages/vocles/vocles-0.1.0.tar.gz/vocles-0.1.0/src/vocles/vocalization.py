import pathlib
from typing import Optional

from attrs import converters, define, field


@define
class Vocalization:
    audio_path: Optional[pathlib.Path] = field(
        converter=converters.optional(pathlib.Path), default=None
    )
    spect_path: Optional[pathlib.Path] = field(
        converter=converters.optional(pathlib.Path), default=None
    )
    annot_path: Optional[pathlib.Path] = field(
        converter=converters.optional(pathlib.Path), default=None
    )
    annot_format: Optional[str] = field(
        converter=converters.optional(str), default=None
    )

    def __attrs_post_init__(self):
        if self.audio_path is None and self.spect_path is None:
            raise ValueError(
                "a Vocalization must have either an audio_path or a spect_path, but both were None"
            )
