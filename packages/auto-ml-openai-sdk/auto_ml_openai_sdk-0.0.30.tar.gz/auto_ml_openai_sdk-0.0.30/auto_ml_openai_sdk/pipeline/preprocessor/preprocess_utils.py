from typing import Tuple

import numpy as np
import pandas as pd


def data_shuffle(data_path: str) -> pd.DataFrame:
    """Shuffle the data randomly.

    Parameters
    ----------
    data_path : str
        the local path of the data

    Returns
    -------
    Dataframe
        shuffled dataframe

    """
    df = pd.read_csv(data_path)
    df = df.sample(frac=1)  # type: ignore
    df.to_csv(data_path, index=False)
    return df


def data_split(
    data_path: str,
    test_data_proportion: float,
    prompt_col_name: str = "prompt",
    completion_col_name: str = "completion",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the provided data.

    Parameters
    ----------
    data_path : str
        the local path of the data
    test_data_proportion : float
        the proportion of the test data for splitting
    prompt_col_name : str
        the name of the column in the dataframe which will be used as prompt
    completion_col_name : str
        the name of the column in the dataframe which will be used as completion

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        training dataframe and test dataframe

    """
    df = pd.read_csv(data_path)
    df[prompt_col_name] = df[prompt_col_name] + "->"

    has_nan = df[completion_col_name].isnull().values.any()
    if has_nan:
        df[completion_col_name].fillna(value="NULL", inplace=True)
    label = df[completion_col_name]
    train, test = train_test_split(df, label, test_data_proportion)
    if has_nan:
        train[completion_col_name].replace(
            to_replace="NULL", value=np.nan, inplace=True
        )
        test[completion_col_name].replace(to_replace="NULL", value=np.nan, inplace=True)

    return train, test


def train_test_split(
    df: pd.DataFrame, label: pd.Series, test_data_proportion: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the data into train and test.

    Parameters
    ----------
    df : Dataframe
        the source dataframe
    label : Series
        the completion/label column value of the dataframe
    test_data_proportion : float
        the proportion of the test data for splitting

    Returns
    -------
    Dataframe, Dataframe
        train dataframe and test dataframe

    """
    labels = np.random.choice(
        label.unique(), replace=False, size=int(label.nunique() * test_data_proportion)  # type: ignore
    )
    df_test = df[label.isin(labels)]
    df_train = df[~label.isin(labels)]
    return df_train, df_test


def save_jsonl(
    df: pd.DataFrame, save_path: str, prompt_col_name: str, completion_col_name: str
) -> None:
    """Save json files ready for training or testing.

    Parameters
    ----------
    df : Dataframe
        the source dataframe
    save_path : str
        the path where the json files to be saved
    prompt_col_name : str
        the name of the column in the dataframe which will be used as prompt
    completion_col_name : str
        the name of the column in the dataframe which will be used as completion

    """
    df = df[[prompt_col_name, completion_col_name]]
    df.columns = ["prompt", "completion"]
    df.to_json(save_path, orient="records", lines=True)
