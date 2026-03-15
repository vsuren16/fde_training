#TASK 1
def filter_orders_by_product(orders, product_lookup):
    search_product = input("Enter product type to filter: ")
    print(f"\nOrders in {product_lookup.get(search_product, search_product)}")
    print("----------------------------------")
    found = False
    for order in orders:
        if order[1].lower() == search_product.lower():  
            print(f"Customer: {order[0]} Amount: {order[2]}")
            found = True
    if not found:
        print("No orders found in this product type.")
    print("----------------------------------")