"""fixtures relating to annotation files"""
import pytest


@pytest.fixture
def annot_file_yarden(source_test_data_root):
    return source_test_data_root.joinpath(
        "spect_mat_annot_yarden", "llb3", "llb3_annot_subset.mat"
    )


@pytest.fixture
def annot_dir_notmat(source_test_data_root):
    return source_test_data_root.joinpath("audio_cbin_annot_notmat", "gy6or6", "032312")


@pytest.fixture
def annot_files_notmat(annot_dir_notmat):
    return sorted(annot_dir_notmat.glob("*.not.mat"))


@pytest.fixture
def annot_file_birdsongrec(source_test_data_root):
    return source_test_data_root.joinpath(
        "audio_wav_annot_birdsongrec", "Bird0", "Annotation.xml"
    )
