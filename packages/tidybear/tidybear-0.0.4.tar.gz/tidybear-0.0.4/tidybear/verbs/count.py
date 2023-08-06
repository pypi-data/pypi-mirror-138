from __future__ import annotations

from typing import List
from typing import Union

from pandas import DataFrame


def count(
    df: DataFrame,
    columns: Union[List[str], str],
    *,
    sort: bool = False,
    name: str = "n",
) -> DataFrame:
    """Quickly count the unique values of one or more variables.

    Parameters
    ----------
    df : DataFrame
        The dataframe to use
    columns : str or list
        The column(s) to group by.
    sort : bool
        If True, will show the largest groups at the top, by default False
    name: str
        What to rename the new column with counts. By default "n" is used.
    """

    counts = df.groupby(columns).size().rename(name).reset_index()

    if sort:
        return counts.sort_values(name, ascending=False)
    else:
        return counts.sort_values(columns)
