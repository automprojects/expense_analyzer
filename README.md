# Organization Expense Analyzer

## Overview
The Organization Expense Analyzer is a Python-based project that leverages machine learning models to analyze expenses, predict income, and allocate amounts based on user input. This project utilizes Streamlit for creating an interactive web application, Pandas for data manipulation, Plotly for data visualization, and scikit-learn for machine learning tasks.

## Features
- **Expense Analysis:** Visualize and analyze expense distribution across various categories using interactive pie charts and bar charts.
- **Income Prediction:** Predict future income based on historical data using a Linear Regression model.
- **Expense Category Prediction:** Predict the expense category for a given amount using a Decision Tree Classifier.
- **Profit Calculation:** Calculate expected profits by balancing predicted income and expenses.

## Modules Used
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [scikit-learn](https://scikit-learn.org/)
- [NumPy](https://numpy.org/)

## Installation
1. Clone the repository: `git clone https://github.com/yourusername/expense-analyzer.git`
2. Navigate to the project directory: `cd expense-analyzer`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Run the Streamlit app: `streamlit run app.py`
2. Access the app in your web browser at `http://localhost:8501`

## Project Structure
- `app.py`: Main script containing the Streamlit application.
- `company_dataset.csv`: Sample dataset (replace with your actual dataset file).
- `requirements.txt`: List of project dependencies.

## Contributing
Contributions are welcome! If you have suggestions, bug reports, or improvements, please open an issue or create a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

---

**Note:** Replace the placeholders (`yourusername`, `company_dataset.csv`, etc.) with your actual information and project details.
