###########################################################################################
#                           TELCO CUSTOMER ONBOARDING SYSTEM                              #
###########################################################################################

import re

customer_name = input("Enter Customer Name: ")
customer_mobile = input("Enter Mobile Numer: ")
customer_city = input("Enter Customer City: ")

mobile_no_length = len(customer_mobile)

mobile_no_alphabets_check = bool(re.search(r"[A-Za-z]",customer_mobile))
mobile_no_spl_char_check = bool(re.search(r"[^A-Za-z0-9]",customer_mobile))

mobile_no_req_start_numbers = ["6","7","8","9"]
mobile_no_start = customer_mobile[0]

if mobile_no_start in mobile_no_req_start_numbers:
    mobile_no_start_check = True
else: 
    mobile_no_start_check = False


if (mobile_no_length == 10) and (mobile_no_alphabets_check == False) and (mobile_no_spl_char_check == False) and (mobile_no_start_check == True):
    final_validation_check  = True 
else: 
    final_validation_check = False 
    

if final_validation_check == True:
    print("--------------------------------------------")
    print("      Welcome to ABC Telecom Services")
    print("--------------------------------------------")
    print(f" Customer Name: {customer_name}")
    print(f" Mobile Number: {customer_mobile}")
    print(f" City         : {customer_city}")
    print("\nThank you for choosing our services.")
else: 
    print("--------------------------------------------")
    print("Invalid Mobile Number")
    print("--------------------------------------------")
    print("\nPlease enter a valid 10-digit mobile number starting with 6,7,8 or 9.")




