#1). EVEN OR ODD PROGRAM 

#number = int(input("Enter a number:"))

#function model one
# def evenodd(number): 
#     if number%2==0:
#         print(f"{number} is Even.")
#     else: 
#         print(f"{number} is Odd.")

#evenodd(number)

#function model two
# def even_odd(number):
#     if number % 2 == 0: 
#         return "Even"
#     else:
#         return "Odd"


#function model three - refactoring
# def even_odd2(number):
#     return "Even" if number % 2 == 0 else "Odd"

# result = even_odd2(number)
# print(result)

##---------------------------------

#2). Find the vowels present in string

# input = input("Enter a string:")

# def print_vowels(input):
#     vowel_present = []
#     for i in input:
#         if i.lower() in 'aeiou':
#             vowel_present+=i;
#     return vowel_present

# result = print_vowels(input)
# print(result)

##----------------------------------

#3). *numbers - example for N of arguments

# def calculate_total(*numbers):
#     total = 0
#     for i in numbers:
#         total = total+i
#     return total 


# result = calculate_total(1,2,3)
# print(result)

##4----------------------------------

username = "Suren"
password = "1234"

username_entered = input("Enter your Username: ")
password_entered = input("Enter your Password: ")

def user_login_check(username,password,username_entered,password_entered):
    if username == username_entered and password == password_entered:
        return True
    else:
        return False 

if user_login_check(username,password,username_entered,password_entered):
    print("Login Successfull")
else: 
    print("Login Unsuccessfull")