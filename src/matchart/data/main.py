import pandas as pd

from .core.main import DataProperties, DataContainer, DataFactory


class Data:
    """Orchestrates data modules for different chart types."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def bar(self, properties: DataProperties) -> DataContainer:
        """Prepare data for bar plots."""

        data = DataFactory(self.df).build(properties=properties)

        return data

    def line(self, properties: DataProperties, running_total: bool) -> DataContainer:
        """Prepare data for line plots."""

        data = DataFactory(self.df).build(properties=properties)

        if running_total:
            data = DataContainer(
                pivot=data.pivot.cumsum().round(2),
                df=data.df,
                index=data.index,
                values=data.values,
                columns=data.columns,
                agg_func=data.agg_func,
            )

        return data
