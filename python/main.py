from functions import calculate_variable_components, calculate_earnings, calculate_savings, calculate_tax, update_savings, update_salary

# Parameters (user input)
years = 5 # Number of years to simulate
salary = 6200
CPF_cap = 8000 # CPF cap for contribution
salary_percentage_saved = 0.3 # i.e. 30% of salary saved (after CPF)
bonus_percentage_saved = 0.7 # i.e. 70% of bonus saved (after CPF)
promotion_years = [2, 4, 8, 15, 22] # Promotion years
rank_cap = 7500 # Current rank cap
rank_increase = 2500 # Increase in rank cap

# Variable Components initialized
BONUS_MONTHS = 4 # Number of bonus months
SALARY_INCREMENT = 0.035 # Salary increment rate
SALARY_PROMOTION = 0.07 # Salary promotion rate
INVESTMENT_RATE = 0.04 # Investment rate
INFLATION_RATE = 0.03 # Inflation rate

def main():
    salary = 6200
    total_savings_nominal = 0
    total_savings_real = 0
    for year in range(1, years + 1):
        print(f"Year {year}:")
        # Calculate variable components for the year
        bonus_months, salary_increment, salary_promotion, investment_rate, inflation_rate = calculate_variable_components(BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE)
        print(f"Bonus Months: {bonus_months:.2f}, Salary Increment: {salary_increment*100:.2f}%, Salary Promotion: {salary_promotion*100:.2f}%, Investment Rate: {investment_rate*100:.2f}%, Inflation Rate: {inflation_rate*100:.2f}%")

        # Calculate total earnings for the year (gross salary + bonus)
        total_earnings = calculate_earnings(salary, bonus_months)
        print(f"Earnings: ${total_earnings:.2f}")

        # Calculates savings for the year (after CPF and savings rate)
        savings = calculate_savings(salary, CPF_cap, salary_percentage_saved, bonus_percentage_saved, bonus_months)
        print(f"Savings: ${savings:.2f}")

        # Calculate tax payable this year (based off total earnings)
        total_tax, effective_tax_rate = calculate_tax(total_earnings)
        print(f"Tax Payable: ${total_tax:.2f}, Effective Tax Rate: {effective_tax_rate:.2f}%")

        # Effective Savings = Savings - Tax
        effective_savings = savings - total_tax
        print(f"Effective Savings: ${effective_savings:.2f}")

        # Update total savings nominal and real, and cumulative interest
        savings_nominal, savings_real = update_savings(effective_savings, total_savings_nominal, total_savings_real, investment_rate, inflation_rate)
        print(f"Savings (Nominal): ${savings_nominal:.2f}, Savings (Real): ${savings_real:.2f}")

        # Add to total savings
        total_savings_nominal += savings_nominal
        total_savings_real += savings_real
        print(f"Total Savings (Nominal): ${total_savings_nominal:.2f}, Total Savings (Real): ${total_savings_real:.2f}")

        # Update salary for next year
        salary = update_salary(salary, salary_increment, salary_promotion, year, promotion_years, rank_cap, rank_increase)
        print(f"Salary next year: ${salary:.2f}\n")


main()