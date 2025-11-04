# Retrieve Operation
## Command
from bookshelf.models import Book
Book.objects.get(title="1984")
print(book)

## Expected Output
<QuerySet [<Book: 1984 by George Orwell, published in 1949.>]>

