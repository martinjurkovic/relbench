import duckdb
import pandas as pd

from relbench.base import Database, EntityTask, RecommendationTask, Table, TaskType
from relbench.metrics import (
    accuracy,
    average_precision,
    f1,
    link_prediction_map,
    link_prediction_precision,
    link_prediction_recall,
    mae,
    r2,
    rmse,
    roc_auc,
)

class CustomersTask(EntityTask):
    r"""Predict the number of customers for each store."""

    task_type = TaskType.REGRESSION
    entity_col = "Store"
    entity_table = "historical"
    time_col = "Date"
    target_col = "Customers"
    timedelta = pd.Timedelta(days=7)
    metrics = [r2, mae, rmse]

    def make_table(self, db: Database, timestamps: "pd.Series[pd.Timestamp]") -> Table:
        historical = db.table_dict["historical"].df
        historical_removed_cols = db.table_dict["historical"].removed_cols

        df = duckdb.sql(
            f"""
            SELECT
                h.Date as {self.time_col},
                h.Store as {self.entity_col},
                historical_removed_cols.Customers as {self.target_col}
            FROM
                historical h
            LEFT JOIN
                historical_removed_cols
            ON
                h.Store = historical_removed_cols.Store
            """
        ).df()

        return Table(
            df=df,
            fkey_col_to_pkey_table={self.entity_col: self.entity_table},
            pkey_col=None,
            time_col=self.time_col,
        )