#1 WRITE the json file
# import json 

# data = [
#     {"id": 1, "name": "A"},
#     {"id": 2, "name": "B"}
# ]

# with open("newdata.json","w") as file:
#     json.dump(data, file, indent=4)


#2 READ the json file 

# import json 

# try:
#     with open("newdata.json","r") as file:
#         data = json.load(file)
#         print(data)
# except FileNotFoundError:
#     print("File does not exists. Please check the file name again")
# except Exception as e:
#     print("An error occurred:",e)
# finally: 
#     print("Execution completed.")


#3 Modify the data 
import json 

try: 
    with open("newdata.json","r") as file:
        data = json.load(file)

    #Modify
    data[0]['name'] = "Suren"
    data.append ( {'id': 3, 'name': 'ABC'})

    with open("newdata.json","w") as file:
        json.dump(data, file, indent=4)

except FileNotFoundError:
    print("File Not exist. Please check the filename.")

except Exception as e: 
    print("An error occured:",e)

finally:
    print("Execution completed.")

