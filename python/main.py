from tax_calculator import calculate_tax
from savings_calculator import calculate_savings
from salary_calculator import calculate_variable_components

# Parameters (user input)
years = 1
salary = 6200
CPF_cap = 8000 # CPF cap for contribution
salary_percentage_saved = 0.3 # i.e. 30% of salary saved (after CPF)
bonus_percentage_saved = 0.7 # i.e. 70% of bonus saved (after CPF)
promotion_years = [2, 4, 8, 15, 22] # Promotion years
rank_cap = 7500 # Current rank cap i.e. E1 -> E2 -> Senior -> Manager -> Senior Manager -> Director
rank_increase = 2500 # Increase in rank cap

# Variable Components initialized
BONUS_MONTHS = 4 # Number of bonus months
SALARY_INCREMENT = 0.035 # Salary increment rate
SALARY_PROMOTION = 0.07 # Salary promotion rate
INVESTMENT_RATE = 0.04 # Investment rate
INFLATION_RATE = 0.03 # Inflation rate

def main():
    total_savings_nominal = 0
    total_savings_real = 0
    cumulative_interest = 0

    salary = 6200
    for year in range(1, years + 1):
        print(f"Year {year}:")
        # Calculate variable components for this year
        bonus_months, salary_increment, salary_promotion, investment_rate, inflation_rate = calculate_variable_components(BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE)
        print(f"Bonus Months: {bonus_months}, Salary Increment: {salary_increment}, Salary Promotion: {salary_promotion}, Investment Rate: {investment_rate}, Inflation Rate: {inflation_rate}")
        # Calculates potential money saved this year
        savings = calculate_savings(salary, CPF_cap, salary_percentage_saved, bonus_percentage_saved, bonus_months)
        # Calculate tax payable this year
        total_tax, effective_tax_rate = calculate_tax(savings)
        # Effective Savings = Savings - Tax
        effective_savings = savings - total_tax
        # Factor in inflation and investment rate

        # Update total savings nominal and real, and cumulative interest

        # Update salary for next year
        salary = update_salary(salary, salary_increment, salary_promotion)


main()