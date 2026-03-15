#1 Class demo
# class Student:

#     #initializing the variables
#     def __init__(self,name,marks):
#         self.name = name 
#         self.marks = marks

#     def display(self):
#         print("Name: ", self.name)
#         print("Marks: ", self.marks)

# #object creation 

# s1 = Student("Kanna",60)
# s2 = Student("Ravi",90)

# s1.display()
# s2.display()


#2 Bank account class creation

class Bankaccount:

    def __init__(self,acc_no,acc_holder_name,acc_balance):
        self.acc_no = acc_no 
        self.acc_holder_name = acc_holder_name
        self.acc_balance = acc_balance

    def display_account(self):
        print("Account No: ", self.acc_no)
        print("Account Holder Name: ", self.acc_holder_name)
        print("Account Balance: ", self.acc_balance)

    def withdraw(self,withdraw_amount):
        if withdraw_amount <= self.acc_balance:
            self.acc_balance = self.acc_balance - withdraw_amount
            print(withdraw_amount,"withdraw completed.")
            print(self.acc_holder_name,"current Balance: Rs.",self.acc_balance)
        else: 
            print(self.acc_holder_name," has insufficient funds.")

    def deposit(self,deposit_amount):
        self.acc_balance = self.acc_balance + deposit_amount
        print(deposit_amount,"deposit completed.")
        print(self.acc_holder_name,"current Balance: Rs.",self.acc_balance)

# #object creation 

a1 = Bankaccount(123,"Suren",1000)
a2 = Bankaccount(234,"Siva",100)
a3 = Bankaccount(345,"Thiru",10000)

a1.display_account()
a1.withdraw(500)
a1.deposit(1000)

a2.display_account()
a2.withdraw(500)
a2.deposit(1000)

a3.display_account()
a3.withdraw(500)
a3.deposit(1000)


{ _id: 1, title: "Clean Code", author: "Robert Martin",category: "Programming", year: 2008,isbn: "978-0132350884", copies: 5, available: 3 },
{ _id: 2, title: "Python Programming", author: "Jane Asten",category: "Programming", year: 2001,isbn: "971-0132350456", copies: 10, available: 7 },
{ _id: 3, title: "Robotics", author: "Agatha Christie",category: "AI/ML", year: 1997,isbn: "978-01323508682", copies: 10, available: 8 },
{ _id: 4, title: "Concepts of NLP", author: "Chethan",category: "AI/ML", year: 2016,isbn: "972-0132350809", copies: 15, available: 12 },
{ _id: 5, title: "Civil Engineering", author: "Leo Tolstay",category: "Engineering", year: 2001,isbn: "978-0132350156", copies: 4, available: 3 },
{ _id: 6, title: "Basic concepts of Architect", author: "Stephen King",category: "Engineering", year: 2011,isbn: "978-013235088083", copies: 10, available: 5 },
{ _id: 7, title: "World War3", author: "JK Rowling",category: "History", year: 1987,isbn: "978-01323508955", copies: 5, available: 3 },
{ _id: 8, title: "Geopolitics in 90s", author: "Shakespere",category: "History", year: 1999,isbn: "974-01323508345", copies: 8, available: 7 },
{ _id: 9, title: "Right Investment", author: "Salman Rushdie",category: "Finance", year: 2005,isbn: "978-0132350867", copies: 6, available: 1 },
{ _id: 10, title: "Understanding F&O, Stocks", author: "Leo Tolstay",category: "Finance", year: 2011,isbn: "978-0132350222", copies: 10, available: 2 }


db.restaurants.find({ $or: [{availableSeats: {$lt:3}}, {cuisine: {$type: "array"}}]},{_id:0, name:1, availableSeats: 1})

db.ega.updateOne({title: 'miraj'}, {$set:{'rating':4}}, {upsert : true})