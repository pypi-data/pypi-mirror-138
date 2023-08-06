"""Tests the predict function in predict.py."""
from src.model.predict import make_prediction_inputs
from src.preprocessing.datamanager import preprocess_input

TOTAL_FEATURES = [
    "Gender",
    "Smoke",
    "Diabetes",
    "Age",
    "Ejection Fraction",
    "Sodium",
    "Creatinine",
    "Pletelets",
    "Creatinine phosphokinase",
    "Blood Pressure",
    "Hemoglobin",
    "Height",
    "Weight",
    "BMI",
]

# sample input with no smoking and baseline CK
sample_input_0 = [
    "Male",
    "No",  # smoking
    "Normal",
    75,
    "Low",
    134,
    2.5,
    224000,
    350,  # CK
    162,
    13,
    140,
    47,
    23.97959183673469,
]

# sample input with smoking
sample_input_1 = [
    "Male",
    "Yes",  # smoking
    "Normal",
    75,
    "Low",
    134,
    2.5,
    224000,
    350,
    162,
    13,
    140,
    47,
    23.97959183673469,
]

# sample input with increased CK
sample_input_2 = [
    "Male",
    "No",  # smoking
    "Normal",
    75,
    "Low",
    134,
    2.5,
    224000,
    550,  # CK
    162,
    13,
    140,
    47,
    23.97959183673469,
]


def test_predict():
    """
    Post train test where known factors (smoking/ CK) should affect survival rate negatively.

    :return: None
    """
    processed_sample_input_0 = preprocess_input(sample_input_0)
    processed_sample_input_1 = preprocess_input(sample_input_1)
    processed_sample_input_2 = preprocess_input(sample_input_2)

    pred_proba_processed_sample_input_0 = make_prediction_inputs(
        processed_sample_input_0, proba=True
    )
    pred_proba_processed_sample_input_1 = make_prediction_inputs(
        processed_sample_input_1, proba=True
    )
    pred_proba_processed_sample_input_2 = make_prediction_inputs(
        processed_sample_input_2, proba=True
    )

    # survival rate for sample input 0 should be higher than sample input 1
    assert (
        pred_proba_processed_sample_input_0[0][1]
        > pred_proba_processed_sample_input_1[0][1]
    )

    # survival rate for sample input 0 should be higher than sample input 2
    assert (
        pred_proba_processed_sample_input_0[0][1]
        > pred_proba_processed_sample_input_2[0][1]
    )
