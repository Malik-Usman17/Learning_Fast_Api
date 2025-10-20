from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

#pydantic comes pre-installed with our fastapi installation.

'''
pydantic is the framework that allows us to do validation on our data and base model is what we're
going to be using for our model, which is the object coming in to be able to validate the variables
within the object itself.
'''

book_app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_date: int

    def __init__(self, book_id, title, author, description, rating, published_date):
        self.id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    #book_id: Optional[int] = None
    book_id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=0, lt=6)     #gt means greater than and lt means less than
    published_date: int = Field(gt=1999, lt=2031)


    model_config = {
        "json_schema_extra": {             #this "json_schema_extra" and "example" should be same
            "example": {
                "title": "A book title",
                "author": "Book's author name",
                "description": "Some detail about book",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science', 'Harry Brooks', 'Absolutely worth it!', 5, 2030),
Book(2, 'Crazy Techniques', 'Joe Root', 'Should read it once.', 4, 2030),
Book(3, 'A Tall Fast Bowler', 'Stephen Finn', 'Great book', 3.5, 2029),
Book(4, 'Computer Science', 'James Anderson', 'Absolutely worth it!', 5, 2028),
Book(5, 'Computer Science', 'Shawn Tait', 'Must read', 1, 2027),
Book(600, 'Swimmers', 'Michael Phelps', 'Amazing', 2, 2026)
]

@book_app.get("/books", status_code=status.HTTP_200_OK)
async def read_books():
    return BOOKS

'''
@book_app.post('/create_newBook')
async def create_book(book_request=Body()):
    BOOKS.append(book_request)
'''

@book_app.get('/books/publish/')
#async def read_books_by_publish_date(published_date: int):
async def read_books_by_publish_date(published_date: int=Query(gt=1999, lt=2031)):     # adding validation to query parameter
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@book_app.post('/create_newBook', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):     #book request type of book request
    #print(type(book_request))
    #BOOKS.append(book_request)
    new_book = Book(**book_request.model_dump())    #converting the request to Book object
    print(type(new_book))
    #BOOKS.append(new_book)
    BOOKS.append(find_book_id(new_book))


'''def find_book_id(book_param: Book):
    if len(BOOKS) > 0:
        book_param.id = BOOKS[-1].id + 1
    else:
        book_param.id = 1
    return book_param'''


#we can also write the above function with ternary operator
def find_book_id(book_param: Book):
    book_param.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book_param


@book_app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
#async def create_book(book_id: int):
async def create_book(book_id: int = Path(gt=0)):     #adding validation to path parameter
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


'''@book_app.get('/books/{book_rating}')           
async def find_book_by_rating(book_rating: float):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return'''

#So we cannot find out books by rating through path parameter concept for this we need to use query parameter,
#that's why I made the function again with query parameter.Query parameter is for filter data, path parameter is use to
#take out specific information (e.g., here it take out only one object)

@book_app.get('/books_rating')
#async def find_book_by_rating(book_rating: float):
async def find_book_by_rating(book_rating: float=Query(gt=0, lt=6)):  #adding validation to query parameter
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@book_app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_req: BookRequest):
    is_book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_req.book_id:
            BOOKS[i] = book_req
            is_book_changed = True
    if not is_book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@book_app.delete('/delete_books/{b_id}', status_code=status.HTTP_204_NO_CONTENT)
#async def delete_books(b_id: int):
async def delete_books(b_id: int = Path(gt=0)):   #adding validation to path parameter
    is_book_changed = False
    for b in range(len(BOOKS)):
        if BOOKS[b].id == b_id:
            BOOKS.pop(b)
            is_book_changed = True
            break
    if not is_book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
