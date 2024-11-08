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
    print(f"Total Savings: ${total_saved:.2f}")
    return total_saved
