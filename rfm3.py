import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("email_database3.csv", sep=';')

# Convert the purchase_date column to a datetime type
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

# Calculate the recency (days since last purchase) for each customer
recency = df.groupby(['email']).purchase_date.max().reset_index()
recency.columns = ['email','last_purchase_date']
recency['recency'] = (recency['last_purchase_date'].max() - recency['last_purchase_date']).dt.days

# Calculate the frequency (number of purchases) for each customer
frequency = df.groupby(['email']).purchase_date.count().reset_index()
frequency.columns = ['email','frequency']

# Calculate the monetary value (total cost) for each customer
monetary = df.groupby(['email']).purchase_amount.sum().reset_index()
monetary.columns = ['email','monetary']

# Merge the recency, frequency, and monetary data into one DataFrame
rfm = recency.merge(frequency, on='email').merge(monetary, on='email')
print(rfm)

# Create recency segments
r_labels = range(3, 0, -1)
r_quartiles = pd.qcut(rfm['recency'], q=3, labels=r_labels)
rfm['r_quartile'] = r_quartiles

# Create frequency segments
f_labels = range(1, 4)
f_quartiles = pd.qcut(rfm['frequency'], q=3, labels=f_labels)
rfm['f_quartile'] = f_quartiles

# Create monetary segments
m_labels = range(1, 4)
m_quartiles = pd.qcut(rfm['monetary'], q=3, labels=m_labels)
rfm['m_quartile'] = m_quartiles

# Concatenate recency, frequency, and monetary segments
rfm['RFM_Score'] = rfm[['r_quartile','f_quartile','m_quartile']].apply(lambda x: ''.join(x.astype(str)), axis=1)

#Group by RFM_Score and count the number of customers in each segment
segment_counts = rfm.groupby(['RFM_Score']).email.nunique()

#Print the segments and the number of customers in each one
print(segment_counts)

# Recency
recency_stats = rfm['recency'].describe()
print("In order for recency to be estimated at 1, it must be from", recency_stats['min'], "to", recency_stats['50%'])
print("In order for recency to be estimated at 2, it must be from", recency_stats['50%'], "to", recency_stats['75%'])
print("In order for recency to be estimated at 3, it must be from", recency_stats['75%'], "to", recency_stats['max'])

# Frequency
frequency_stats = rfm['frequency'].describe()
print("In order for frequency to be estimated at 1, it must be from", frequency_stats['min'], "to", frequency_stats['50%'])
print("In order for frequency to be estimated at 2, it must be from", frequency_stats['50%'], "to", frequency_stats['75%'])
print("In order for frequency to be estimated at 3, it must be from", frequency_stats['75%'], "to", frequency_stats['max'])

# Monetary
monetary_stats = rfm['monetary'].describe()
print("In order for monetary to be estimated at 1, it must be from", monetary_stats['min'], "to", monetary_stats['50%'])
print("In order for monetary to be estimated at 2, it must be from", monetary_stats['50%'], "to", monetary_stats['75%'])
print("In order for monetary to be estimated at 3, it must be from", monetary_stats['75%'], "to", monetary_stats['max'])

# Create a list of all RFM segments
segment_list = rfm['RFM_Score'].unique()

for segment in segment_list:
    segment_df = rfm.query('RFM_Score == @segment')
    segment_df.to_csv(f"segment_{segment}.csv", index=False)

# Group the data by RFM_Score and calculate the sum of the monetary value for each group
segment_monetary = rfm.groupby(['RFM_Score']).monetary.sum()

# Print the segments and the total monetary value for each one
print(segment_monetary)

import seaborn as sns
# Create a new DataFrame with frequency, recency, and monetary
scatter_df = rfm[['frequency','recency','monetary']]
sns.scatterplot(x='frequency', y='recency', size='monetary', data=scatter_df)



#     import seaborn as sns
# import matplotlib.pyplot as plt

# rfm_segments_monetary = rfm.groupby(['RFM_Score']).purchase_amount.sum()
# print(rfm_segments_monetary)

# rfm_table = rfm.pivot_table(values='recency', index='r_quartile', columns='f_quartile', aggfunc='mean')
# sns.heatmap(rfm_table, annot=True, fmt='.1f', cmap='Blues')

# # Add labels and title
# plt.xlabel("Квартиль частоты")
# plt.ylabel("Квартиль недавности")
# plt.title("RFM матрица")

# # Show the plot
# plt.show()