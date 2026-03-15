#1 File creation and writing

# with open("demo2.txt","w") as file: 
#     file.write("This is a demo file.\n")
#     file.write("It contains sample text for file operations.\n")
#     file.write("File handling is important in programming. \n")
#     print("File successfully created.")

#2 File reading 

with open("demo2.txt","r") as file: 
    content = file.read()
    print("The file contents :")
    print(content)