import csv
import math

# Open your CSV file
with open('./data/btcusdt_data.csv', mode='r', newline='') as file:
    # Create a DictReader object
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    fieldnames = reader.fieldnames + ['log_price']

    # Open a new file to write the updated data
    with open('./data/btcusdt_feature.csv', mode='w', newline='') as outfile:
        # Create a DictWriter object with the updated fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write the header to the new file
        writer.writeheader()

        # Iterate over each row in the original file
        for row in reader:
            # Compute the log of the price and add it to the row under 'log_price' key
            if row['close']:  # Ensure there is a value in 'close'
                row['log_price'] = math.log(float(row['close']))
            else:
                row['log_price'] = None  # If no value, set as None or an appropriate value

            # Write the updated row to the new file
            writer.writerow(row)
