#1 STRING COMPARISION 
# str_1 = 'Welcome to our Program'
# str_2 = 'Hello World' 
# str_3 = 'Welcome to our Program'

# print(str_1==str_3)
# print(str_1 + '. ' + str_2)
# print('a' in str_2)

#2 IF_ELSE
# age = int(input("Enter your age: "))
# if age < 18:
#     print(f"{age} is less than 18")
# else:
#     print(f"{age} is greater than 18")

#3 IF ELIF 
# number = int(input("Enter a number: "))
# if number == 0:
#     print(f"Entered number is {number}")
# elif number > 0:
#     print(f"Entered number is greater than 0.")
# else: 
#     print(f"Entered number is less than 0.")

#4 odd or even
#number = int(input("Enter a number: "))
# if number % 2 == 0:
#     print(f"{number} is an Even number.")
# else:
#     print(f"{number} is an Odd number.")

#5 IF_ELSE
# name = input("Enter your name: ")
# age = int(input("Enter your age: "))
# if age >= 18:
#     print(f"{name} is eligible to vote.")
# else:
#     print(f"{name} is not eligible to vote.")  


#6 
# city = input("Enter the city: ")

# if city == 'Tokyo':
#     print(f"You have entered {city}. Must visit place is Senso-ji.")
# elif city == 'Kyoto': 
#     print(f"You have entered {city}. Must visit place is Arashiyama.")
# else: 
#     print(f"You have entered {city}. Must visit place is Dotonbori.")

#7: 
# number1 = int(input("Enter your first number: "))
# number2 = int(input("Enter your second number: "))
# number3 = int(input("Enter your third number: "))

# if (number1 > number2) and (number1 > number3):
#     print(f"{number1} is maximum")
# elif (number2 > number3): 
#     print(f"{number2} is maximum")
# else: 
#     print(f"{number3} is maximum")


#8.
# age = int(input("Enter your age: "))

# if (age >= 0) and (age <= 12):
#     print("Child")
# elif (age >= 13) and (age <= 19):
#     print("Teenager")
# elif (age >= 20) and (age <= 59):
#     print("Adult")
# elif (age >= 60): 
#     print("Senior Citizen")


#9
weight = float(input("Enter your weight(in kgs): "))
height = float(input("Enter your height (in meters): "))

bmi = weight / (height * height)

if (bmi >= 0) and (bmi < 18.5):
    print(f"Your BMI is {bmi}, so Underweight.")
elif (bmi >= 18.5) and (bmi <= 24.9):
    print(f"Your BMI is {bmi}, so Normal weight")
elif (bmi >= 25) and (bmi <= 29.9):
    print(f"Your BMI is {bmi}, so Overweight")
elif (bmi >= 30): 
    print(f"Your BMI is {bmi}, so Obesity")