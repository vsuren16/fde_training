###########################################################################################
#                             LOAN ELIGILITY CHECKER SYSTEM                               #
###########################################################################################

customer_name = input("Enter Customer Name: ")
customer_monthly_income = int(input("Enter Monthly Income: "))
customer_credit_score = int(input("Enter Credit Score: "))

if (customer_monthly_income >= 30000) and (customer_credit_score >= 700):
    print("--------------------------------------------")
    print("      Loan Eligibility Checker")
    print("--------------------------------------------")
    print(f" Customer Name: {customer_name}")
    print(" Status       : Eligible for Loan")
    print("--------------------------------------------")

else: 
    print("--------------------------------------------")
    print("      Loan Eligibility Checker")
    print("--------------------------------------------")
    print(f" Customer Name: {customer_name}")
    print(" Status       : Not Eligible for Loan")
    print("--------------------------------------------")