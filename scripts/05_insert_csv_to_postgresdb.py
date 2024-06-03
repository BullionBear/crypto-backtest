import argparse
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description="Load CSV data into PostgreSQL using batches")
    parser.add_argument("--config", type=str, required=True, help="Path to the JSON config file")
    return parser.parse_args()


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def insert_data_to_db(df, connection, table_config):
    cursor = connection.cursor()
    # Correctly constructing SQL statement for execute_values
    columns = ', '.join(table_config['column'])
    # The %s here is a placeholder for the whole VALUES list that execute_values will format
    sql = f"INSERT INTO {table_config['name']} ({columns}) VALUES %s"
    data_tuples = [tuple(x) for x in df.to_numpy()]

    execute_values(cursor, sql, data_tuples, page_size=len(data_tuples))
    connection.commit()
    logging.info(f"Inserted {len(data_tuples)} records successfully.")


def main():
    args = parse_args()
    config = load_config(args.config)
    dbconfig = config['postgres']
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
        # Process CSV file in chunks

        for chunk in pd.read_csv(config['csvfile'], chunksize=config['batch']):
            insert_data_to_db(chunk, connection, config['table'])
    finally:
        connection.close()


if __name__ == "__main__":
    main()
