from src.data.db import get_client
import pandas as pd
import logging
from datetime import datetime, timedelta


def make_binance_market_stat(date: str, symbol: str, dst: str) -> bool:
    """
    :param date: YYYY-MM-DD
    :param symbol: example: BTCUSDT, ETHBTC
    :param dst: path/to/data.csv
    :return: is success
    """
    client = get_client()
    db = client.get_database('binance')
    collection = db.get_collection('wsMarketStatEvents')
    # Parse the date and create a date range for the query
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)

    # Construct the query for the specified date and symbol
    query = {
        "E": {"$gte": start_date, "$lt": end_date},
        "s": symbol
    }

    try:
        # Execute the query
        documents = collection.find(query)

        # Convert the cursor to a list and then to a DataFrame
        df = pd.DataFrame(list(documents))

        # If the DataFrame is not empty, process and save it
        if not df.empty:
            # Convert MongoDB Timestamp fields to string format
            # Adjust the format as needed
            for field in ['E', 'C', 'O']:
                if field in df.columns:
                    df[field] = df[field].dt.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Convert other specific fields if they exist and need conversion
            # This part is omitted for now as it seems the main issue was with date fields

            # Save the DataFrame to CSV
            df.to_csv(dst, index=False)
            logging.info("Data successfully written to CSV.")
            return True
        else:
            logging.info("No data found for the given date and symbol.")
            return False
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False


if __name__ == '__main__':
    date = '2024-03-01'
    symbol = 'PEPEUSDT'
    dst = f'./data/raw/binance_{symbol.lower()}_{date}.csv'
    make_binance_market_stat(date, symbol, dst)