"""fixtures relating to audio files"""
import pytest


@pytest.fixture
def audio_dir_cbin(source_test_data_root):
    return source_test_data_root.joinpath("audio_cbin_annot_notmat", "gy6or6", "032312")


@pytest.fixture
def audio_list_cbin(audio_dir_cbin):
    return sorted(audio_dir_cbin.glob("*.cbin"))


@pytest.fixture
def audio_dir_wav(source_test_data_root):
    return source_test_data_root.joinpath(
        "audio_wav_annot_birdsongrec", "Bird0", "Wave"
    )


@pytest.fixture
def audio_list_wav(audio_dir_wav):
    return sorted(audio_dir_wav.glob("*.wav"))
