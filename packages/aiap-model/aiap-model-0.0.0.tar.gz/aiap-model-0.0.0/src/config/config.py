"""Contains all of the constant variables used."""
import os
from pathlib import Path

# main folders
CONFIG_PATH = os.path.dirname(__file__)  # aiap/src/config
SRC_ROOT = Path(CONFIG_PATH).parent  # aiap/src
ROOT = Path(SRC_ROOT).parent  # aiap

DATA_PATH = os.path.join(ROOT, "data")  # aiap/data
MODEL_PATH = os.path.join(SRC_ROOT, "model")  # aiap/src/model
PREPROCESSING_PATH = os.path.join(SRC_ROOT, "preprocessing")  # aiap/src/preprocessing

# Objects
DATABASE_PATH = os.path.join(DATA_PATH, "survive.db")  # aiap/data/survive.db
SAMPLE_DATA_PATH = os.path.join(DATA_PATH, "sample_df.csv")  # aiap/data/sample_df.csv
PIPELINE_NAME = "pipeline.pkl"
PIPELINE_PATH = os.path.join(MODEL_PATH, PIPELINE_NAME)  # aiap/src/model/pipeline.pkl
LOG_OUTPUT_NAME = "log_file.txt"
LOG_OUTPUT_PATH = os.path.join(
    MODEL_PATH, LOG_OUTPUT_NAME
)  # aiap/src/model/log_file.txt

# model specific objects
MODEL_NAME = "Random Forest"
RANDOM_SEED = 42
CV = 5
TEST_RATIO = 0.2
PARAMS = {}  # insert params configuration here

# data base specific objects
ORI_FEATURES = [
    [
        "ID",
        "Survive",
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
        "Favorite color",
    ]
]
TARGET = ["Survive"]
CAT_FEATURES = ["Gender", "Smoke", "Diabetes", "Ejection Fraction"]
ORI_NUM_FEATURES = [
    "Sodium",
    "Creatinine",
    "Pletelets",
    "Creatinine phosphokinase",
    "Blood Pressure",
    "Hemoglobin",
    "Height",
    "Weight",
]
TOTAL_NUM_FEATURES = [
    "Age",
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
TOTAL_FEATURES_W_TARGET = TARGET + TOTAL_FEATURES

# streamlit-specific objects
ST_AGE_DEAFULT = 21
ST_SODIUM_DEFAULT = 120
ST_CREATININE_DEFAULT = 0.2
ST_PLETELETS_DEFAULT = 266000
ST_CK_DEFAULT = 100
ST_BP_DEFAULT = 105
ST_HEMO_DEFAULT = 16.3
ST_HEIGHT_DEFAULT = 185
ST_WEIGHT_DEFAULT = 80
