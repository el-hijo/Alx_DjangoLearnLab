# Delete Operation
## Command
book = Book.objects.get(title = "Nineteen Eighty-Four")
book.delete()
(1, {'bookshelf.Book': 1})
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
