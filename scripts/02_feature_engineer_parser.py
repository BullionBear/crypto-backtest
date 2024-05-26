import argparse
import csv
import math
import backtest.feature_handler as feature_handler


class FeatureProcessor:
    def __init__(self):
        self.log_return_handler = feature_handler.LogReturnHandler()
        self.n_features = 15
        self.ma_handlers = {f"ma_{30 * 2 ** i}": feature_handler.MovingAverageHandler(30 * 2 ** i, 86400 * 30)
                            for i in range(self.n_features)}

    def read(self, price):
        self.log_return_handler.read(price)
        if not self.log_return_handler.is_valid():
            return
        log_return = self.log_return_handler.get()
        for name, ma_handler in self.ma_handlers.items():
            ma_handler.read(log_return)

    def get(self):
        features = {"log_return": self.log_return_handler.get()}
        features.update({feature: handler.get() for feature, handler in self.ma_handlers.items()})
        return features

    def header(self):
        return ["log_return"] + list(self.ma_handlers.keys())


def process_csv(input_file_path, output_file_path):
    processor = FeatureProcessor()
    # Open the input CSV file
    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + processor.header()

        # Open the output file to write the updated data
        with open(output_file_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                processor.read(float(row['close']))
                feature = processor.get()
                row.update(feature)
                writer.writerow(row)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Process a CSV file to add logarithm of closing prices.')
    parser.add_argument('-s', '--source', type=str, required=True, help='The path to the input CSV file')
    parser.add_argument('-d', '--destination', type=str, required=True, help='The path to the output CSV')

    # Parse the arguments
    args = parser.parse_args()

    # Process the CSV file
    process_csv(args.source, args.destination)


if __name__ == "__main__":
    main()