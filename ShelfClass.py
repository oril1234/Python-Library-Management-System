
from ast import Delete

#class a library shelf containing books
class Shelf:

    #Maximum number of books allowed on the shelf
    MAX_BOOKS=5
    def __init__(self) :
        self.__books=[]
        self.__is_shelf_full=False
    
    def get_books(self):
        return self.__books
    
    def check_full_shelf(self):
        return self.__is_shelf_full

    #Add new book to shelf
    def add_book(self,book):

        self.__books.append(book)

        #Executed if shelf becomes full after adding a book
        if len(self.__books)==self.MAX_BOOKS:
            self.__is_shelf_full=True

    #Replace the locations of 2 books on the sfelf given their indices
    def replace(self,first_index,second_index):
        if len(self.__books)==0:
            print("There are no books to replace")
            return

        if first_index+1>len(self.__books):
            print("There is no book in index number "+first_index)
            return

        if second_index+1>len(self.__books):
            print("There is no book in index number "+first_index)
            return

        #Replacing the books
        tmp=self.__books[first_index]
        self.__books[first_index]=self.__books[second_index]
        self.__books[second_index]=tmp

    #Delete book from shelf
    def delete_book(self,title):
        curr_len=len(self.__books)
        self.__books=list(filter(lambda book: book.get_title()!=title,self.__books))

        #Comparing number of books on the shelf after the deletion of the book
        #and before. If there is no change it means the book was not on the shelf
        #in the first place
        if len(self.__books)<curr_len:
            print("The book"+title+" has been deleted")



    #Order the books on the shelf by their numbers of pages in ascending order
    def order_books_by_pages_num(self):
        self.__books.sort(key=lambda book: book.get_num_of_pages())

    #This method find a book with the given title and returns its instance and index
    def get_book_and_index_by_title(self,title):
        indices= [(i,book) for i,book in enumerate(self.__books) 
        if book.get_title()==title] 
        if len(indices)==0:
            return None


        #Returning book and index as long as they were found
        return indices[0]


    #Returning book according to index in books list
    def get_book_by_index(self,index):
        if len(self.__books[index])<index+1:
            return None
        
        return self.__books[index]


    def get_books_by_author(self,author):
        return list(filter((lambda b:
            b.get_author()==author),self.__books))        


    #Putting a book on a specific location on the shelf
    def set_book_in_location(self,index,book):
        self.__books[index]=book
