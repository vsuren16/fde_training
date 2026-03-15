#TASK1
def store_order_records():
    orders = []
    n = int(input("Enter number of orders: "))
    for i in range(n):
        print(f"\nOrder {i+1}")
        customer = input("Customer: ")
        product = input("Product: ")
        amount = float(input("Amount: "))
        orders.append((customer, product, amount))
    return orders
