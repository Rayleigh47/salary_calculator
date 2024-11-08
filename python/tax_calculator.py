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
    print(f"Tax Payable: ${total_tax:.2f}")
    print(f"Effective Tax Rate: {effective_tax_rate:.2f}%")
    return total_tax, effective_tax_rate
