from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

import pandas as pd


def pivot_wider(
    df: pd.DataFrame,
    *,
    names_from: str = "name",
    values_from: Union[List[str], str] = "value",
    fill_value: Optional[Any] = None,
    prefix_names: bool = False,
) -> pd.DataFrame:
    """
    Transform a dataframe from long to wide

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    names_from : str
        The column name to pivot on
    values_from : str, List[str]
        The column name to pivot on
        If multiple names are passed, the columns will be <value>_<name>
    fill_value : Optional[Any]
        The value to fill in the new column

    >>> df = pd.DataFrame({"idx": [1, 2], "name": ["a", "a"], "value": [3, 4]})
    >>> pivot_wider(df)
       idx  a
    0    1  3
    1    2  4

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    if isinstance(values_from, str):
        values_from = [values_from]

    index_cols = [c for c in df.columns if c not in [names_from, *values_from]]
    df = df.pivot(index=index_cols, columns=names_from, values=values_from)

    if len(values_from) == 1 and not prefix_names:
        df.columns = [name for _, name in df.columns.to_flat_index()]
    else:
        df.columns = [f"{value}_{name}" for value, name in df.columns.to_flat_index()]

    if fill_value is not None:
        df = df.fillna(fill_value)

    return df.reset_index()


def pivot_longer(
    df: pd.DataFrame,
    cols: Union[str, List[str]],
    *,
    names_to: str = "name",
    values_to: str = "value",
    cols_are: Literal["index", "targets"] = "index",
    drop_na: bool = True,
) -> pd.DataFrame:
    """
    Transform a dataframe from wide to long

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    cols : List[str]
        The column name to pivot if "flip_cols=False"
        otherwise the columns to use as index
    names_to : str
        The column name to pivot on
    values_to : str
        The column name to pivot on
    cols_are : str, optional
        'index' or 'targets'
    drop_na : bool, optional
        Whether to drop rows with missing values, default True

    Examples
    --------

    >>> df = pd.DataFrame({"idx": [1, 2], "a": [1, 2], "b": [1, 2]})
    >>> pivot_longer(df, "idx")
       idx name  value
    0    1    a      1
    1    1    b      1
    2    2    a      2
    3    2    b      2

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    if isinstance(cols, str):
        cols = [cols]

    if cols_are == "index":
        index_cols = cols
    elif cols_are == "targets":
        index_cols = [c for c in df.columns if c not in cols]
    else:
        raise ValueError(
            f"cols_are must be one of 'index' or 'targets', not {cols_are}"
        )

    df = df.set_index(index_cols)
    df = df.stack(dropna=False).reset_index()

    new_cols = index_cols + [names_to, values_to]
    df.columns = new_cols

    if drop_na:
        df = df.dropna()

    return df
