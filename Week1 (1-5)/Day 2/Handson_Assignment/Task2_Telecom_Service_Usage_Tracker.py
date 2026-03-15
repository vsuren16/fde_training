
def customer_details(no_of_cust):

    i = 0
    j = 0
    cust_details_list = []
    
    while i < no_of_cust:
        
        cust_details_tup = ()
        j=i+1
        print(f"\nRecord {j}:")
        cust_name = input("Customer Name: ")
        cust_city = input("Customer City: ")
        cust_service_type = input("Service Type: ")

        cust_details_tup = (cust_name,cust_city,cust_service_type)
        cust_details_list.append(cust_details_tup)

        i = i+1
    return cust_details_list

def customer_service_type_lookup(cust_service_type):

    cust_service_details_dict = {'Data':'Data plan - To use internet. 200GB Limit.',
                              'Voice':'Voice plan - To Talk over call. 100 Mins Limit.',
                              'SMS':'SMS plan - To send messages. 100 SMS Limit.'}
    return cust_service_type,cust_service_details_dict.get(cust_service_type,"Invalid Service Type")

def customer_service_filter(cust_service, cust_details_list):
    result = []
    for cust in cust_details_list:
        if cust[2] == cust_service:
            result.append(cust)
    return result

no_of_cust = int(input("Enter no of customers: "))
cust_details_list = customer_details(no_of_cust)

cust_service = input("\nEnter Service to filter: ")
filtered_customers = customer_service_filter(cust_service, cust_details_list)

if filtered_customers:
    print("-----------------------------------")
    print(f"Customers using {cust_service} Service:")
    print("-----------------------------------")
    for cust_name, cust_city, cust_service_type in filtered_customers: 
        service_type, service_detail = customer_service_type_lookup(cust_service)
        print(f"Customer Name: {cust_name}")
        print(f"City: {cust_city}")
        print(f"Service Detail: {service_detail}\n")
    print("-----------------------------------")
else:
    print("No matching customer data found for the city.")