import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as colors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


pio.templates.default = "plotly_white"

data = pd.read_csv("https://raw.githubusercontent.com/automprojects/expense_analyzer/main/company_dataset.csv", encoding='latin-1')

st.title("Organization Expense Analyzer")

# Display the first few rows of the dataframe
st.dataframe(data.head())

# Transform the dataset for horizontal bar chart
bar_data = data[['Date', 'Category', 'Amount']].copy()
bar_data['Amount'] *= -1  # Convert expense to negative values

# Convert Amount column to numeric
data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

# Separate the data into income and expense
income_data = data[data['Income'] == 'Income']
expense_data = data[data['Expense'] == 'Expense']

# Calculate total income, total expenses, and profit
total_income = income_data['Amount'].sum()
total_expenses = expense_data['Amount'].sum()
profit = total_income - total_expenses

# Create a grouped bar chart using Plotly Express
fig = px.bar(data_frame=pd.concat([income_data, expense_data]),
             x='Category',
             y='Amount',
             color='Payment_Method',
             barmode='group',
             labels={'Amount': 'Amount (INR)'},
             title='Income and Expense Distribution by Category',
             )

# Show the chart in Streamlit app
st.plotly_chart(fig)

# Display the results
st.write(f"Total Income: {total_income} INR")
st.write(f"Total Expenses: {total_expenses} INR")
st.write(f"Profit: {profit} INR")

# Create a Streamlit app
st.title('Categorized Expenses - Pie Chart')

# Create a horizontal bar chart using Plotly Express
fig1 = px.bar(bar_data, x='Amount', y='Date', color='Category', orientation='h',
              labels={'Amount': 'Amount (INR)'}, template='plotly_white', 
              title='Categorized Expenses')

# Show the horizontal bar chart in Streamlit app
st.plotly_chart(fig1)


# Pie chart for Categorized Expenses Distribution
fig_pie = px.pie(bar_data, 
                 names='Category', 
                 title='Categorized Expenses Distribution',
                 hole=0.5,
                 color='Category',
                 )

# Customize layout
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(title_text='Categorized Expenses Distribution - Pie Chart', title_font=dict(size=24))

# Show the pie chart in Streamlit app
st.plotly_chart(fig_pie)

# Analysis by Category and Payment Method
sales_by_category_payment = data.groupby(['Category', 'Payment_Method'])['Amount'].sum().reset_index()

# Create a Streamlit app
st.title('Expense Analysis by Payment Methods')

# Grouped bar chart for Analysis by Category and Payment Method
fig4 = px.bar(sales_by_category_payment, 
              x='Category', 
              y='Amount', 
              title='Category vs. Payment Method',
              labels={'Amount': 'Total Expense'},
              color='Payment_Method',
              )

# Customize layout
fig4.update_layout(
    xaxis_title='Category',
    yaxis_title='Payment Method',
    barmode='group',  # 'stack' for stacked bar chart, 'group' for grouped bar chart
)

# Show the plot in Streamlit app
st.plotly_chart(fig4)


# Add a footer
st.markdown("---")
st.markdown("Developed by JNNIE | Data Source: Organization's Business Dataset")
