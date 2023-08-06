"""tests the pipeline function."""
import numpy as np
import pandas as pd

from src.config.config import SAMPLE_DATA_PATH
from src.model.pipeline import transform_pipe
from src.preprocessing.datamanager import preprocess_data


def test_pipeline():
    """
    Test no Na values from pipeline output.

    :return: None
    """
    sample_data = pd.read_csv(SAMPLE_DATA_PATH)
    processed_sample_data = preprocess_data(sample_data)

    transformed_processed_sample_data = transform_pipe.fit_transform(
        processed_sample_data
    )

    assert np.all(pd.DataFrame(transformed_processed_sample_data).isna()).sum() == 0
