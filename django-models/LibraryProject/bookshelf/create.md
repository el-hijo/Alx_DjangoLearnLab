# Create Operation
## Command
from bookshelf.models import Book
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()
print(book)
## Expected Output
1984 by George Orwell, published in 1949.
