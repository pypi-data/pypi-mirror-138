"""Manages all of the data processing."""
import sqlite3 as sq3

import joblib
import numpy as np
import pandas as pd

from src.config.config import TOTAL_FEATURES


def preprocess_input(inputs: list) -> pd.DataFrame:
    """
    Preprocess inputs from streamlit or list of observations. It will return a pandas dataframe with the columns.

    :param inputs: list of input conforming with the columns of the database
    :return: Pandas dataframe of the list
    """
    inputs = np.array(inputs).reshape(1, -1)
    rename_cols = {k: v for k, v in zip(range(len(TOTAL_FEATURES)), TOTAL_FEATURES)}
    df = pd.DataFrame(inputs).rename(columns=rename_cols)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess inputs from database file.

    :param df: list of input conforming with the columns of the database
    :return: Processed pandas dataframe
    """
    df.drop(columns=["ID", "Favorite color"], inplace=True)

    bound_numerical_features(df)

    df.Smoke = df.Smoke.replace("NO", "No")
    df.Smoke = df.Smoke.replace("YES", "Yes")
    df.Age = np.where(df.Age < 0, -df.Age, df.Age)
    df["Ejection Fraction"] = (
        df["Ejection Fraction"].replace("L", "Low").replace("N", "Normal")
    )
    df["Ejection Fraction"] = (
        df["Ejection Fraction"]
        .replace("High", "Normal")
        .replace("Normal", "Normal-High")
    )

    df.Survive = df.Survive.str.replace("No", "0")
    df.Survive = df.Survive.str.replace("Yes", "1")
    df.Survive = df.Survive.astype("int")
    df["BMI"] = (df.Weight / df.Height / df.Height) * 10000

    return df


def load_from_database(db_path: str) -> pd.DataFrame:
    """
    Load up the database into a pandas dataframe and returns it.

    :param db_path: str containing the path of the database
    :return: pandas dataframe
    """
    con = sq3.Connection(db_path)

    query = """SELECT * FROM SURVIVE"""
    df: pd.DataFrame = pd.read_sql(query, con)

    df_processed = preprocess_data(df)
    return df_processed


def load_pipeline(pipe_path: str):
    """
    Load the pipeline from a path.

    :param pipe_path:str containing the path to the pipeline
    :return: the pipeline
    """
    pipe = joblib.load(filename=pipe_path)
    return pipe


def return_min_max_boxplot(df, col, min_or_max):
    """
    Return upper(3rd quartile-1.5 of inter-quartile range) or lower(1rd quartile+1.5 of inter-quartile range).

    :param df : dataframe
    :param col: the col of the dataframe
    :param min_or_max : the upper(max) or lower(min) of the inner fence boxplot value
    :return: (float) upper(max) or lower(min) of the inner fence boxplot value
    """
    df_col_q1 = np.quantile(df[col], 0.25, method="midpoint")
    df_col_q3 = np.quantile(df[col], 0.75, method="midpoint")
    df_col_itr = df_col_q3 - df_col_q1
    df_col_min_cap = df_col_q1 - (1.5 * df_col_itr)
    df_col_max_cap = df_col_q3 + (1.5 * df_col_itr)
    if "min" in min_or_max:
        return df_col_min_cap
    else:
        return df_col_max_cap


def bound_outliers(df: pd.DataFrame, col: str):
    """
    Squeezes outliers to within the boxplot inner fences.

    :param df: dataframe
    :param col: the col of the dataframe
    :return: None
    """
    df_col_max = return_min_max_boxplot(df, col, "max")
    df_col_min = return_min_max_boxplot(df, col, "min")
    df[col] = np.where(df[col] >= df_col_max, df_col_max, df[col])
    df[col] = np.where(df[col] <= df_col_min, df_col_min, df[col])


def bound_numerical_features(df: pd.DataFrame):
    """
    Bounds any outliers found in numerical features of a pandas dataframe in the box plot distribution.

    :param df: pd.DataFrame Numerical dataframe
    :return: None
    """
    num_cols = df.select_dtypes(include=["int", "float"]).columns.to_list()
    for col in num_cols:
        bound_outliers(df, col)
