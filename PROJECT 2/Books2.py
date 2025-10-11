from fastapi import FastAPI, Body

book_app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float

    def __init__(self, book_id, title, author, description, rating):
        self.id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1, 'Computer Science', 'Harry Brooks', 'Absolutely worth it!', 5),
Book(2, 'Crazy Techniques', 'Joe Root', 'Should read it once.', 4),
Book(3, 'A Tall Fast Bowler', 'Stephen Finn', 'Great book', 3.5),
Book(4, 'Computer Science', 'Harry Brooks', 'Absolutely worth it!', 5),
Book(5, 'Computer Science', 'Shawn Tait', 'Must read', 1),
Book(600, 'Swimmers', 'Michael Phelps', 'Amazing', 2)
]

@book_app.get("/books")
async def read_books():
    return BOOKS

@book_app.post('/create_newBook')
async def create_book(book_request=Body()):
    BOOKS.append(book_request)


