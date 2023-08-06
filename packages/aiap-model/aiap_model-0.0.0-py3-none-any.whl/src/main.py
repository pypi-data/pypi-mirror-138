#! /usr/bin/env python
"""Runs the application on streamlit."""

import streamlit as st

from src.config.config import (
    ST_AGE_DEAFULT,
    ST_BP_DEFAULT,
    ST_CK_DEFAULT,
    ST_CREATININE_DEFAULT,
    ST_HEIGHT_DEFAULT,
    ST_HEMO_DEFAULT,
    ST_PLETELETS_DEFAULT,
    ST_SODIUM_DEFAULT,
    ST_WEIGHT_DEFAULT,
)
from src.model.predict import make_prediction_inputs


def run_streamlit():
    """
    Establish the streamlit UI when run.

    :return: None
    """
    st.title("Predicting Survival of coronary artery disease")

    st.write("Choose inputs below")

    st_gender = str(st.radio("Gender", ("Male", "Female")))
    st_smoker = str(st.radio("Smoker", ("Yes", "No")))
    st_diabetes = str(
        st.radio("Diabetic Condition?", ("Normal", "Pre-diabetes", "Diabetes"))
    )
    st_age = float(st.number_input("Age", value=ST_AGE_DEAFULT))
    st_ejection_fraction = str(st.radio("Ejection Fraction", ("Low", "Normal-High")))
    st_sodium = float(st.number_input("Sodium (mg/dL)", value=ST_SODIUM_DEFAULT))
    st_creatinine = float(
        st.number_input("Creatinine (md/dL)", value=ST_CREATININE_DEFAULT)
    )
    st_pletelets = int(
        st.number_input("Pletelets (kilo-platelets/mL)", value=ST_PLETELETS_DEFAULT)
    )
    st_ck = int(
        st.number_input("Creatinine Phosphokinase (mcg/L)", value=ST_CK_DEFAULT)
    )
    st_bp = int(st.number_input("Blood pressure(mmHG)", value=ST_BP_DEFAULT))
    st_hemo = float(st.number_input("Hemoglobin (g/dL)", value=ST_HEMO_DEFAULT))
    st_height = int(st.number_input("Height in cm", value=ST_HEIGHT_DEFAULT))
    st_weight = int(st.number_input("Weight in Kg", value=ST_WEIGHT_DEFAULT))

    inputs = [
        st_gender,
        st_smoker,
        st_diabetes,
        st_age,
        st_ejection_fraction,
        st_sodium,
        st_creatinine,
        st_pletelets,
        st_ck,
        st_bp,
        st_hemo,
        st_height,
        st_weight,
    ]

    if st.button("Predict"):

        bmi = (st_weight / st_height / st_height) * 10000
        inputs.append(bmi)
        prediction = make_prediction_inputs(inputs)
        predict_proba = make_prediction_inputs(inputs, proba=True)
        if prediction == 0:
            st.write(
                "Prediction is "
                + strip_brackets(prediction)
                + " with probability "
                + strip_brackets(predict_proba[0][prediction])
            )
            st.write("Please see a doctor!")
        else:
            st.write(
                "Prediction is "
                + strip_brackets(prediction)
                + " with probability "
                + strip_brackets(predict_proba[0][prediction])
            )
            st.write("Please keep up the healthy habits")


def strip_brackets(_string: str) -> str:
    """
    Strip the brackets [ ] out of strings and returns it without brackets.

    :param _string: a string with brackets
    :Returns: string without brackets
    """
    return str(_string).replace("[", "").replace("]", "")


if __name__ == "__main__":
    run_streamlit()
