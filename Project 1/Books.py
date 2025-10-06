from fastapi import FastAPI, Body


my_app = FastAPI()

Books = [
    {'title': 'Good Habits', 'author': 'Author 1', 'category': 'life'},
    {'title': 'Book 2', 'author': 'Author 2', 'category': 'science'},
    {'title': 'Good Habits PartII', 'author': 'Author 3', 'category': 'life'},
    {'title': 'Book 3', 'author': 'Author 4', 'category': 'geography'},
    {'title': 'Book 4', 'author': 'Author 1', 'category': 'geography'},
]

@my_app.get("/my_books")
async def read_all_books():
    #return {"message": "Hello Mr. Thomas Michael!!"}
  return Books

'''
@my_app.get("/my_books/fav_book")
async def read_fav_book():
    return {'book title': 'Favorite Book!!!'}


@my_app.get("/my_books/{dynamic_parameter}")
async def read_one_book(dynamic_parameter: str):
    return {'my_dynamic_parameter': dynamic_parameter}
'''

#Path parameter
@my_app.get("/my_books/{author_name}")
async def get_author_name(author_name: str):
    for book in Books:
        if book.get('author').casefold() == author_name.casefold():
            return book

#Query Parameter
@my_app.get("/my_books_category")
async def get_books_category(category: str):
    books = []
    for book in Books:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books


#Path parameter and Query parameter
@my_app.get("/my_books/{book_author}/")
async def get_books_author_category(book_author: str, category: str):
    books = []
    for book in Books:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
          books.append(book)
    return books


#Post api
@my_app.post("/my_books/add_new_book")
async def create_book(new_book=Body()):
    Books.append(new_book)


#Put api
@my_app.put("/my_books/update_book")
async def update_book_info(update_book=Body()):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == update_book.get('title').casefold():
            Books[i] = update_book


#Delete api
@my_app.delete("/my_books/delete_book/{book_name}")
async def delete_book(book_name: str):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == book_name.casefold():
            Books.pop(i)
            break


#Revision query parameter
@my_app.get("/fetch_author_books")
async def get_author_books(author_name: str):
    books = []
    for book in Books:
        if book.get('author').casefold() == author_name.casefold():
            books.append(book)
    return books