# Employee Data Conversion Project

## Overview

This project converts an employee data CSV file (`employees.csv`) into a Parquet file using the Polars library.

## Files and Structure

- `employees.csv`: The input CSV file containing employee data.
- `script.py`: The Python script to read the CSV, convert it to Parquet, and save it.
- `requirements.txt`: Lists the project dependencies.
- `app.log`: Log file for storing information and error messages.

## Installation

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To convert the CSV to a Parquet file, run the script:

```sh
python script.py
```

The script will read `employees.csv`, convert it to Parquet, and save it as `employees.parquet` in the same directory. Log messages will be recorded in `app.log`.

## Logging

- The script uses basic logging to write information and error messages to `app.log`.
- You can view the log file by opening `app.log` with a text editor.

## Notes

- The Parquet file will have all columns as string data types.
- Ensure your Python environment has the necessary permissions to read/write files in the current directory.

Feel free to modify the script or add more features as needed!