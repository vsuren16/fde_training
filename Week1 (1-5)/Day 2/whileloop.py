#1). ATM PIN ATTEMPT

# correct_pin = "1234"
# attempts = 0 

# while attempts < 3: 
#     customer_pin = input("Enter your ATM PIN: ")
#     if customer_pin =="":
#         print("PIN cannot be empty")
#         continue
#     if customer_pin == correct_pin: 
#         print("You have entered correct PIN. Login Successfull.")
#         break
#     if customer_pin != correct_pin: 
#         attempts = attempts + 1
#         if attempts < 3:
#             print("Incorrect Password. Retry.")
#         else:
#             print("Incorrect PIN. Your Card is Blocked.")
#         continue

#2). USER LOGIN ATTEMPT

# username = "Suren"
# password = "1234"
# attempts = 0
# attempt_left = 3

# while attempts < 3: 
#     username_entered = input("Enter your Username: ")
#     password_entered = input("Enter your Password: ")

#     if username_entered =="" or password_entered =="" :
#         print("Username or Password cannot be empty.")
#         continue

#     if username == username_entered and password == password_entered: 
#         print("Login Successfull.")
#         break
    
#     if username != username_entered or password != password_entered:
        
#         attempts = attempts+1
#         attempt_left = attempt_left-1

#         if attempts < 3:
#             print(f"Login Unsuccessful. Retry Attempt Left: {attempt_left}")
#         else:
#             print("Unauthorized User.")
#         continue


#3 SHOPPING CART 

cart = []

while True: 
    item = input("Enter item name: ")

    if item == 'checkout':
        print(f"You've entered Checkout. Items in the cart: {cart} \nPlease proceed for payment...")
        break

    if item == 'skip':
        print(f"Item Skipped.")
        continue

    cart.append(item)
    print(f"{item} added to cart.")



    