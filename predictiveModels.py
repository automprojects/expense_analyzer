import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import warnings

# Load the expense dataset (replace 'your_expense_dataset.csv' with your actual dataset file)
expenses = pd.read_csv('https://raw.githubusercontent.com/automprojects/expense_analyzer/main/company_dataset.csv')

# Streamlit App
st.title('Expense Analyzer')

# Display the expense dataset
st.write('### Organization Expense Dataset')
st.write(expenses)

# Choose relevant features for prediction
features = ['Amount']  # Replace with your actual feature names
target = 'Category'

# Handle missing values (NaN) in the dataset
imputer = SimpleImputer(strategy='mean')
expenses[features] = imputer.fit_transform(expenses[features])

# Map categorical values to numeric labels
category_mapping = {category: idx for idx, category in enumerate(expenses['Category'].unique())}
expenses['Category'] = expenses['Category'].map(category_mapping)

# Reverse mapping to get original category names
reverse_category_mapping = {idx: category for category, idx in category_mapping.items()}

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(expenses[features], expenses[target], test_size=0.2, random_state=42)

# Train a Decision Tree Classifier model
model_expenses = DecisionTreeClassifier()
model_expenses.fit(X_train, y_train)

# Train a Linear Regression model 
model_income = LinearRegression()
model_income.fit(X_train, y_train)

# Streamlit App
st.title('Expense Predictor using ML Models')

# Prediction Form
st.sidebar.header('Expense Prediction Input')
new_expense_amount = st.sidebar.number_input('Enter Amount', value=2000000)
warnings.filterwarnings("ignore", category=UserWarning)

# Visualization: Pie chart for predicted expense distribution by category
predicted_expenses = pd.DataFrame({'Category': expenses['Category'], 'Amount': model_expenses.predict(expenses[features])})

# Reverse mapping to get original category names
predicted_expenses['Category'] = predicted_expenses['Category'].map(reverse_category_mapping)

# Make a prediction for the input data
predicted_category_idx = model_expenses.predict([[new_expense_amount]])[0]
predicted_category = [category for category, idx in category_mapping.items() if idx == predicted_category_idx][0]

# Display the predicted expense category
st.sidebar.subheader('(Category & Amount Distribution Prediction)')


# Visualization: Pie chart for predicted expense distribution by category
predicted_expenses = pd.DataFrame({'Category': expenses['Category'],
                                    'Amount': model_expenses.predict(expenses[features])})

# Print the predicted_expenses DataFrame for debugging
st.write("Predicted Expenses DataFrame:")
st.write(predicted_expenses)

# Reverse mapping to get original category names
predicted_expenses['Category'] = predicted_expenses['Category'].map(reverse_category_mapping)

# Calculate the percentage distribution
percentage_distribution = predicted_expenses.groupby('Category').size() / len(predicted_expenses)

# Print the percentage_distribution 
st.write("Percentage Distribution:")
st.write(percentage_distribution)

# Allocate amounts based on the percentage
amount_distribution = (percentage_distribution * new_expense_amount).reset_index()
amount_distribution.columns = ['Category', 'Allocated_Amount']

# Visualization: Sunburst chart for predicted expense amounts
fig_sunburst = px.sunburst(
    amount_distribution,
    names='Category',
    parents=[''] * len(amount_distribution),  # Set a common parent for all categories
    values='Allocated_Amount',
    title='Predicted Expense Amount Distribution Sunburst Chart',
)

# Display the chart using Streamlit
st.plotly_chart(fig_sunburst)

# Print the amount_distribution for debugging
st.write("Allocated Amount Distribution:")
st.write(amount_distribution)

# Visualization: Pie chart for predicted expense distribution by category
fig_pie = px.pie(amount_distribution, values='Allocated_Amount', names='Category', title='Predicted Expense Distribution by Category')
st.plotly_chart(fig_pie)

# Visualization: Bar chart for predicted expense amounts
fig_bar = px.bar(amount_distribution, x='Category', y='Allocated_Amount', color='Category',
                 title='Predicted Expense Amount Distribution by Category')
st.plotly_chart(fig_bar)


# Streamlit app
st.title('Predicted Expense Amount Bubble Chart')

# Plotly Express bubble chart
fig_bubble = px.scatter(
    amount_distribution,
    x='Category',
    y='Allocated_Amount',
    size='Allocated_Amount',  # Bubble size based on the allocated amount
    color='Category',    # Color bubbles by category
    hover_name='Category',    # Display category name on hover
    # log_x=True,               # Log scale on the x-axis for better visibility
    size_max=60,              # Set the maximum bubble size  
)

# Customize the layout
fig_bubble.update_layout(
    xaxis_title='Category',
    yaxis_title='Allocated Amount',
    title='Predicted Expense Amount Bubble Chart',
)

# Display the chart using Streamlit
st.plotly_chart(fig_bubble)

# Add a footer
st.markdown("---")
st.markdown("Developed by JNNIE | Data Source: Organization's Business Dataset")
