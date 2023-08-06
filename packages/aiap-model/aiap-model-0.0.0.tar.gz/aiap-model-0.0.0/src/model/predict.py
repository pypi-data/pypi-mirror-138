"""Contains function to return prediction of input."""
from src.config.config import PIPELINE_PATH
from src.preprocessing import datamanager


def make_prediction_inputs(input_data: list, proba=False) -> int:
    """
    Load pipeline and preprocess input then predict.

    Parameters
    ----------
    input_data: List
        Input data from streamlit application, expects 1 row of observation
    proba: Bol
        True if return probability instead
    Returns
    -------
    Int | Float
        Int: If proba is not set to True. Returns class of survival. 0 for no, 1 for yes
        Float: If proba is set to True, the probability of survival [0,1]
    """
    survive_pipeline = datamanager.load_pipeline(PIPELINE_PATH)
    processed_input = datamanager.preprocess_input(input_data)
    if proba:
        prediction_proba = survive_pipeline.predict_proba(processed_input)
        return prediction_proba
    else:
        prediction = survive_pipeline.predict(processed_input)
        return prediction
