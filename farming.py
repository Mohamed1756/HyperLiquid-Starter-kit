import requests
import datetime

def fetch_perpetual_funding_rates():
    # Define the API endpoint URL
    url = 'https://api.hyperliquid.xyz/info'

    # Define the request payload as a dictionary
    payload = {
        "type": "metaAndAssetCtxs"
    }

    # Define the headers with "Content-Type" set to "application/json"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send an HTTP POST request to the API with the specified headers
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            # Request was successful, parse the response JSON
            data = response.json()
            #print(data)
            # Find the BTC data in the second part of the array
            symbol_data = data[1][0-100]

            # Create a dictionary to combine the data for 'BTC'
            combined_data = {
                'name': 'BTC',
                'mark price': symbol_data['markPx'],
                'funding': symbol_data['funding'],
               # 'premium': btc_data['premium'],
            }

            # Add a new column for time left to the nearest hour with seconds
            current_time = datetime.datetime.now()
            remaining_seconds = (60 - current_time.second) % 60
            combined_data['time_left_to_hour'] = f"{(60 - current_time.minute) % 60} min {remaining_seconds} sec"

            # Print the combined data for 'BTC' including funding information and time left to the nearest hour
            print(f"Combined Data for BTC:")
            for key, value in combined_data.items():
                print(f"{key}: {value}")

        else:
            print(f"API request failed with status code: {response.status_code}")
    except Exception as e:
        print("An error occurred during the API request:", str(e))

if __name__ == '__main__':
    fetch_perpetual_funding_rates()
