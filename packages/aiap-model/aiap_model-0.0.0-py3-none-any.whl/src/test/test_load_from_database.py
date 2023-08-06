"""Tests the load from database function."""
import pandas as pd

from src.config.config import DATABASE_PATH, SAMPLE_DATA_PATH, TOTAL_FEATURES_W_TARGET
from src.preprocessing.datamanager import load_from_database, preprocess_data

sample_data = pd.read_csv(SAMPLE_DATA_PATH)
processed_sample_data = preprocess_data(sample_data)

sample_input = [
    "Male",
    "Yes",
    "Normal",
    21,
    "Low",
    120,
    0.2,
    266000,
    100,
    105,
    16.3,
    185,
    80,
    23.374726077428782,
]


def test_load_from_database():
    """
    Checks if the columns retrieved are all present.

    :return: None
    """
    sample_database = load_from_database(DATABASE_PATH)

    assert sample_database.columns.to_list() == TOTAL_FEATURES_W_TARGET
