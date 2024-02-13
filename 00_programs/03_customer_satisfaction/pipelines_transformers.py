from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from workalendar.america import Brazil

cal = Brazil()


class DateImputer(TransformerMixin):
    def __init__(self, date_columns):
        self.date_columns = date_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.date_columns:
            X_transformed[col] = X_transformed[col].fillna("2099-12-31 00:00:00")
        for col in self.date_columns:
            X_transformed.loc[:, col] = pd.to_datetime(X_transformed[col])
        X_transformed["wd_estimated_delivery_time"] = X_transformed.apply(
            lambda x: cal.get_working_days_delta(
                x.order_approved_at, x.order_estimated_delivery_date
            ),
            axis=1,
        )
        X_transformed["wd_actual_delivery_time"] = X_transformed.apply(
            lambda x: cal.get_working_days_delta(
                x.order_approved_at, x.order_delivered_customer_date
            ),
            axis=1,
        )

        # Calculate the time between the actual and estimated delivery date. If negative was delivered early, if positive was delivered late.
        X_transformed["wd_delivery_time_delta"] = (
            X_transformed.wd_actual_delivery_time
            - X_transformed.wd_estimated_delivery_time
        )

        # Calculate the time between the actual and estimated delivery date. If negative was delivered early, if positive was delivered late.
        X_transformed["is_late"] = (
            X_transformed.order_delivered_customer_date
            > X_transformed.order_estimated_delivery_date
        )
        cols2drop = [
            "order_approved_at",
            "order_estimated_delivery_date",
            "order_delivered_customer_date",
        ]
        X_transformed.drop(cols2drop, axis=1, inplace=True)
        return X_transformed


class VolumeCalculator(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed["volume_of_product"] = (
            X_transformed["product_length_cm"]
            * X_transformed["product_height_cm"]
            * X_transformed["product_width_cm"]
        )
        X_transformed["volume_weight_ratio"] = (
            X_transformed["product_weight_g"] / X_transformed["volume_of_product"]
        )
        return X_transformed
