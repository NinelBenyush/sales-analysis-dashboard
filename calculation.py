import pandas as pd
import matplotlib.pyplot as plt 
import streamlit as st

sales = pd.read_csv('cleaned_data.csv')

#Revenue KPIs
total_revenue = sales["total"].sum()
#print(f"Total Revenue: {total_revenue}")

monthly_revenue = sales.groupby(['year','month'])['total'].sum().reset_index()
#print(f"Monthly Revenue: {monthly_revenue}")

per_product_revenue = sales.groupby('product_name')['total'].sum().reset_index()
#print(f"Revenue per Product: {per_product_revenue}")

per_category_revenue = sales.groupby('category')['total'].sum().reset_index()
#print(f"Revenue per Category: {per_category_revenue}")

per_customer_revenue = sales.groupby('customer_id')['total'].sum().reset_index()
#print(f"Revenue per Customer: {per_customer_revenue}")

#Customer KPIs
total_customers = sales["customer_id"].nunique()
#print(f"Total Customers: {total_customers}")

customers_count = sales["customer_id"].value_counts().reset_index()
customers_count.columns = ["customer_id", "order_count"]  
returning_customers = customers_count[customers_count["order_count"] > 1]
#print(f"Returning Customers: {len(returning_customers)}")

sorted_total_customers = per_customer_revenue.sort_values(by='total', ascending=False)
top_10_customers = sorted_total_customers.head(10)
#print(f"Top 10 Customers by Revenue: {top_10_customers}")

#Product KPIs
top_5_products = per_product_revenue.sort_values(by='total', ascending=False).head(5)
#print(f"Top 5 Products by Revenue: {top_5_products}")

top_5_categories = per_category_revenue.sort_values(by='total', ascending=False).head(5)
#print(f"Top 5 Categories by Revenue: {top_5_categories}")

average_order_value = sales["total"].mean()
#print(f"Average Order Value: {average_order_value}")



"""
#Monthly Revenue Line Chart
monthly_revenue['year_month'] = monthly_revenue['year'].astype(str) + '-' + monthly_revenue['month'].astype(str).str.zfill(2)

# all years
plt.figure(figsize=(12,6))
plt.plot(monthly_revenue['year_month'], monthly_revenue['total'], marker='o', linestyle='-')
plt.xticks(rotation=45)
plt.title('Monthly Revenue Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Revenue')
plt.grid(True)
plt.tight_layout()
plt.show()

#line for each year
years = monthly_revenue['year'].unique()

plt.figure(figsize=(12,6))

for year in years:
    data = monthly_revenue[monthly_revenue['year'] == year]
    months = data['month']
    revenue = data['total']
    plt.plot(months, revenue, marker='o', label=str(year))

plt.xticks(range(1,13))  
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.title('Monthly Revenue by Year')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#Category/Department Bar Chart
per_category_revenue = per_category_revenue.sort_values(by='total', ascending=False)

plt.figure(figsize=(8,5))
plt.bar(per_category_revenue['category'], per_category_revenue['total'], color='skyblue')
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Top 10 Products Bar Chart
top_10_products = per_product_revenue.sort_values(by='total', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.barh(top_10_products['product_name'], top_10_products['total'], color='salmon')
plt.xlabel('Revenue')
plt.ylabel('Product')
plt.title('Top 10 Products by Revenue')
plt.gca().invert_yaxis()  
plt.tight_layout()
plt.show()

sales['date'] = pd.to_datetime(sales['date'], format='%Y-%m-%d')  
latest_date = sales['date'].max() + pd.Timedelta(days=1)
rfm = sales.groupby('customer_id').agg({
    'date': lambda x: (latest_date - x.max()).days,  
    'order_id': 'count',  
    'total': 'sum'        
}).reset_index()
rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

#Recent (<30 days), Moderate (30-90), Old (>90)
rfm['Recency_Segment'] = pd.cut(rfm['Recency'], bins=[0,30,90, rfm['Recency'].max()], labels=['Recent','Moderate','Old'])

segment_counts = rfm['Recency_Segment'].value_counts()

plt.figure(figsize=(6,6))
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', colors=['#4CAF50','#FFC107','#F44336'])
plt.title('Customer Segments by Recency')
plt.show()

"""


st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect("Select Year", options=sales['year'].unique(), default=sales['year'].unique())
selected_category = st.sidebar.multiselect("Select Category", options=sales['category'].unique(), default=sales['category'].unique())
selected_country = st.sidebar.multiselect("Select Country", options=sales['country'].unique(), default=sales['country'].unique())

filtered_sales = sales[
    (sales['year'].isin(selected_year)) &
    (sales['category'].isin(selected_category)) &
    (sales['country'].isin(selected_country))
]

st.title("Sales & Revenue Dashboard")
total_revenue = filtered_sales['total'].sum()
total_customers = filtered_sales['customer_id'].nunique()
total_products = filtered_sales['product_name'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Customers", total_customers)
col3.metric("Total Products", total_products)

monthly_revenue = filtered_sales.groupby(['year','month'])['total'].sum().reset_index()
monthly_revenue['year_month'] = monthly_revenue['year'].astype(str) + '-' + monthly_revenue['month'].astype(str).str.zfill(2)

st.subheader("Monthly Revenue")
fig, ax = plt.subplots(figsize=(10,5))
for year in monthly_revenue['year'].unique():
    data = monthly_revenue[monthly_revenue['year']==year]
    ax.plot(data['month'], data['total'], marker='o', label=str(year))
ax.set_xlabel('Month')
ax.set_ylabel('Revenue')
ax.set_xticks(range(1,13))
ax.legend()
st.pyplot(fig)

per_category_revenue = filtered_sales.groupby('category')['total'].sum().reset_index()
per_category_revenue = per_category_revenue.sort_values(by='total', ascending=False)
st.subheader("Revenue by Category")
fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.bar(per_category_revenue['category'], per_category_revenue['total'], color='skyblue')
ax2.set_ylabel("Revenue")
ax2.set_xlabel("Category")
st.pyplot(fig2)

per_product_revenue = filtered_sales.groupby('product_name')['total'].sum().reset_index()
top_10_products = per_product_revenue.sort_values(by='total', ascending=False).head(10)
st.subheader("Top 10 Products by Revenue")
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.barh(top_10_products['product_name'], top_10_products['total'], color='salmon')
ax3.invert_yaxis()
ax3.set_xlabel("Revenue")
st.pyplot(fig3)


st.subheader("Customer Data")
st.dataframe(filtered_sales)