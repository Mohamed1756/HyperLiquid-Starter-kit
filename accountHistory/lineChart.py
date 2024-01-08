import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV 
df = pd.read_csv('./accountHistory/fills.csv')

# Convert time column to datetime
df['time'] = pd.to_datetime(df['time'])

df = df[df['dir'].str.contains('Close')]

plt.plot(df['time'], df['closedPnl'], marker='o')

# Plot the closed PnL 
#plt.plot(df['time'], df['closedPnl'])
plt.xlabel('Time')
plt.ylabel('Closed PnL')
plt.title('Closed PnL Over Time')

plt.show()