import pathlib

import pytest

import vocles


def _get_vocalizations(
    audio_paths,
    spect_paths,
    annot_paths,
    annot_format,
):
    """helper function that builds a list of Vocalizations.
    Factored out to make core logic of unit test below more readable.

    creates a zip (audio_paths, spect_paths, annot_paths)
    to iterate over, and then builds Vocalizations with tuples from zip
    """
    # below, whenever any 'paths' variable is None,
    # we convert it to a list of Nones,
    # so we can zip it with the real paths and iterate over all of them
    if audio_paths is not None and spect_paths is not None:
        assert len(audio_paths) == len(spect_paths)

    elif audio_paths is not None and spect_paths is None:  # just audio, no spect
        spect_paths = [spect_paths] * len(audio_paths)

    elif spect_paths is not None and audio_paths is None:  # just spect, no audio
        audio_paths = [audio_paths] * len(spect_paths)

    # after we deal with audio and/or spect paths, handle annotation paths
    if annot_paths is not None:
        if isinstance(annot_paths, pathlib.Path) or isinstance(
            annot_paths, str
        ):  # just one annot file
            annot_paths = [annot_paths] * len(audio_paths)
        elif isinstance(annot_paths, list):
            assert len(annot_paths) == len(audio_paths) == len(spect_paths)
    else:  # no annotation
        annot_paths = [annot_paths] * len(audio_paths)

    assert (
        len(annot_paths) == len(audio_paths) == len(spect_paths)
    )  # should be True by this point no matter what
    zipped = zip(audio_paths, spect_paths, annot_paths)
    vocalizations = []
    for audio_path, spect_path, annot_path in zipped:
        vocalizations.append(
            vocles.Vocalization(
                audio_path=audio_path,
                spect_path=spect_path,
                annot_path=annot_path,
                annot_format=annot_format,
            )
        )
    return vocalizations


@pytest.mark.parametrize(
    "audio_format, spect_format, annot_format, path_as_str",
    [
        ("cbin", None, None, False),
        ("cbin", "npz", None, False),
        ("cbin", "npz", "notmat", False),
        ("cbin", None, None, "audio_paths"),
        ("cbin", "npz", None, ["audio_paths", "spect_paths"]),
        ("cbin", "npz", "notmat", ["audio_paths", "spect_paths", "annot_paths"]),
        ("wav", None, None, False),
        ("wav", None, "birdsongrec", False),
        ("wav", None, None, "audio_paths"),
        ("wav", None, "birdsongrec", ["audio_paths", "annot_paths"]),
        (None, "mat", None, False),
        (None, "mat", "yarden", False),
        (None, "mat", None, "spect_paths"),
        (None, "mat", "yarden", ["spect_paths", "annot_paths"]),
    ],
)
def test_dataset(audio_format, spect_format, annot_format, path_as_str, paths_factory):
    # this test is very verbose.
    # thought about making it a fixture, but then we'd have
    # one of the core classes inside a fixture. Seems weird.
    # Basically this test replicates in miniature a user workflow,
    # so we have to go through step-by-step getting files,
    # instantiating Vocalizations, before we actually test the dataset
    audio_paths, spect_paths, annot_paths = paths_factory(
        audio_format, spect_format, annot_format, path_as_str=path_as_str
    )

    vocalizations = _get_vocalizations(
        audio_paths,
        spect_paths,
        annot_paths,
        annot_format,
    )

    dataset = vocles.Dataset(vocalizations=vocalizations)
    assert isinstance(dataset, vocles.Dataset)
    assert hasattr(dataset, "vocalizations")
    assert isinstance(dataset.vocalizations, list)
    assert len(dataset.vocalizations) == len(vocalizations)
    assert all([vocal in dataset.vocalizations for vocal in vocalizations])
