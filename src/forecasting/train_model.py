import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_parquet(
    "ml/training_sales.parquet"
)

df["month"] = df["event_date"].dt.month

df["day_of_week"] = (
    df["event_date"].dt.dayofweek
)

df = pd.get_dummies(
    df,
    columns=[
        "category",
        "brand",
        "region"
    ],
    drop_first=True
)

X = df.drop(
    columns=[
        "event_date",
        "revenue"
    ]
)

y = df["revenue"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(
    f"MAE: {mae}"
)

model_columns = X.columns.tolist()

print(
    pd.Series(
        model.feature_importances_,
        index=model_columns
    ).sort_values(
        ascending=False
    )
)

joblib.dump(
    model,
    "ml/artifacts/revenue_forecast.pkl"
)

joblib.dump(
    model_columns,
    "ml/artifacts/model_columns.pkl"
)