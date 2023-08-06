import pandas as pd

from molgenis.capice.vep.template import Template


class MotifEScoreChange(Template):
    def __init__(self):
        super(MotifEScoreChange, self).__init__(
            name='MOTIF_SCORE_CHANGE',
            usable=True
        )

    @property
    def columns(self):
        return ['motifEScoreChng']

    def _process(self, dataset: pd.DataFrame):
        dataset = dataset.join(
            pd.DataFrame(pd.Series(dataset[self.name].tolist()), columns=self.columns)
        )
        return dataset
