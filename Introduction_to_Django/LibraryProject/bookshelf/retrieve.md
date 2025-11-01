# Retrieve Operation
## Command
from bookshelf.models import Book
book = Book.objects.all()
print(book)

## Expected Output
<QuerySet [<Book: 1984 by George Orwell, published in 1949.>]>

