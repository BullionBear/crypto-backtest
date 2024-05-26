import argparse
import zipfile
import os
import csv
import logging
import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process and append CSV files from ZIP archives.')
    parser.add_argument('--symbol', type=str, help='target symbol aim to containing ZIP files')
    parser.add_argument('--dst-file', type=str, help='Destination file path to append CSV data')
    return parser.parse_args()


def process_zip_files(src_folder, dst_file):
    header = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'count', 'taker_buy_volume',
        'taker_buy_quote_volume', 'ignore'
    ]
    # Ensure the source folder exists
    if not os.path.exists(src_folder):
        logging.error(f"The source folder {src_folder} does not exist.")
        return

    # Create or open the destination file
    with open(dst_file, 'a', newline='') as f_out:
        csv_writer = csv.writer(f_out)
        # Write the header if the file is empty
        if os.stat(dst_file).st_size == 0:
            csv_writer.writerow(header)

        # List and sort all zip files in the directory
        zip_files = sorted([file for file in os.listdir(src_folder) if file.endswith('.zip')])
        for zip_file in tqdm.tqdm(zip_files):
            zip_path = os.path.join(src_folder, zip_file)
            logging.info(f"Processing file: {zip_path}")

            with zipfile.ZipFile(zip_path, 'r') as zfile:
                # Each ZIP contains exactly one CSV file
                csv_files = [f for f in zfile.namelist() if f.endswith('.csv')]
                for csv_file in csv_files:
                    logging.info(f"Reading CSV file: {csv_file}")
                    with zfile.open(csv_file) as f_csv:
                        csv_reader = csv.reader(f_csv.read().decode('utf-8').splitlines())
                        for row in csv_reader:
                            csv_writer.writerow(row)


if __name__ == '__main__':
    args = parse_arguments()
    symbol = args.symbol
    src_folder = f"/Users/yite/crypto_data/binance/data/spot/daily/klines/{symbol.upper()}/1s"
    process_zip_files(src_folder, args.dst_file)
