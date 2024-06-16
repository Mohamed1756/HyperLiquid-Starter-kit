import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() 

# Set the date to extract pnl records
start_date = datetime(2024,1,1) 
end_date = datetime.now()

def retrieve_user_fills(wallet_address, start_date, end_date):

  url = 'https://api.hyperliquid.xyz/info'

  headers = {
    'Content-Type': 'application/json'
  }

  data = {
    'type': 'userFills',
    'user': wallet_address
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))

  if response.status_code == 200:

    data = response.json()
    
    df = pd.DataFrame(data)

    # Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    # Filter fills within the specified date range
    df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]

    df = df.drop(columns=['crossed','startPosition','tid','side','oid','liquidationMarkPx','hash'])

    df.set_index('time', inplace=True)

    output_directory = './accountHistory'
    os.makedirs(output_directory, exist_ok=True)

    df.to_csv(os.path.join(output_directory, 'fills.csv'))
    
    print(df)

  else:
    print("There was an issue with the request.")

# input wallet address 
address = os.getenv('WALLET_ADDRESS')
retrieve_user_fills(address, start_date,end_date)