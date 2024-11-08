import numpy as np
def calculate_variable_components(BONUS_MONTHS, SALARY_INCREMENT, SALARY_PROMOTION, INVESTMENT_RATE, INFLATION_RATE):
    # Define mean values and standard deviations realistically
    params = {
        "bonus_months": (BONUS_MONTHS, 0.5), # 3.5-4.5 months
        "salary_increment": (SALARY_INCREMENT, 0.01), # 2.5% to 4.5%
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