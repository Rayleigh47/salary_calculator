import numpy as np
import pandas as pd
import streamlit as st

# Calculate variable components for the year e.g. bonus months, salary increment, salary promotion, investment rate, inflation rate
def calculate_variable_components(BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE):
    print("Generating variable components for the year:")
    # Define mean values and standard deviations realistically
    params = {
        "bonus_months": (BONUS_MONTHS, 0.25), # 3.75 to 4.25 months
        "salary_increment": (SALARY_INCREMENT, 0.005), # 3% to 4%
        "salary_promotion": (SALARY_PROMOTION, 0.02), # 5% to 9%
        "investment_rate": (INVESTMENT_RATE, 0.01), # 3% to 5%
        "inflation_rate": (INFLATION_RATE, 0.005) # 2.5% to 3.5%
    }
    parameters = []
    # Generate normally distributed values
    for param, (mean, std_dev) in params.items():
        value = np.random.normal(mean, std_dev)
        parameters.append(value)
        if (param == "bonus_months"):
            print(f"    {param}: {value:.2f}")
        else:
            print(f"    {param}: {value*100:.3f}%")
    print("\n")
    # Return the generated values
    return parameters

# Raw calculation of earnings for the year
def calculate_earnings(salary, bonus_months):
    print("Calculating earnings for the year:")
    print(f"    Monthly Salary: ${salary:.2f}")
    # Calculate total salary + bonus for the year
    total_salary = salary * 12
    print(f"    Total Salary (12 months): ${total_salary:.2f}")
    total_bonus = salary * bonus_months
    print(f"    Total Bonus ({bonus_months:.2f} months): ${total_bonus:.2f}")
    total = total_salary + total_bonus
    print(f"    Total Earnings: ${total:.2f}")
    print("\n")
    return total

# calculate savings in a year based off salary, total number of months
def calculate_savings(salary, CPF_cap, salary_percentage_saved, bonus_percentage_saved, bonus_months):
    print("Calculating savings for the year:")
    # Calculate true salary after CPF deduction (capped at CPF cap)
    if salary > CPF_cap:
        true_salary = salary - (CPF_cap * 0.2)
        print(f"    True salary after CPF (exceeded CPF cap of ${CPF_cap:.2f}): ${true_salary:.2f}")
    else:
        true_salary = salary * 0.8
        print(f"    True salary after CPF (within CPF cap of ${CPF_cap:.2f}): ${true_salary:.2f}")
    # Calculate savings from salary and bonus
    saved_salary = true_salary * 12 * salary_percentage_saved
    print(f"    Percentage of Salary Saved is {salary_percentage_saved*100:.2f}% : ${saved_salary:.2f}")
    saved_bonus = true_salary * bonus_months * bonus_percentage_saved
    print(f"    Percentage of Bonus Saved is {bonus_percentage_saved*100:.2f}% : ${saved_bonus:.2f}")
    total_saved = saved_salary + saved_bonus
    print(f"    Total Saved (Sum): ${total_saved:.2f}")
    print("\n")
    return total_saved

# Naive tax calculator for Singapore tax rates assuming no tax relief or deductions
def calculate_tax(chargeable_income):
    print("Calculating tax payable for the year:")
    print(f"    Chargeable Income (Gross earnings): ${chargeable_income:.2f}")
    # Taxable income ranges with gross tax payable up to each limit from IRAS website
    print("    Using Tax Brackets from IRAS (2024)...")
    tax_brackets = [
        (20000, 0.02, 0),        # Up to $20,000: $0 tax, 2% tax rate above $20,000
        (30000, 0.035, 200),     # Up to $30,000
        (40000, 0.07, 550),      # Up to $40,000
        (80000, 0.115, 3350),    # Up to $80,000
        (120000, 0.15, 7950),    # Up to $120,000
        (160000, 0.18, 13950),   # Up to $160,000
        (200000, 0.19, 21150),   # Up to $200,000
        (240000, 0.195, 28750),  # Up to $240,000
        (280000, 0.2, 36550),    # Up to $280,000
        (320000, 0.22, 44550),   # Up to $320,000
        (500000, 0.23, 84150),   # Up to $500,000
        (1000000, 0.24, 199150), # Up to $1,000,000
    ]
    total_tax = 0
    # Iterate from highest to lowest tax bracket to find the first bracket that the chargeable income exceeds
    for bracket_limit, rate, gross_tax_up_to in reversed(tax_brackets):
        # Find bracket where chargeable income is first greateer than bracket limit
        if chargeable_income >= bracket_limit:
            # Calculate tax payable for this bracket
            print(f"    Tax Bracket is ${bracket_limit:.2f} with {rate*100:.2f}% tax for remaining income")

            remaining_income_tax = (chargeable_income - bracket_limit) * rate
            total_tax = remaining_income_tax + gross_tax_up_to
            print(f"    Total Tax Payable: ${gross_tax_up_to:.2f} + ${remaining_income_tax:.2f} = ${total_tax:.2f}")
            break
    # Calculate the effective tax rate as a percentage
    effective_tax_rate = (total_tax / chargeable_income) * 100 if chargeable_income > 0 else 0
    print(f"    Effective Tax Rate: {effective_tax_rate:.2f}%")
    print("\n")
    return total_tax, effective_tax_rate

