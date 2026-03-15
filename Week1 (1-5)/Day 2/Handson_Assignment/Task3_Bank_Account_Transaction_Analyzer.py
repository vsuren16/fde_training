
def customer_details(no_of_cust):

    i = 0
    j = 0
    cust_details_list = []
    
    while i < no_of_cust:
        
        cust_details_tup = ()
        j=i+1
        print(f"\nRecord {j}:")
        acc_name = input("Account Holder: ")
        acc_trans_type = input("Transaction Type: ")
        acc_trans_amount = int(input("Amount: "))

        cust_details_tup = (acc_name,acc_trans_type,acc_trans_amount)
        cust_details_list.append(cust_details_tup)

        i = i+1
    return cust_details_list

def customer_transaction_lookup(cust_trans):

    cust_transaction_dict = {'Deposit':'Amount has been credited to your account.',
                              'Withdrawal':'Amount has been deducted from your account.'}
    return cust_trans,cust_transaction_dict.get(cust_trans,"Invalid Service Type")

def customer_transaction_filter(cust_trans, cust_details_list):
    result = []
    for cust in cust_details_list:
        if cust[1] == cust_trans:
            result.append(cust)
    return result

no_of_cust = int(input("Enter no of customers: "))
cust_details_list = customer_details(no_of_cust)

cust_trans = input("\nEnter Transaction type to filter: ")
filtered_customers = customer_transaction_filter(cust_trans, cust_details_list)

if filtered_customers:
    print("-----------------------------------")
    print(f"{cust_trans} Transaction:")
    print("-----------------------------------")
    for acc_name, acc_trans_type, acc_trans_amount in filtered_customers: 
        trans_type, trans_type_detail = customer_transaction_lookup(cust_trans)
        print(f"Account Holder: {acc_name}")
        print(f"Amount: {acc_trans_amount}")
        print(f"Transaction Type Detail: {trans_type_detail}\n")
    print("-----------------------------------")
else:
    print("No matching customer data found for the city.")