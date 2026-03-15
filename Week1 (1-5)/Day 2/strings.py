#1). Multiple 

email = '  surendar.v@COMP.com   '

def email_format(email):
    email = email.strip() 
    email = email.lower()
    return email 

def email_validate(email):
    if "@" in email and "." in email:
        username,domain = email.split("@")
        name_with_space = username.replace("."," ")
        employee_name = name_with_space.title()
        return username,domain,employee_name
    else:
        return False

def domain_validation(Domain):
    if Domain.lower().endswith("comp.com"):
        return True 
    else:
        return False

result = email_format(email) 
email_len = len(email)
Username,Domain,Employee_name =  email_validate(email)
if domain_validation(Domain) == True:
    Valid = 'Yes'
else:
    Valid = 'No'
print(f"Employee_name : {Employee_name}" )
print(f"Username : {Username}" )
print(f"Domain : {Domain}" )
print(f"Valid Email: {Valid}")
print(f"Email Length : {email_len}" )