# Update total savings nominal and real as well as cumulative interest
def update_savings(effective_savings, total_savings_nominal, total_savings_real, investment_rate, inflation_rate):
    print("Updating savings for the year:")
    print(f"    Effective Savings (Total Saved - Total Tax Payable): ${effective_savings:.2f}")
    print(f"    Existing Savings (Nominal): ${total_savings_nominal:.2f}")
    # Update total savings nominal which is  total_savings_nominal + effective_savings * (1 + investment_rate)
    total_savings_nominal += effective_savings
    total_savings_nominal *= (1 + investment_rate)
    print(f"    Total Savings (Nominal) after {investment_rate*100:.2f}% investment rate: ${total_savings_nominal:.2f}")
    # Update total savings real which is total savings nominal - inflation rate
    total_savings_real = total_savings_nominal / (1 + inflation_rate)
    print(f"    Total Savings (Real) after {inflation_rate*100:.2f}% inflation rate:: ${total_savings_real:.2f}")
    print("\n")
    return total_savings_nominal, total_savings_real

# Update salary for next year based off salary increment and promotion, promotion years, rank cap and rank increase
def update_salary(salary, salary_increment, salary_promotion, year, promotion_years, rank_cap, rank_increase):
    print("Updating salary for next year:")
    # Check if current year is a promotion year
    if year in promotion_years:
        # Increase rank cap by rank increase
        rank_cap += rank_increase
        # Increase salary by salary promotion rate
        salary *= (1 + salary_promotion)
        print(f"    Promotion to ${salary:.2f} and rank cap to ${rank_cap}")
    else:
        if salary < rank_cap:
            # If salary is below rank cap, increase salary by salary increment rate
            salary *= (1 + salary_increment)
            print(f"    Salary Increment of {salary_increment*100:.2f}% to ${salary:.2f}")
        else:
            print(f"    Salary capped at ${salary:.2f}")
    return salary, rank_cap

# Display the yearly data in using streamlit line charts
def display_yearly_data(yearly_data, years_list, earnings_list, total_savings_nominal_list, total_savings_real_list, salary_list):
    # Create a selection box to choose which chart to display
    chart_selection = st.selectbox(
        "Select a chart to view:",
        ["Total Earnings", "Total Savings (Nominal)", "Total Savings (Real)", "Salary"]
    )

    # Display the selected chart
    if chart_selection == "Total Earnings":
        st.write("### Total Earnings Over Time")
        st.line_chart({
            "Total Earnings": earnings_list,
            "Years": years_list
        }, y="Total Earnings", x="Years")
        df = pd.DataFrame(earnings_list, columns=["Total Earnings"])
        st.dataframe(df)

    elif chart_selection == "Total Savings (Nominal)":
        st.write("### Total Savings (Nominal) Over Time")
        st.line_chart({
            "Total Savings (Nominal)": total_savings_nominal_list,
            "Years": years_list
        }, y="Total Savings (Nominal)", x="Years")
        df = pd.DataFrame(total_savings_nominal_list, columns=["Total Savings (Nominal)"])
        st.dataframe(df)

    elif chart_selection == "Total Savings (Real)":
        st.write("### Total Savings (Real) Over Time")
        st.line_chart({
            "Total Savings (Real)": total_savings_real_list,
            "Years": years_list
        }, y="Total Savings (Real)", x="Years")
        df = pd.DataFrame(total_savings_real_list, columns=["Total Savings (Real)"])
        st.dataframe(df)

    elif chart_selection == "Salary":
        st.write("### Salary Over Time")
        st.line_chart({
            "Salary": salary_list,
            "Years": years_list
        }, y="Salary", x="Years")
        df = pd.DataFrame(salary_list, columns=["Salary"])
        st.dataframe(df)
    print("\n")