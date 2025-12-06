import pandas as pd

sales = pd.read_csv('salesData.csv')

#remove duplicate rows
duplicates = sales.duplicated()
#print(f"Number of duplicate rows: {duplicates.sum()}") - 0

#handle missing values
#print(sales.isna().sum()) 0

#convert data types
sales["date"] = pd.to_datetime(sales["date"],format='%d/%m/%Y')
#print(sales.dtypes)

#create new columns
sales["month"] = sales["date"].dt.month
sales["year"] = sales["date"].dt.year

sales.to_csv('cleaned_data.csv', index=False)