import os
from typing import Dict, Optional

import manta_lab.util as manta_util
from manta_lab.dtypes._interface import BatchableMedia, MEDIA_TEMP_DIR


class Audio(BatchableMedia):
    _log_type = "audio"

    # from arguments
    _sample_rate: Optional[str]
    _caption: Optional[str]
    # from __init__
    _duration: Optional[str]
    # from _set_file
    _path: Optional[str]
    _is_tmp: Optional[str]
    _extension: Optional[str]
    _digest: Optional[str]
    _size: Optional[str]

    def __init__(self, data_or_path, sample_rate=None, caption: Optional[str] = None) -> None:
        super().__init__()

        self._sample_rate = sample_rate
        self._caption = caption

        self._duration = None

        if isinstance(data_or_path, str):
            self._init_from_path(data_or_path)
        elif isinstance(data_or_path, Audio):
            self._init_from_manta_audio(data_or_path)
        else:
            if sample_rate is None:
                raise ValueError('Argument "sample_rate" is required when instantiating manta_lab.Audio with raw data.')
            self._init_from_data(data_or_path, sample_rate)

    def _init_from_path(self, path):
        self._set_file(path, is_tmp=False)

    def _init_from_data(self, data, sample_rate):
        soundfile = manta_util.get_module(
            "soundfile",
            required='Raw audio requires the soundfile package. To get it, run "pip install soundfile"',
        )

        temp_path = os.path.join(MEDIA_TEMP_DIR.name, manta_util.generate_id() + ".wav")
        soundfile.write(temp_path, data, sample_rate)
        self._duration = len(data) / float(sample_rate)

        self._set_file(temp_path, is_tmp=True)

    def _init_from_manta_audio(self, audio):
        self._sample_rate: audio._sample_rate
        self._caption: audio._caption
        self._duration: audio._duration
        self._path = audio._path
        self._is_tmp = audio._is_tmp
        self._extension = audio._extension
        self._digest = audio._digest
        self._size = audio._size

    @classmethod
    def from_json(cls, json_obj, artifact):
        # TODO: Implement
        return cls(
            artifact.get_path(json_obj["path"]).download(),
            caption=json_obj["caption"],
        )

    def to_json(self) -> Dict:
        json_dict = super().to_json()
        json_dict.update(
            {
                "_type": Audio._log_type,
                "caption": self._caption,
            }
        )
        return json_dict

    def bind_run(
        self,
        run,
    ) -> None:
        super().bind_run(run)

    def upload_file(self, key, step):
        super().upload_file(key, step)

    @staticmethod
    def get_media_subdir():
        return os.path.join("media", "audio")

    @staticmethod
    def seq_to_json(seq):
        jsons = [obj.to_json() for obj in seq]

        json_dict = {
            "_type": "audios",
            "count": len(seq),
            "contents": jsons,
            "captions": Audio.all_captions(seq),
            "sampleRates": Audio.all_sample_rates(seq),
            "durations": Audio.all_durations(seq),
        }
        return json_dict

    @staticmethod
    def all_durations(audio_list):
        return [a._duration for a in audio_list]

    @staticmethod
    def all_sample_rates(audio_list):
        return [a._sample_rate for a in audio_list]

    @staticmethod
    def all_captions(audio_list):
        captions = [a._caption for a in audio_list]
        return ["" if c is None else c for c in captions]
