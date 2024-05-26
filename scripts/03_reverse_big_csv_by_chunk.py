import argparse
import pandas as pd
import os
import shutil
import gc
import tqdm


def reverse_by_chunk(input_file_path, output_file_path, chunk_size):
    chunks = pd.read_csv(input_file_path, chunksize=chunk_size)
    basename = os.path.basename(output_file_path).split('.')[0]
    tmpdir = 'tmp'
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    for i, chunk in enumerate(chunks):
        chunk = chunk.iloc[::-1].reset_index(drop=True)
        chunk.to_csv(f"tmp/{basename}_{str(i).zfill(4)}.csv", index=False)
    return tmpdir


def merge_files_in_reverse(output_file_path, chunk_folder):
    first_file = True
    csv_files = sorted([file for file in os.listdir(chunk_folder) if file.endswith('.csv')], reverse=True)
    for file in tqdm.tqdm(csv_files):
        chunk_path = os.path.join(chunk_folder, file)
        df = pd.read_csv(chunk_path)
        df.to_csv(output_file_path, mode='a', index=False, header=first_file)
        gc.collect()
        if first_file:
            first_file = False



def reverse_csv(input_file_path, output_file_path):
    tmp_folder = reverse_by_chunk(input_file_path, output_file_path, 86400)
    merge_files_in_reverse(output_file_path, tmp_folder)
    shutil.rmtree(tmp_folder)


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Reverse a big csv file.')
    parser.add_argument('-s', '--source', type=str, required=True, help='The path to the input CSV file')
    parser.add_argument('-d', '--destination', type=str, required=True, help='The path to the output CSV file with the added log price')

    # Parse the arguments
    args = parser.parse_args()

    # Process the CSV file
    reverse_csv(args.source, args.destination)


if __name__ == '__main__':
    main()