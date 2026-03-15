# LIBRARY MANAGEMENT SYSTEM

class Book:
    
    def __init__(self,book_title,availability,user,lend_return_option):
        self.book_title = book_title 
        self.availability = availability
        self.user = user
        self.lend_return_option = lend_return_option

    def _book_details(self):
        print("Book Title: ", self.book_title)
        print("Availability: ", self.availability)

    def book_lending(self):

        if self.lend_return_option == 'lend':

            if self.availability > 1:
                self.availability = self.availability-1
                print(f"{self.book_title} book lended successfully to {self.user}. Current book availability is {self.availability}.")
            else:
                print("Currently, book is not available.")

    def book_returning(self):

        if self.lend_return_option == 'return':

            self.availability = self.availability+1
            print(f"{self.book_title} book returned successfully by {self.user}. Current book availability is {self.availability}.")

class Student(Book):

    def get_book_details(self):
        self._book_details()
        self.book_lending()
        self.book_returning()

class Staff(Book):

    def get_book_details(self):
        self._book_details()
        self.book_lending()
        self.book_returning()

b2 = Student('Wings of fire',5,'Student','lend')
b3 = Staff('Tomorrows Land',2,'Staff','return')

b2.get_book_details()
b3.get_book_details()
            

########################






