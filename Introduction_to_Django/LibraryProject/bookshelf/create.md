# Create Operation
## Command
from bookshelf.models import Book
book = Book(title = "1984", author = "George Orwell", 
publication_year = 1949)
book.save()
print(book)
## Expected Output
1984 by George Orwell, published in 1949.
