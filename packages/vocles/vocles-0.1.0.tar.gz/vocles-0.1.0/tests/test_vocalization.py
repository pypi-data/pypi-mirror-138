from pathlib import Path

import pytest

import vocles


@pytest.mark.parametrize(
    "audio_path, spect_path, annot_path, annot_format",
    [
        ("./path/to/audio.wav", None, None, None),
        (None, "./path/to/spect.npz", None, None),
        ("./path/to/audio.wav", "./path/to/spect.npz", None, None),
        (Path("./path/to/audio.wav"), None, None, None),
        (None, Path("./path/to/spect.npz"), None, None),
        (Path("./path/to/audio.wav"), Path("./path/to/spect.npz"), None, None),
        ("./path/to/audio.wav", None, "./path/to/aud.txt", "aud-txt"),
        (None, "./path/to/spect.npz", "./path/to/aud.txt", "aud-txt"),
        ("./path/to/audio.wav", "./path/to/spect.npz", "./path/to/aud.txt", "aud-txt"),
        (Path("./path/to/audio.wav"), None, Path("./path/to/aud.txt"), "aud-txt"),
        (None, Path("./path/to/spect.npz"), Path("./path/to/aud.txt"), "aud-txt"),
        (
            Path("./path/to/audio.wav"),
            Path("./path/to/spect.npz"),
            Path("./path/to/aud.txt"),
            "aud-txt",
        ),
    ],
)
def test_vocalization(audio_path, spect_path, annot_path, annot_format):
    vocal = vocles.Vocalization(
        audio_path=audio_path,
        spect_path=spect_path,
        annot_path=annot_path,
        annot_format=annot_format,
    )
    assert isinstance(vocal, vocles.Vocalization)
    for attr_name, attr_val in zip(
        (
            "audio_path",
            "spect_path",
            "annot_path",
            "annot_format",
        ),
        (audio_path, spect_path, annot_path, annot_format),
    ):
        val_from_instance = getattr(vocal, attr_name)
        if attr_val is None:
            assert val_from_instance is None
        elif isinstance(attr_val, str) and attr_name == "annot_format":
            assert val_from_instance == attr_val
        elif isinstance(attr_val, str) and attr_name != "annot_format":
            assert val_from_instance == Path(attr_val)
        else:
            assert val_from_instance == attr_val


def test_vocalization_raises():
    with pytest.raises(ValueError):
        vocles.Vocalization(audio_path=None, spect_path=None)
