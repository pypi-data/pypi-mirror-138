from typing import Any
from typing import Callable

from pandas import DataFrame


def mutate(
    df: DataFrame,
    **kwargs: Callable[..., Any],
) -> DataFrame:
    """Create a new column in a dataframe using applied functions

    ```python
    tb.mutate(df, col_squared=lambda x: x.col**2)
    ```

    Parameters
    ----------
    df : DataFrame
    new_name : str
        the name of the new column to create
    definition : function
        the function to apply

    Returns
    -------
    DataFrame
    """

    df = df.copy()

    for name, definition in kwargs.items():
        df[name] = df.apply(definition, axis=1)

    return df
