
import os

import skops.io as sio
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import ElasticNet, LinearRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def train_model(kc_data):
    drop_lst = [
        "price",
        "sqft_price",
        "date",
        "delta_lat",
        "delta_long",
    ]

    all_features = [x for x in kc_data.columns if x not in drop_lst]
    X = kc_data[all_features]
    y = kc_data.price

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    for variables in (["grade"], ["grade", "last_known_change"]):
        model_lin_reg = LinearRegression()
        model_lin_reg.fit(X_train[variables], y_train)

        print(
            "Adj. R²:",
            round(
                1
                - (1 - model_lin_reg.score(X_test[variables], y_test))
                * (X_test.shape[0] - 1)
                / (X_test.shape[0] - len(variables) - 1),
                2,
            ),
        )

    poly = PolynomialFeatures(2)

    X_train_poly = X_train.drop(columns=["id"])
    X_test_poly = X_test.drop(columns=["id"])

    X_train_sq = poly.fit_transform(X_train_poly)
    X_test_sq = poly.transform(X_test_poly)

    model_lin_reg = LinearRegression()
    model_lin_reg.fit(X_train_sq, y_train)

    print(
        "Adj. R²:",
        round(
            1
            - (1 - model_lin_reg.score(X_test_sq, y_test))
            * (X_test_sq.shape[0] - 1)
            / (X_test_sq.shape[0] - X_test_sq.shape[1] - 1),
            2,
        ),
    )

    param_grid = {
        "model__regressor__alpha": [0.01, 0.1, 1],
        "model__regressor__l1_ratio": [0.2, 0.5, 0.8],
    }

    elastic_pipeline = Pipeline([
        ("polynomial", PolynomialFeatures(2, include_bias=False)),
        ("scaler", StandardScaler()),
        (
            "model",
            TransformedTargetRegressor(
                regressor=ElasticNet(
                    max_iter=5000,
                    tol=1e-4,
                    precompute=True,
                ),
                transformer=StandardScaler(),
            ),
        ),
    ])

    elastic_cv = GridSearchCV(
        elastic_pipeline,
        param_grid,
        cv=5,
        scoring="r2",
        verbose=2,
        n_jobs=1,
        error_score="raise",
    )

    elastic_cv.fit(X_train_poly, y_train)

    elastic = elastic_cv.best_estimator_

    print("Best parameters:", elastic_cv.best_params_)
    print("Test R²:", round(elastic.score(X_test_poly, y_test), 3))

    os.makedirs("model", exist_ok=True)

    with open("model/model.bin", "wb") as f_out:
        sio.dump(elastic, f_out)

    return elastic
