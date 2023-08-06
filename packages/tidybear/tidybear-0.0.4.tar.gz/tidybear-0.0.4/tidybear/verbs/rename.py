from typing import Any

from pandas import DataFrame


def rename(df: DataFrame, *args: Any, **kwargs: Any) -> DataFrame:
    """Rename the columns of a dataframe

    You can use this function is a few different ways.
    - Use a list of strings to be used as the new column names.
      In this case the length of the list must equal the number
      of columns in the dataframe.
    - Use the new column names as arguments to the function.
      Again the number of arguments passed must equal the number
      of columns in the dataframe.
    - Use a dictionary with the keys as existing column names and
      values as the new column names.
    - Use keyword arguments with the key as existing column names
      and values as the new columns names.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    DataFrame

    Examples
    --------

    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>>
    >>> df = pd.DataFrame({"A": [1, 2],"B": [3, 4]})
    >>> df
    A  B
    0  1  3
    1  2  4
    >>> tb.rename(df, ["X", "Y"])
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, "X", "Y")
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, {"A": "X", "B": "Y"})
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, A="X", B="Y")
    X  Y
    0  1  3
    1  2  4
    ```
    """
    df = df.copy()
    if len(kwargs) > 0:
        return df.rename(columns=kwargs)

    if len(args) == 1 and isinstance(args[0], dict):
        return df.rename(columns=args[0])

    if len(args) >= 1:
        new_cols = args[0] if isinstance(args[0], list) else list(args)

        assert len(new_cols) == df.shape[1], (
            f"Number of columns provided ({len(new_cols)}) "
            f"does not match the number of features in the dataframe ({df.shape[1]})."
        )

        df.columns = new_cols
        return df

    return df
