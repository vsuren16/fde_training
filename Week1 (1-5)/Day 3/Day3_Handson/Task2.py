# TELCO SUBSCRIBER MANAGEMENT SYSTEM

class Customer:
    def __init__(self, cust_id, cust_name, cust_city):
        self.__cust_id = cust_id 
        self.__cust_name = cust_name
        self.__cust_city = cust_city

    def get_customer_info(self):
        return f"Customer ID: {self.__cust_id}, Name: {self.__cust_name}, City: {self.__cust_city}"

class Sim:
    def __init__(self, sim_no, sim_status, sim_type):
        self.sim_no = sim_no 
        self.sim_status = sim_status
        self.sim_type = sim_type

    def get_sim_info(self):
        return f"SIM No: {self.sim_no}, Status: {self.sim_status}, Sim Type: {self.sim_type}"

# Parent class Plan
class Plan:
    def __init__(self, plan_name):
        self.plan_name = plan_name 

    def get_plan_details(self):
        return f"Plan Details for {self.plan_name}"

# Child class for Postpaid Plan
class PostpaidPlan(Plan):
    def __init__(self, plan_name, bill_date, sim):
        super().__init__(plan_name)  # Initialize Plan class
        self.bill_date = bill_date
        self.sim = sim  

    def get_plan_details(self):
        if self.sim.sim_status == "Activated":
            return f"{super().get_plan_details()} - Bill Date: {self.bill_date} - Monthly Rental: Rs.1000"
        else:
            return "Sim is in deactivated state, cannot show plan details."

# Child class for Prepaid Plan
class PrepaidPlan(Plan):
    def __init__(self, plan_name, data_limit, sim):
        super().__init__(plan_name)   # Initialize Plan class
        self.data_limit = data_limit
        self.sim = sim  

    def get_plan_details(self):
        if self.sim.sim_status == "Activated":
            return f"{super().get_plan_details()} - Data Limit: {self.data_limit}GB - Recharge Amount: Rs.1000"
        else:
            return "Sim is in deactivated state, cannot show plan details."

class Subscriber(Customer, Sim, Plan):
    def __init__(self, customer, sim, plan):
        self.customer = customer
        self.sim = sim
        self.plan = plan

    def display_subscriber_details(self):
        print("Subscriber Information:")
        print(self.customer.get_customer_info())
        print(self.sim.get_sim_info())

        if self.sim.sim_type == 'Prepaid':
            prepaid_plan = PrepaidPlan('Prepaid', 100, self.sim) 
            print(prepaid_plan.get_plan_details())
        else:
            # Create PostpaidPlan
            postpaid_plan = PostpaidPlan('Postpaid', '1st of every month', self.sim)  
            print(postpaid_plan.get_plan_details())


# Creating object for class
customer1 = Customer(101, 'Alice', 'New York')

# Postpaid Scenario
sim1 = Sim('12345', 'Dectivated', 'Postpaid')
subscriber1 = Subscriber(customer1, sim1, None)
subscriber1.display_subscriber_details()

# Prepaid Scenario
sim2 = Sim('67890', 'Activated', 'Prepaid')  
subscriber2 = Subscriber(customer1, sim2, None)
subscriber2.display_subscriber_details()
