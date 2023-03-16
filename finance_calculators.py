'''
First "capstone" task: Variables and Control Structures
For this task, assume that you have been approached by a small financial
company and asked to create a program that allows the user to access two
different financial calculators: an investment calculator and a home loan
repayment calculator.
'''


import math

# Present the menu and ask user to state the calculation they want to do, or whether they want to quit

print('''Choose either 'investment' or 'bond' from the menu below to proceed:
    
investment  -   to calculate the amount of interest you'll earn on your investment
bond        -   to calculate the amount you'll have to pay on a home loan
''')

calculation_type = input("Please enter your selection (investment/bond), or stop to cancel: ").lower()

while calculation_type != "stop" and calculation_type != "bond" and calculation_type != "investment":
    calculation_type = input("Unrecognised selection, please enter investment, bond or stop: ").lower()


# Obtain the inputs from the user that apply to both calculation types (currency and interest rate)
if calculation_type != "stop":
    currency_symbol = input("Please enter the currency symbol for the calculation: ")
    interest_rate = float(input("Please enter the annual percentage interest rate (number only): "))
    interest_rate = interest_rate / 100   # Store over 100 for use as a multiplier


# For investment, first request the rate, length of time and type of interest (check interest type is valid)
# Additional input validation would be appropriate, but omitted here for clarity
if calculation_type == "investment":
    principal_sum = float(input("Please enter the amount of money you are depositing (number only): "))

    investment_years = int(input("Please enter a whole number of years for which you plan to invest: "))
    interest = input("Please enter the type of interest (simple/compound): ").lower()
    while interest != "simple" and interest != "compound":
        interest = input("Unrecognised selection, please enter simple or compound: ").lower()
    
    # Proceed to the calculations
    # Simple interest: gain is principal * time * rate
    if interest == "simple":
        investment_gain = principal_sum * investment_years * interest_rate
        final_value = principal_sum + investment_gain
    # Compound interest: final value is P(1 + r); use of math.pow is specified but ** would be equivalent
    else:
        final_value = principal_sum * math.pow((1 + interest_rate), investment_years)
        investment_gain = final_value - principal_sum

    # Give the user the results; truncate the results (won't pay out fractional pennies)
    print(f'''Your selections and outcomes are as follows:

        Yearly interest rate       {interest_rate * 100}%
        Value desposited           {currency_symbol}{principal_sum:.2f}
        Investment period (years)  {investment_years} years
        Interest gained            {currency_symbol}{investment_gain:.2f}
        Final value                {currency_symbol}{final_value:.2f}
        '''
    )


# For bond, first obtain the value and the number of repayment months, then do the calculations
if calculation_type == "bond":
    principal_sum = int(input("Please enter the present value of the house to the nearest whole number: "))
    repayment_months = int(input("Please enter a whole number of months over which you will repay the loan: "))

    # Calculate monthly repayment and provide the results using repayment = (rate * principal)/(1 - (1 + rate)^(-months))
    monthly_int_rate = interest_rate / 12
    monthly_payment = (monthly_int_rate * principal_sum) / (1 - math.pow((1 + monthly_int_rate), (-1 * repayment_months)))
    
    # Give the user the results
    print(f'''Your selections and outcomes are as follows:
        
        Yearly interest rate        {interest_rate * 100}%
        House value borrowed        {currency_symbol}{principal_sum:.2f}
        Repayment period (months)   {repayment_months} 
        Monthly payment             {currency_symbol}{monthly_payment:.2f}
        '''
    )