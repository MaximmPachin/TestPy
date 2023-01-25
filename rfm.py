import pandas as pd

try:
    # Load the email database into a pandas dataframe
    df = pd.read_csv("email_database3.csv", sep=';')

    # convert the purchase date column to datetime format
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])

    # set the retention period
    retention_period = 1 # years

    # calculate the average purchase frequency
    average_purchase_frequency = df.groupby('email')['purchase_date'].count().mean()

    # calculate the total purchase value per customer
    df_customer_value = df.groupby('email')['purchase_amount'].sum()

    # calculate the lifetime value
    LTV = df_customer_value.mean() * average_purchase_frequency * retention_period
    print(LTV)
    
except pd.errors.ParserError as e:
    print(f'Error: {e}')
    pass

import time
time.sleep(3)
input("Press Enter to close the terminal")