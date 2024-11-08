import numpy as np
# Calculate variable components for the year e.g. bonus months, salary increment, salary promotion, investment rate, inflation rate
def calculate_variable_components(BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE):
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
    # Return the generated values
    return parameters

# Raw calculation of earnings for the year
def calculate_earnings(salary, bonus_months):
    # Calculate total salary + bonus for the year
    total_salary = salary * 12
    total_bonus = salary * bonus_months
    total = total_salary + total_bonus
    return total

# calculate savings in a year based off salary, total number of months
def calculate_savings(salary, CPF_cap, salary_percentage_saved, bonus_percentage_saved, bonus_months):
    # Calculate true salary after CPF deduction (capped at CPF cap)
    if salary > CPF_cap:
        true_salary = salary - (CPF_cap * 0.2)
    else:
        true_salary = salary * 0.8
    # Calculate savings from salary and bonus
    saved_salary = true_salary * 12 * salary_percentage_saved
    saved_bonus = true_salary * bonus_months * bonus_percentage_saved
    total_saved = saved_salary + saved_bonus
    return total_saved

# Naive tax calculator for Singapore tax rates assuming no tax relief or deductions
def calculate_tax(chargeable_income):
    # Taxable income ranges with gross tax payable up to each limit from IRAS website
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
            total_tax = (chargeable_income - bracket_limit) * rate + gross_tax_up_to
            break
    # Calculate the effective tax rate as a percentage
    effective_tax_rate = (total_tax / chargeable_income) * 100 if chargeable_income > 0 else 0
    return total_tax, effective_tax_rate

# Update total savings nominal and real as well as cumulative interest
def update_savings(effective_savings, total_savings_nominal, total_savings_real, investment_rate, inflation_rate):
    # Update total savings nominal which is effective_savings * (1 + investment_rate)
    total_savings_nominal += effective_savings * (1 + investment_rate)
    # Update total savings real which is total savings nominal - inflation rate
    total_savings_real = total_savings_nominal / (1 + inflation_rate)
    return total_savings_nominal, total_savings_real

# Update salary for next year based off salary increment and promotion, promotion years, rank cap and rank increase
def update_salary(salary, salary_increment, salary_promotion, year, promotion_years, rank_cap, rank_increase):
    # Check if current year is a promotion year
    if year in promotion_years:
        # Increase rank cap by rank increase
        rank_cap += rank_increase
        # Increase salary by salary promotion rate
        salary *= (1 + salary_promotion)
    else:
        if salary < rank_cap:
            # If salary is below rank cap, increase salary by salary increment rate
            salary *= (1 + salary_increment)
    return salary
