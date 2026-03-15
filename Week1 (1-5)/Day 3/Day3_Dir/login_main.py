from login_package.login_module import validateuser

username = 'admin'
password = 'admin123'

if validateuser(username,password):
    print("Login Successfull")
else:
    print("Login Failed")
