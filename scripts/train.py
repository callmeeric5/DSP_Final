import pandas as pd
import joblib
from xgboost import XGBRegressor
from scripts.config import MODEL_PATH, CATEGORICAL_FEATURES
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from scripts.preprocess import preprocess, make_encoder


def split_data(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    X = df.drop(columns=["User_ID", "Product_ID", 'Purchase'])
    y = df["Purchase"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def train(
        df: pd.DataFrame,
        categorical_columns: list = CATEGORICAL_FEATURES,
) -> dict:
    X_train, X_test, y_train, y_test = split_data(df)
    make_encoder(X_train, categorical_columns)
    X_train = preprocess(X_train)

    X_test = preprocess(X_test)

    model = make_model(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)


    return r2


def make_model(
        X_train: pd.DataFrame, y_train: pd.Series, path: str = MODEL_PATH
) -> XGBRegressor:
    model = XGBRegressor()
    model.fit(X_train, y_train)
    joblib.dump(model, path)
    return model
