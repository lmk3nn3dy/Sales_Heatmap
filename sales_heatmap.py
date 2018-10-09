import pandas as pd
import seaborn as sns

# import the .csv into a data frame
transactions = pd.read_csv('transactions_jul17-aug18.csv')

# isolate purchases (remove account withdrawals)
transactions = transactions[transactions['Balance Impact']=='Credit']

# concat date and time columns
transactions['DateTime'] = transactions['Date'] + ' ' + transactions['Time']

# convert date from str to datetime
transactions['DateTime'] = pd.to_datetime(transactions['DateTime'])

# create dayhour column
transactions['Day_Hour'] = transactions['DateTime'].dt.strftime('%w-%H')

# group and get counts
tmp_srs = transactions.groupby(['Day_Hour']).size()/len(transactions['Day_Hour'])
df = pd.DataFrame(tmp_srs)

# isolate day and hour variables
df = df.reset_index()
df['Day'] = df['Day_Hour'].str.split('-').str[0]
df['Hour'] = df['Day_Hour'].str.split('-').str[1]

df = df.iloc[:,1:4]

# reformat for heatmap
df = df.pivot(index='Hour', columns='Day', values=0)
df.columns = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

# generate heatmap
sns.heatmap(df, cmap='RdBu_r')

