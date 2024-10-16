import os
import shutil
from pathlib import Path

import pandas as pd

from relbench.base import Database, Dataset, Table


class RossmannDataset(Dataset):
    # Train for the most recent 1 year out of 2 years of the original
    # time period
    val_timestamp = pd.Timestamp("2014-09-01")
    test_timestamp = pd.Timestamp("2014-09-10")

    def make_db(self) -> Database:
        path = os.path.join("data", "original", "rossmann_subsampled")
        store = os.path.join(path, "store.csv")
        historical = os.path.join(path, "historical.csv")
        if not os.path.exists(store) or not os.path.exists(historical):
            raise RuntimeError(
                """Dataset not found.
                    Put dataset into 'data/original/rossmann_subsampled' folder.
                    Inside should be 'store.csv' and 'historical.csv'.
                    """
            )

        store_df = pd.read_csv(store)
        historical_df = pd.read_csv(historical)
        historical_df["Date"] = pd.to_datetime(historical_df["Date"], format="%Y-%m-%d")

        db = Database(
            table_dict={
                "store": Table(
                    df=store_df,
                    fkey_col_to_pkey_table={},
                    pkey_col="Store",
                ),
                "historical": Table(
                    df=historical_df,
                    fkey_col_to_pkey_table={"Store": "store"},
                    time_col="Date",
                ),
            }
        )

        db = db.from_(pd.Timestamp("2014-07-31"))

        return db
