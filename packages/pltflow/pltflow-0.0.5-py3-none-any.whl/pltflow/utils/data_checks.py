from typing import Union

import numpy as np
import pandas as pd


def check_column_is_numeric(df: pd.DataFrame, column: str) -> None:
    try:
        df[column].astype("float64")
    except ValueError:
        print(
            f"""
            {column} is not a numerical python type.
            Notes based on only one axis can only be perfom on numerical columns")
            """
        )


def check_array_is_numeric(data: Union[pd.Series, list, np.ndarray]) -> None:
    try:
        pd.Series(data).astype("float64")
    except ValueError:
        print(
            """
            The data provided is not completely numerical.
            """
        )
