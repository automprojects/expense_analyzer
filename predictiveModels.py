import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings("ignore")
st.logo("https://cyber.gachon.ac.kr/theme/image.php/coursemosv2/theme/1762327820/svg/logo")
# -------------------- Streamlit App --------------------

st.sidebar.header("💰 Budget Manager")
st.sidebar.download_button(
    label="⬇️ Download Sample",
    data=pd.read_csv("company_dataset.csv").to_csv(index=False),
    file_name='sample_expense_dataset.csv',
    mime='text/csv'
)

expenses_file = st.sidebar.file_uploader("📂 Expense Dataset (CSV or XLSX)", type=["csv", "xlsx"])

if expenses_file is not None:
    if expenses_file.name.endswith('.csv'):
        expenses = pd.read_csv(expenses_file)
    else:
        expenses = pd.read_excel(expenses_file)
else:
    st.warning("Please upload your expense dataset to continue.")
    st.stop()

# -------------------- Data Overview --------------------
st.write('### 📊 Uploaded Expense Dataset')
st.dataframe(expenses.head())

# Basic cleaning using pandas
if 'Amount' not in expenses.columns or 'Category' not in expenses.columns:
    st.error("Dataset must include at least 'Amount' and 'Category' columns.")
    st.stop()

# Fill missing values using pandas
expenses['Amount'] = expenses['Amount'].fillna(expenses['Amount'].mean())

# Clean mislabeled or empty categories
expenses['Category'] = expenses['Category'].fillna('Uncategorized')
expenses['Category'] = expenses['Category'].astype(str).str.strip().str.title()

# Show summary
st.write("### 🧾 Cleaned Dataset")
st.dataframe(expenses.head())

# -------------------- Expense Analysis --------------------
st.subheader("📈 Expense Trends and Insights")

# Group by category
category_summary = expenses.groupby('Category')['Amount'].sum() \
        .reset_index() \
        .sort_values('Amount', ascending=False)

# Bar chart by category
fig_bar = px.bar(
    category_summary,
    x='Category',
    y='Amount',
    color='Category',
    title='Total Expenses by Category',
)
st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart by category
fig_pie = px.pie(
    category_summary,
    values='Amount',
    names='Category',
    title='Expense Category Distribution'
)
st.plotly_chart(fig_pie, use_container_width=True)

# -------------------- Monthly Trends --------------------
if 'Date' in expenses.columns:
    expenses['Date'] = pd.to_datetime(expenses['Date'], errors='coerce')
    expenses['Month'] = expenses['Date'].dt.to_period('M')
    
    monthly_trends = expenses.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
    monthly_trends['Month'] = monthly_trends['Month'].astype(str)
    
    st.subheader("📅 Monthly Expense Trends")
    fig_line = px.line(
        monthly_trends,
        x='Month',
        y='Amount',
        color='Category',
        markers=True,
        title='Monthly Expense Trend by Category'
    )
    st.plotly_chart(fig_line, use_container_width=True)

# -------------------- Predict Next Month’s Expense --------------------
st.subheader("🤖 Predict Next Month's Total Expenses (Simple Regression)")

# Aggregate by month for regression
if 'Date' in expenses.columns:
    monthly_total = expenses.groupby(expenses['Date'].dt.to_period('M'))['Amount'].sum().reset_index()
    monthly_total['Month'] = monthly_total['Date'].astype(str)
    monthly_total['Month_Num'] = range(len(monthly_total))

    X = monthly_total[['Month_Num']]
    y = monthly_total['Amount']

    if len(X) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)

        next_month_num = monthly_total['Month_Num'].max() + 1
        predicted_amount = abs(model.predict([[next_month_num]])[0]) # type: ignore

        st.success(f"📅 Predicted total expenses for next month: **₩{predicted_amount:,.0f}**")

        # Forecast visualization
        forecast_df = monthly_total.copy()
        forecast_df = pd.concat([
            forecast_df,
            pd.DataFrame({'Month_Num': [next_month_num], 'Amount': [predicted_amount]})
        ], ignore_index=True)

        forecast_df['Label'] = ['Actual'] * (len(forecast_df) - 1) + ['Predicted']

        fig_forecast = px.line(
            forecast_df,
            x='Month_Num',
            y='Amount',
            color='Label',
            title='Expense Forecast (Next Month Prediction)',
            markers=True
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
    else:
        st.warning("Not enough monthly data to make predictions.")
else:
    st.info("Add a 'Date' column to enable trend and forecast analysis.")
