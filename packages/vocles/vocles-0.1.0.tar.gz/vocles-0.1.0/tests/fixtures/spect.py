"""fixtures relating to array files containing spectrograms"""
import pytest


@pytest.fixture
def spect_dir_mat(source_test_data_root):
    return source_test_data_root.joinpath("spect_mat_annot_yarden", "llb3", "spect")


@pytest.fixture
def spect_dir_npz(source_test_data_root):
    return sorted(
        source_test_data_root.joinpath(
            "audio_cbin_annot_notmat",
            "gy6or6",
            "032312",
        ).glob("spectrograms_generated*")
    )[0]


@pytest.fixture
def spect_list_mat(spect_dir_mat):
    return sorted(spect_dir_mat.glob("*.mat"))


@pytest.fixture
def spect_list_npz(spect_dir_npz):
    return sorted(spect_dir_npz.glob("*.spect.npz"))
