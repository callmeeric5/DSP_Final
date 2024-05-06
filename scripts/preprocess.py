from sklearn.preprocessing import OrdinalEncoder
import joblib
import pandas as pd
from .__init__ import CATEGORICAL_FEATURES, NUMERICAL_FEATURES, ENCODER_PATH


def preprocess(
    df: pd.DataFrame,
    categorical_columns: list = CATEGORICAL_FEATURES,
    encoder_path: str = ENCODER_PATH,
) -> pd.DataFrame:
    df = fill_features_nulls(df)

    df = encode_categorical(df, categorical_columns, encoder_path)

    return df


def make_encoder(
    df: pd.DataFrame, categorical_columns: list, path: str = ENCODER_PATH
) -> joblib:
    encoder = OrdinalEncoder()
    encoder.fit(df[categorical_columns])
    joblib.dump(encoder, path)


def encode_categorical(
    df: pd.DataFrame, categorical_columns: list, path: str = ENCODER_PATH
) -> pd.DataFrame:
    encoder = joblib.load(path)
    encoded_columns = encoder.transform(df[categorical_columns])
    df[categorical_columns] = pd.DataFrame(encoded_columns, columns=categorical_columns)
    df.reset_index()
    return df


def fill_features_nulls(
    df: pd.DataFrame,
    categorical_columns: list = CATEGORICAL_FEATURES,
    continuous_columns: list = NUMERICAL_FEATURES,
) -> pd.DataFrame:
    df[continuous_columns] = df[continuous_columns].fillna(
        df[continuous_columns].mean()
    )
    for feature in categorical_columns:
        df[feature] = df[feature].fillna(df[feature].mode()[0])

    return df
