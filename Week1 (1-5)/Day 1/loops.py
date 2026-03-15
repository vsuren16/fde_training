#1 demo statements
# s = 'Hello'
# for i in s: 
#     print(i)

# n=5
# for i in range(n): 
#     print(i)


#2 Get name and number of times and print the name that no of times
# name = input("Enter your name: ")
# number = int(input("Enter number of times to print: "))

# for i in range(number):
#     for j in name: 
#         print(j)


# 3 while loop
# c=0 
# while c<3: 
#     c = c+1 
#     print("hello")

#4 check for prime number or not 

number = int(input("Enter a number: "))

i = number - 1

while i > 0 and i < number:
    modulo = number%i 
    if modulo == 0: 
        print("This is not a prime number")
        break
    i = i-1
    print(f"Next iteration for {i}.")