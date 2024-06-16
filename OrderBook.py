import requests
import json
from symbolDictionary import SymbolDictionary

def fetch_order_book_snapshot(coin, limit=10, cursor=None):
    #  API endpoint URL
    url = 'https://api.hyperliquid.xyz/info'

    # headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # payload (body) of the request
    data = {
        'type': 'l2Book',
        'coin': coin,
        'limit': limit,
        'cursor': cursor
    }

    try:
        # Send an HTTP POST request to the API
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            # Request was successful, parse the response JSON
            order_book_snapshot = response.json()
            
            # Extract the cursor for pagination
            new_cursor = order_book_snapshot.get('cursor')

            # Process the order book snapshot data and print it
            process_order_book_snapshot(order_book_snapshot)

            # Return the new cursor for the next page of results
            return new_cursor
        else:
            print("API request failed with status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred during the API request:", str(e))
        return None

def process_order_book_snapshot(snapshot_data):
    # Display the order book snapshot data more clearly
    coin = snapshot_data.get('coin')
    levels = snapshot_data.get('levels')
    
    print(f"Order Book Snapshot for {coin}:\n")
    
    # Extract Buy Side and Sell Side data
    buy_side = levels[0]  # First level for buy side
    sell_side = levels[1]  # Second level for sell side
    
    print("Buy Side:")
    for entry in buy_side:
        print(f"  Price: {entry['px']}, Size: {entry['sz']}")
    
    print("\nSell Side:")
    for entry in sell_side:
        print(f"  Price: {entry['px']}, Size: {entry['sz']}")

def get_user_input():
    while True:
        # Prompt the user for a coin input
        user_input = input("Enter a coin symbol (Symbol-USD): ").strip().upper()  # Convert input to uppercase

        # Check if the user input exists in the symbol dictionary
        if user_input in [key.upper() for key in SymbolDictionary.symbols.keys()]:
            return SymbolDictionary.symbols[user_input]
        else:
            print(f"Unknown coin: {user_input}")

if __name__ == '__main__':
   
    limit = 10

    while True:
        coin = get_user_input()
        if coin:
            # Fetch the first page of data
            cursor = fetch_order_book_snapshot(coin, limit)

            # Continue fetching next pages if needed
            while cursor:
                cursor = fetch_order_book_snapshot(coin, limit, cursor)