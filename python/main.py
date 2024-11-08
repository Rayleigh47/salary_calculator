import streamlit as st
# import streamlit_scrollable_textbox as stx
import pandas as pd
import sys
import io
from functions import calculate_variable_components, calculate_earnings, calculate_savings, calculate_tax, update_savings, update_salary, display_yearly_data

def main():
    # Streamlit app title
    st.title("Savings Calculator")

    # User input for parameters
    years = st.number_input("Number of years to simulate:", min_value=1, max_value=30, value=10, step=1)
    salary = st.number_input("Initial salary:", min_value=0, value=5000, step=100)
    salary_saved_percentage = st.slider("Percentage of salary you want to save every month (%):", min_value=0.0, max_value=100.0, value=30.0, step=0.5)
    salary_percentage_saved = salary_saved_percentage / 100
    bonus_saved_percentage = st.slider("Percentage of your bonus you want to save (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    bonus_percentage_saved = bonus_saved_percentage / 100
    promotion_years = st.multiselect("Years where promotion occurs:", list(range(1, 30)), default=[2, 4, 8])
    rank_cap = st.number_input("Starting salary cap (Current salary limit untl promotion)", min_value=0, value=7500)
    rank_increase = st.number_input("Increase to salary cap after a promotion", min_value=0, value=2500)
    CPF_cap = st.number_input("CPF Cap (Maximum salary of which CPF is calculated - $8000 by 2026)", min_value=0, value=8000, step=100)
    
    # Variable components with sliders
    st.write("## Variable Components (Provide an estimate)")
    st.write("#### These figures will be normally distributed around their mean values")
    BONUS_MONTHS = st.slider("Bonus months", min_value=0, max_value=12, value=4)
    salary_increment_percentage = st.slider("Salary increment rate (%)", min_value=0.0, max_value=20.0, value=3.5, step=0.5)
    SALARY_INCREMENT = salary_increment_percentage / 100
    salary_promotion_percentage = st.slider("Salary promotion rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.5)
    SALARY_PROMOTION = salary_promotion_percentage / 100
    investment_rate_percentage = st.slider("Investment return rate (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    INVESTMENT_RATE = investment_rate_percentage / 100
    inflation_rate_percentage = st.slider("Inflation rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
    INFLATION_RATE = inflation_rate_percentage / 100

    # Initialize savings variables
    total_savings_nominal = 0
    total_savings_real = 0
    yearly_data = []
    years_list = []
    earnings_list = []
    total_savings_nominal_list = []
    total_savings_real_list = []
    salary_list = []

    # Create a StringIO buffer to capture the printed output
    output_buffer = io.StringIO()

    # Redirect the standard output (print statements) to the buffer
    sys.stdout = output_buffer

    # Simulation loop
    for year in range(1, years + 1):
        print(f"\nYear {year}:")
        # Calculate variable components
        bonus_months, salary_increment, salary_promotion, investment_rate, inflation_rate = calculate_variable_components(
            BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE
        )
        
        # Calculate earnings, savings, and tax
        total_earnings = calculate_earnings(salary, bonus_months)
        savings = calculate_savings(salary, CPF_cap, salary_percentage_saved, bonus_percentage_saved, bonus_months)
        total_tax, effective_tax_rate = calculate_tax(total_earnings)
        
        # Effective savings calculation
        effective_savings = savings - total_tax
        total_savings_nominal, total_savings_real = update_savings(
            effective_savings, total_savings_nominal, total_savings_real, investment_rate, inflation_rate
        )
        
        # Update salary for next year
        salary, rank_cap = update_salary(salary, salary_increment, salary_promotion, year, promotion_years, rank_cap, rank_increase)

        # Store the data for this year in the list
        yearly_data.append({
            'Year': year,
            'Total Earnings': total_earnings,
            'Total Savings (Nominal)': total_savings_nominal,
            'Total Savings (Real)': total_savings_real,
            'Salary': salary,
        })

        # Store data for line charts
        years_list.append(year)
        earnings_list.append(total_earnings)
        total_savings_nominal_list.append(total_savings_nominal)
        total_savings_real_list.append(total_savings_real)
        salary_list.append(salary)

    # Display the yearly data in a DataFrame and line charts
    display_yearly_data(yearly_data, years_list, earnings_list,total_savings_nominal_list, total_savings_real_list, salary_list)

    # Redirect the standard output back to the console
    sys.stdout = sys.__stdout__

    # Get the printed output from the buffer
    collected_output = output_buffer.getvalue()

    # Debug Console box for streamlit
    st.write("## Debug Console")
    # stx.scrollableTextbox(collected_output, height=300)

if __name__ == "__main__":
    main()
