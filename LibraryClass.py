
from gettext import find
from BookClass import Book
from ReaderClass import *
from ShelfClass import Shelf
import json
import os
import sys

#Library class to mangage its shelves, books and readers data
class Library:
    def __init__(self):
        #The library shelves
        self.__shelves=[]

        #Registered readers in the library who cab borrow books
        self.__readers=[]
    
    #Searching for an available shelves to put a new book on and returning them if exist
    def get_available_shelves(self):
        available_shelves_obj=filter((lambda s:
            s.check_full_shelf()==False),self.__shelves)

        available_shelves_list=list(available_shelves_obj)

        #An available shelf was found    
        if len(available_shelves_list)>0:    
            return available_shelves_list[0]

        return None
  

    #Add new shelf     
    def add_new_shelf(self,shelf):
        self.__shelves.append(shelf)

    #Add new book to the first available shelf in the library
    def add_new_book(self):
        
        author=input("Please enter book author\n") or "default author"
        title=input("Please enter book title\n") or "default title"
        num_of_pages=int(input("Please enter number of pages\n") or "100")
        book=Book(author,title,num_of_pages)
        available_shelf=self.get_available_shelves()

        #Adding the book to an available shelf as long as it was found
        if available_shelf is not None:
            available_shelf.add_book(book)
            print("Book was successfully added")

        print("Book addition failed")

    #Remove a book from a shelf in the library
    def delete_book(self):
        title=input("Please insert a book title to delete\n")
        for shelf in self.__shelves:
            shelf.delete_book(title)

    #Searching all books writte
    def search_books_by_author(self):
        author=input("Please enter author name\n")
        corresponding_books=[]

        #Adding to corresponding list of books the ones written by the selected author
        for shelf in self.__shelves:
            corresponding_books.extend(shelf.get_books_by_author(author))

        #Printing books written by selected author
        for book in corresponding_books:
            print(book.get_title())

        if len(corresponding_books)==0:
            print("No books written by "+author+" were found")

    #Change locations of books according to their titles
    def change_locations(self):
        title1=input("Insert first title\n")
        title2=input("Insert second title\n")
        shelf1_idx=None
        book1=None
        book1_idx=None

        shelf2_idx=None
        book2=None
        book2_idx=None
        for index,shelf in enumerate(self.__shelves):
            title1_result=shelf.get_book_and_index_by_title(title1)
            title2_result=shelf.get_book_and_index_by_title(title2)

            #Executed when a book with the title=title1 was found
            if title1_result is not None:
                (book1_idx,book1)=title1_result
                shelf1_idx=index

            #Executed when a book with the title=title2 was found
            if title2_result is not None:
                (book2_idx,book2)=title2_result
                shelf2_idx=index
        
        #Executed if at least one of the books was not found
        if shelf1_idx is None or shelf2_idx is None:
            print("Changing locations of books is not possible"
             +" because one or more of the books with the titles you provided "
             +" does not exist")
            return

        #Swapping the books
        self.__swap_books(book1,book1_idx,book2,book2_idx,shelf1_idx,shelf2_idx)
        

    #Change locations of books in a given shelf using their indices
    def change_locations_in_same_shelf(self,shelf_index,book1_idx,book2_idx):
        
        book1=self.__shelves[shelf_index].get_book_by_index(book1_idx)
        book2=self.__shelves[shelf_index].get_book_by_index(book2_idx)

        if book1 is None or book2 is None:
            print("Replacement is not possible because one of the locations"
            +" does does not have any book")
            return

        #Swapping the books
        self.__swap_books(book1,book1_idx,book2,book2_idx,shelf_index,shelf_index)


    #Changing locations of books according to their indices and shelves
    def __swap_books(self,book1,book1_idx,book2,book2_idx,shelf1_idx,shelf2_idx):

        #Swapping the books
        tmp=book1
        self.__shelves[shelf1_idx].set_book_in_location(book1_idx,
            book2)
        self.__shelves[shelf2_idx].set_book_in_location(book2_idx,
            tmp)
    
    def order_books(self):
        for shelf in self.__shelves:
            shelf.order_books_by_pages_num()

    #Register new reader in the library given his name and id
    def register_reader(self):
        id=int(input("Please insert reader id\n"))
        name=input("Please insert reader name\n")
        self.__readers.append(Reader(id,name))

    #Removing reader given his name
    def remove_reader(self):
        name=input("Please insert reader name to delete\n")
        updated_readers=filter((lambda r:
            r.get_name()!=name),self.__readers)
        self.__readers=list(updated_readers)

    #Adding a book to a reader based on input from the user
    def read_book(self):
        reader_id=int(input("Please provide reader id\n"))
        book_title=input("Please provide the title of the book\n")
        readers=list(filter((lambda r:
            r.get_id()==reader_id),self.__readers))
        
        if len(readers)==0:
            print("No reader with the id "+reader_id+" was found")
            return
        reader=readers[0]
        book=None

        #Adding to corresponding list of books the ones written by the selected author
        for shelf in self.__shelves:

            # get_book_and_index_by_title returns a tuple of the book instance and its
            #index. The second element of the tuple is the book instance
            result=shelf.get_book_and_index_by_title(book_title)


            #Executed if book was found
            if result is not None:
                book=result[1]
                break



        if book is None:
            print("No book titled "+book_title+" was found")
            return
        
        reader.read_book(book.get_title())
        

    #Save all the library data, including shelves, books and readers in a json file    
    def save_data_in_json(self):
        library_json={}
        library_json["shelves"]=[]
        for shelf in self.__shelves:
            shelf_json={}
            
            shelf_json["is_shelf_full"]=shelf.check_full_shelf()
            shelf_json["books"]=[]

            for book in shelf.get_books():
                book_json={}
                book_json["author"]=book.get_author()
                book_json["title"]=book.get_title()
                book_json["num_of_pages"]=book.get_num_of_pages()
                shelf_json["books"].append(book_json)

                

            library_json["shelves"].append(shelf_json)
        
        library_json["readers"]=[]
        for reader in self.__readers:
            reader_json={}
            
            reader_json["id"]=reader.get_id()
            reader_json["name"]=reader.get_name()
            reader_json["books"]=reader.get_borrowed_books()
            library_json["readers"].append(reader_json)

        with open(os.path.join(sys.path[0],"library_json.json"),'w') as f:
            json.dump(library_json,f,indent=4)

    
    #Loading library data - including shekves, readers and books from a json file 
    def load_data_from_json(self):

        #Removing any previous data from libary in order to load it with data from json
        self.clear_data()
        file_path=input("Please Select file to load data from\n")
        if not os.path.exists(file_path):
            print("NO SUCH FILE!")
            return

        with open(os.path.join(sys.path[0],file_path),'r') as f:
            data = json.load(f)

            shelves = data["shelves"]
            for shelf in shelves:
                #Shelf object to add to library
                shelf_obj=Shelf()
                for book in shelf["books"]:
                    #Book object to add to shelf
                    book_obj=Book(book["author"],book["title"],book["num_of_pages"])
                    shelf_obj.add_book(book_obj)
                
                #Add shelf to library
                self.__shelves.append(shelf_obj)

            readers = data["readers"]
            for reader in readers:
                #reader object to add to library
                reader_obj=Reader(reader["id"],reader["name"])

                #Add to reader object data about books the reader borrowed
                reader_obj.add_books_loans(reader["books"])
                
                #Add reader to library
                self.__readers.append(reader_obj)


    #Clearing library data - activated when data is loaded from json file
    def clear_data(self):
        self.__shelves=[]
        self.__readers=[]


