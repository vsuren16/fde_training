

def customer_details(no_of_cust):

    i = 0
    cust_details_list = []
    
    while i < no_of_cust:
        
        cust_details_tup = ()

        cust_name = input("Enter Your Name: ")
        cust_city = input("Enter Your City: ")
        cust_plan_type = input("Enter Your Plan Type: ")

        cust_details_tup = (cust_name,cust_city,cust_plan_type)
        cust_details_list.append(cust_details_tup)

        i = i+1
    return cust_details_list

def customer_plan_lookup(cust_plan_type):

    cust_plan_details_dict = {'Prepaid':'Preaid plan - Need to recharge first and then use.',
                              'Postpaid':'Postpaid plan - Use first and then pay the bill amount later.'}
    return cust_plan_type,cust_plan_details_dict.get(cust_plan_type,"Invalid Plan Type")

def customer_city_filter(cust_city, cust_details_list):
    result = []
    for cust in cust_details_list:
        if cust[1] == cust_city:
            result.append(cust)
    return result


no_of_cust = int(input("Enter no of customers: "))
cust_details_list = customer_details(no_of_cust)
#print(cust_details_list)

# for record in cust_details_list:
#     plan_type  = record[2]
#     plan_type,plan_detail = customer_plan_lookup(plan_type)
#     print(plan_type,plan_detail)

cust_city = input("Enter City to filter: ")
filtered_customers = customer_city_filter(cust_city, cust_details_list)

if filtered_customers:
    print("---------------------")
    print("Customers in Chennai:")
    print("---------------------")
    for cust_name, cust_city, cust_plan_type in filtered_customers: 
        plan_type, plan_detail = customer_plan_lookup(cust_plan_type)
        print(f"Name: {cust_name}")
        print(f"Plan: {cust_plan_type}")
        print(f"Plan Detail: {plan_detail}\n")
    print("---------------------")
else:
    print("No matching customer data found for the city.")

