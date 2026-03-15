#TASK1 

def display_orders(orders, product_lookup):
    print("\nAll Orders:")
    print("----------------------------------")
    for order in orders:
        prod_desc = product_lookup.get(order, order)
        print(f"Customer: {order} Product: {prod_desc} Amount: {order}")
    print("----------------------------------")
