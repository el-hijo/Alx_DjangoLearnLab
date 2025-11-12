# Update Operation
## Command
 book = Book.objects.get(title = "1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
## Expected Output
Nineteen Eighty-Four by George Orwell, published in 1949.
