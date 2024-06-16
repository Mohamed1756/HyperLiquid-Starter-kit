import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV 
df = pd.read_csv('./accountHistory/fills.csv')

df['time'] = pd.to_datetime(df['time'])


df = df[df['dir'].str.contains('Close')]


df['closedPnl'] = df['closedPnl'].where(df['closedPnl'] != 0, np.nan)

# Plot the closed PnL where it's non-zero
plt.plot(df['time'], df['closedPnl'], marker='o', linestyle='-')

plt.xlabel('Time')
plt.ylabel('Closed PnL')
plt.title('Closed PnL Over Time')

plt.show()
