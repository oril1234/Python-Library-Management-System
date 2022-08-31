#A class of a book int the library
class Book:

    def __init__(self,author,title,num_of_pages) :
        self.__author=author
        self.__title=title
        self.__num_of_pages=num_of_pages

    def get_title(self):
        return self.__title
        
    def get_author(self):
        return self.__author

    def get_num_of_pages(self):
        return self.__num_of_pages
               


