
from BookClass import Book
from LibraryClass import Library
from ShelfClass import Shelf
import requests
from pymongo import MongoClient
from bson import ObjectId

#Library object to hold its information
lib=Library()

#Returning the instructions to the user
def create_instructions_string():
    return ("For adding a book - Press 1.\n"+
    "For deleting a book - Press 2.\n"+
    "For changing books locations - Press 3.\n"+
    "For registering a new reader - Press 4.\n"+
    "For removing a reader - Press 5.\n"+
    "For searching books by author – Press 6.\n"+
    "For reading a book by a reader – Press 7.\n"+
    "For ordering all books – Press 8.\n"+
    "For saving all data – Press 9.\n"+
    "For loading data – Press 10.\n"+
    "For exit – Press 11.\n")

#True if authentication succeeded
found_user=False

#True if user wants to exit the program
exit_program=False

#Executed as long as the user did not login successfully or if he hasn't existed
#the program
while (not found_user) and (not exit_program):
    username=input("Please insert user name\n")
    email=input("Please insert email\n")
    resp = requests.get("https://jsonplaceholder.typicode.com/users?username="+username+"&email="+email)
    user = list(resp.json())
    if len(user)==0:
        answer=input("Wrong details! What would you like "+ 
        "to do? In order to retry login press 1. To exit program type any other key\n")
        if answer!="1":
            exit_program=True
    else:
        print("You have successfully logged in to the system")
        found_user=True

client = MongoClient(port=27017)

#Accessing a library data base in mongo db in which all the data
#related to shelves and books the have is stored
db = client["libraryDB"]

#A collection of shelves which contains the above mentioned data
shelves_collection = db["shelves"]

#Loading the data
shelves = shelves_collection.find({}) 
for shelf in shelves:
    shelf_obj=Shelf()

    for book in shelf["books"]:
        shelf_obj.add_book(Book(book["author"],book["title"],book["num_of_pages"]))

    lib.add_new_shelf(shelf_obj)


#The instructions prompted to the user in order to inform him what his options are
instructions=create_instructions_string()

#True only if the bellow while loop is true
is_first_iter=True      

#In every iteration of this loop the user selectes an action to perform in the library
#as long as he doesn't exit the program ( by typing 11)
while(not exit_program):

    #Executed if this is the first iteration of the loo[]
    if is_first_iter:
        is_first_iter=False
    else:
        input("Press Enter key to continue\n")

    #If the user inputs an empty choice it will be set to 11 ( terminating the loop)
    choice=input(instructions) or "11"

    #Executed when the user is interested in adding a new book to the library
    if choice=="1":
        lib.add_new_book()

    #Executed when the user is interested in deleting a book from the library
    elif choice=="2":
        lib.delete_book()

    #Executed when the user is interested in chnging locations of books in the library
    elif choice=="3":
        lib.change_locations()

    #Executed when the user is interested in registering a new reader 
    # ( who can borrow books) from the library
    elif choice=="4":
        lib.register_reader()
    
    elif choice=="5":
        lib.remove_reader()

    #Executed when the user is interested in viewing all the books written by 
    # an author he selects
    elif choice=="6":
        lib.search_books_by_author()

    #Executed when the user is interested in documenting a book borrowed by a reader
    elif choice=="7":
        lib.read_book()

    #Executed when the user is interested in orderring the books on the 
    #library shelves according to their number of pages
    elif choice=="8":
        lib.order_books()

    #Executed when the user is interested in saving the library data in a json file
    elif choice=="9":
        lib.save_data_in_json()

    #Executed when the user is interested in loading already existed data to the library
    #from json file
    elif choice=="10":
        lib.load_data_from_json()

    #Executed when the user is interested in existing the program
    elif choice=="11":
        exit_program=True