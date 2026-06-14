import polars as pl
from pathlib import Path
import os
import logging

# Setup logging
log_file = "app.log"
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        pass


def read_and_convert_csv_to_parquet(csv_path, parquet_path):
    try:
        # Read CSV file using Polars
        df = pl.read_csv(csv_path)

        # Convert all columns to string type
        df = df.with_columns([pl.col("*").cast(pl.Utf8)])

        # Write DataFrame to Parquet file
        df.write_parquet(parquet_path)

        logging.info(f"CSV converted and saved as Parquet: {parquet_path}")
    except Exception as e:
        logging.error(f"Error during conversion: {e}")


if __name__ == "__main__":
    csv_path = "employees.csv"
    parquet_path = "employees.parquet"

    read_and_convert_csv_to_parquet(csv_path, parquet_path)
