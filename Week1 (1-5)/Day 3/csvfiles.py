#1. CSV WRITE
# import csv 

# data = [
#     ["id","name","marks"],
#     [101,"Ram",85],
#     [102,"Ravi",90]
# ]

# with open("students.csv","w",newline="") as file:
#     writer = csv.writer(file)
#     writer.writerows(data)
# print("Data written successfully.")

#2. CSV READER 
import csv 

try: 
    with open("student.csv","r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

except FileNotFoundError: 
    print("CSV File not found")