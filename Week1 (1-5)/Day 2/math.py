loan_amount = 78783.67
interest_rate = 8.75
tenure_years = 7 
monthly_income = 50000


principal = round(float(loan_amount))
months = tenure_years*12 
monthly_rate = interest_rate / (12 * 100)

emi = ( principal * monthly_rate * pow(1 + monthly_rate,months)) / ( pow(1+monthly_rate,months) -1 )

emi = abs(emi)

total_payment = emi * months

total_interest = total_payment - principal

emi_options = [1258,1547,1875]
max_emi = max(emi_options)
min_emi = min(emi_options)
average_emi = sum(emi_options)/len(emi_options)

print(f"Loan Amount (Rounded): {principal}") 
print(f"Tenure (Months): {months}") 
print(f"Monthly EMI: {round(emi,2)}") 
print(f"Total Payment: {round(total_payment,2)}") 
print(f"Total Interest: {round(total_interest,2)}") 
print(f"Max EMI Option: {max_emi}") 
print(f"Min EMI Option: {min_emi}") 
print(f"Average EMI: {round(average_emi,2)}")