"""fixtures relating to paths"""
import pathlib

import pytest


@pytest.fixture
def paths_factory(
    annot_file_birdsongrec,
    annot_files_notmat,
    annot_file_yarden,
    audio_list_cbin,
    audio_list_wav,
    spect_list_mat,
    spect_list_npz,
):
    audio_format_list_map = {
        "cbin": audio_list_cbin,
        "wav": audio_list_wav,
        None: None,
    }

    spect_format_list_map = {
        "mat": spect_list_mat,
        "npz": spect_list_npz,
        None: None,
    }

    annot_format_file_map = {
        "birdsongrec": annot_file_birdsongrec,
        "notmat": annot_files_notmat,
        "yarden": annot_file_yarden,
        None: None,
    }

    def _paths_for_dataset(audio_format, spect_format, annot_format, path_as_str=False):

        audio_paths = audio_format_list_map[audio_format]
        spect_paths = spect_format_list_map[spect_format]
        annot_paths = annot_format_file_map[annot_format]

        if audio_paths is not None and spect_paths is not None:
            # extra logic to deal with how ``vak`` preps a dataset;
            # only keep audio paths that have corresponding spectrograms
            audio_paths_from_spect = [
                # below Path(path.stem).stem converts '.cbin.spect.mat' --> '.cbin'
                pathlib.Path(spect_path.stem).stem
                for spect_path in spect_paths
            ]
            audio_paths = [
                audio_path
                for audio_path in audio_paths
                if audio_path.name in audio_paths_from_spect
            ]

        if annot_paths is not None:
            # only need to modify list of annot paths
            if isinstance(annot_paths, list):
                # extra logic to deal with how ``vak`` preps a dataset;
                # only keep annot paths that have corresponding audio path
                audio_path_names = [audio_path.name for audio_path in audio_paths]
                annot_paths = [
                    annot_path
                    for annot_path in annot_paths
                    # below Path(path.stem).stem converts '.cbin.not.mat' --> '.cbin'
                    if pathlib.Path(annot_path.stem).stem in audio_path_names
                ]

        # make dict so we can modify val based on key
        paths_dict = dict(
            audio_paths=audio_paths,
            spect_paths=spect_paths,
            annot_paths=annot_paths,
        )

        if path_as_str is not False:
            if isinstance(path_as_str, str):  # e.g. 'spect_path'
                # make a list so we can iterate over it
                path_as_str = [path_as_str]
            for these_paths in path_as_str:
                the_paths = paths_dict[these_paths]
                if isinstance(the_paths, list):
                    the_paths = [str(path) for path in the_paths]
                elif isinstance(the_paths, pathlib.Path):
                    the_paths = str(the_paths)
                paths_dict[these_paths] = the_paths

        return (
            paths_dict["audio_paths"],
            paths_dict["spect_paths"],
            paths_dict["annot_paths"],
        )

    return _paths_for_dataset
