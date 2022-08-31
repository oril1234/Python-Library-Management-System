
from datetime import date

#Class of registered reader in the library
class Reader:
    def __init__(self,id,name) :
        #Reader ID
        self.__id=id

        #Reader name
        self.__name=name

        #Informations about books borrowed by the reader - the title of the book and 
        #the date it was borrowed by the reader
        self.__books=[]
    
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name   

    #Recording a loan of a book
    def read_book(self,book_title):

        today=date.today()

        #String representation of current date in the format dd/mm/yyyy
        today_str=str(today.day)+"/"+str(today.month)+"/"+str(today.year)
        book={}
        book["title"]=book_title
        book["date"]=today_str
        self.__books.append(book)
    
    #Load the data structure of book loans with already prepared data
    def add_books_loans(self,books_loans_data):
        self.__books.extend(books_loans_data)

    def get_borrowed_books(self):
        return self.__books
        


        



