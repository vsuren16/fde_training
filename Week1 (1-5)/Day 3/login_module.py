def validateuser(username,password):

    entered_username = input("Enter Customer Name: ")
    entered_password = input("Enter your password: ")
    
    if entered_username == username and entered_password == password:
        return True 
    else: 
        return False