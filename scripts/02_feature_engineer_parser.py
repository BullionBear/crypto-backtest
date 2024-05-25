import argparse
import csv
import math
import backtest.feature_handler as feature_handler


def process_csv(input_file_path, output_file_path):
    # Open the input CSV file
    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['log_price']

        # Open the output file to write the updated data
        with open(output_file_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row['close']:  # Check if there is a value in 'close'
                    row['log_price'] = math.log(float(row['close']))
                else:
                    row['log_price'] = None

                writer.writerow(row)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Process a CSV file to add logarithm of closing prices.')
    parser.add_argument('-s', '--source', type=str, required=True, help='The path to the input CSV file')
    parser.add_argument('-d', '--destination', type=str, required=True, help='The path to the output CSV file with the added log price')

    # Parse the arguments
    args = parser.parse_args()

    # Process the CSV file
    process_csv(args.source, args.destination)


if __name__ == "__main__":
    main()