import pathlib
from collections import defaultdict
from collections.abc import Sequence

import pandas as pd
from attrs import define, field

from .vocalization import Vocalization


@define
class Dataset:
    COLUMNS = ("audio_path", "spect_path", "annot_path", "annot_format")

    vocalizations: Sequence[Vocalization] = field()

    @vocalizations.validator
    def are_all_vocalizations(self, attribute, value):
        if not all([isinstance(item, Vocalization) for item in value]):
            raise ValueError("all items passed in must be a Vocalization")

    def to_df(self) -> pd.DataFrame:
        records = defaultdict(list)
        for vocalization in self.vocalizations:
            for key in self.COLUMNS:
                records[key].append(getattr(vocalization, key))

        df = pd.DataFrame.from_records(records, columns=self.COLUMNS)
        return df

    def to_csv(self, csv_path: [str, pathlib.Path]) -> None:
        df = self.to_df()
        df.to_csv(csv_path)

    def to_sqlite(self):
        return NotImplemented
