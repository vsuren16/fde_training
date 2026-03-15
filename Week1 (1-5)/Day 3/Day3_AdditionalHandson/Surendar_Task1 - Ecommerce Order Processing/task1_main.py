# E-COMMERCE ORDER PROCESSING SYSTEM

from orders.order_records import store_order_records
from products.product_lookup import maintain_product_lookup
from display.display_orders import display_orders
from utils.filters import filter_orders_by_product

def main():
    #Task1 : Store Order Records
    orders = store_order_records()  
    #Task2 : Maintain Product Lookup
    product_lookup = maintain_product_lookup() 
    #Tast3: Filter Orders by Product
    display_orders(orders, product_lookup)
    #Task4: Final function call
    filter_orders_by_product(orders, product_lookup)  

main()  