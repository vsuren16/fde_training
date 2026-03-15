###########################################################################################
#                               TELECOM PLAN BILLING SYSTEM                               #
###########################################################################################

customer_name = input("Enter Customer Name: ")
customer_plan_type = input("Enter Plan Type: ")
customer_no_of_calls = int(input("Enter Number of Calls: "))

if customer_plan_type == 'Prepaid':
    bill_amount = customer_no_of_calls * 1
elif customer_plan_type == 'Postpaid':
    bill_amount = 199 + (customer_no_of_calls * 0.75)
else: 
    print("--------------------------------------------")
    print("Please enter valid plan type.")
    print("--------------------------------------------")

if (customer_plan_type == 'Prepaid') or (customer_plan_type == 'Postpaid'):
    print("--------------------------------------------")
    print("      Telecom Billing Details")
    print("--------------------------------------------")
    print(f" Customer Name: {customer_name}")
    print(f" Plan Type    : {customer_plan_type}")
    print(f" Total Bill   : ₹{bill_amount}")
    print("--------------------------------------------")
    print("\nThank you for choosing our services.\n")