"""test the bound outliers function."""
import pandas as pd

from src.config.config import ORI_NUM_FEATURES, SAMPLE_DATA_PATH
from src.preprocessing.datamanager import bound_outliers, preprocess_data

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


def test_bound_outliers():
    """
    Test if the outliers have been cap to the min or max.

    :return: None
    """
    arbitary_value = 1
    for col in ORI_NUM_FEATURES:
        ori_min = processed_sample_data[col].min()
        ori_max = processed_sample_data[col].max()

        bound_outliers(processed_sample_data, col)

        current_min = processed_sample_data[col].min()
        current_max = processed_sample_data[col].max()

        assert ori_min - arbitary_value <= current_min
        assert ori_max + arbitary_value >= current_max
