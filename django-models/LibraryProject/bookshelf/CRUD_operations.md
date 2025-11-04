# CRUD_operations SUMMARY

# Create Operation.
## Command
from bookshelf.models import Book
book = Book(title = "1984", author = "George Orwell", 
publication_year = 1949)
book.save()
print(book)
## Expected Output
1984 by George Orwell, published in 1949.

# Retrieve Operation
## Command
from bookshelf.models import Book
book = Book.objects.all()
print(book)
## Expected Output
<QuerySet [<Book: 1984 by George Orwell, published in 1949.>]>

# Update Operation
## Command
 book = Book.objects.get(title = "1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
## Expected Output
Nineteen Eighty-Four by George Orwell, published in 1949.

# Delete Operation
## Command
book = Book.objects.get(title = "Nineteen Eighty-Four")
book.delete()
print(book)
Book.objects.get(title = "1984")
## Expected Output
(1, {'bookshelf.Book': 1})
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\HP\AppData\Local\Programs\Python\Python311\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\HP\AppData\Local\Programs\Python\Python311\Lib\site-packages\django\db\models\query.py", line 633, in get
    raise self.model.DoesNotExist(
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.

