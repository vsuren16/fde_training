
# with open("demo1.txt","w") as file: 
#     file.write("This is a day 3 demo file.\n")
#     file.write("It contains sample text for file operations.\n")
#     file.write("File handling is important in programming. \n")
#     print("File successfully created.")

#1 Get the file name and open it in read mode and print the content in the file

filename = input("Enter file name: ")

try:
    with open(filename,"r") as file: 
        content = file.read()
        print("The file contents :")
        print(content)
except FileNotFoundError:
    print("File does not exists. Please check the file name again")
except Exception as e:
    print("An error occurred:",e)
finally: 
    print("Execution completed.")
