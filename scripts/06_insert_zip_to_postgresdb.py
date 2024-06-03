import argparse
import zipfile
import os
import json
import logging
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
import tqdm


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description="Insert zipped csv data into PostgreSQL using batches")
    parser.add_argument("--config", type=str, required=True, help="Path to the JSON config file")
    return parser.parse_args()


def process_zip_files(src_folder, connection, table_config):
    header = table_config['column']
    # Ensure the source folder exists
    if not os.path.exists(src_folder):
        logging.error(f"The source folder {src_folder} does not exist.")
        return

    # List and sort all zip files in the directory
    zip_files = sorted([file for file in os.listdir(src_folder) if file.endswith('.zip')])
    logging.info(f"{zip_files=}")
    for zip_file in tqdm.tqdm(zip_files):
        zip_path = os.path.join(src_folder, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zfile:
            # Each ZIP contains exactly one CSV file
            csv_files = [f for f in zfile.namelist() if f.endswith('.csv')]
            for csv_file in csv_files:
                logging.info(f"Reading CSV file: {csv_file}")
                with zfile.open(csv_file) as f_csv:
                    df = pd.read_csv(f_csv, names=header)
                    if not df.empty:
                        logging.info(f"Inserting {len(df)} rows from {csv_file}")
                        insert_data_to_db(df, connection, table_config['name'])


def insert_data_to_db(df, connection, table_name):
    df = df.where(pd.notnull(df), None)  # Replace NaN with None for SQL compatibility
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES %s"
    cursor = connection.cursor()
    try:
        execute_values(cursor, query, tuples)
        connection.commit()
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def main():
    args = parse_args()
    config = load_config(args.config)
    dbconfig = config['postgres']
    table_config = config['table']
    logging.info(f"Connect to {dbconfig}")
    # Database connection setup
    connection = psycopg2.connect(
        dbname=dbconfig['dbname'],
        user=dbconfig['user'],
        password=dbconfig['password'],
        host=dbconfig['host'],
        port=dbconfig['port']
    )
    logging.info(f"Connect success")
    try:
        # Process CSV files
        process_zip_files(config["zipfolder"], connection, table_config)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
