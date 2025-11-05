from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    """returns all books written by a specified author."""
    try:
        author = Author.objects.get(name =author_name),objects.filter(author=author)
        books = author.books.all()
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"-{book.title}")
            
    except Author.DoesNotExist:
        print(f"No author found with the name '{author_name}'.")
        
     
def books_in_library(library_name):
    """returns all books available in a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExitst:
        print(f"No library found with the '{library_name}'.")
        
def librarian_for_library(library_name):
    """returns the librarian responsible for a given library."""
    try: 
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"\nLibrarian for {library_name}: {librarian.name}") 
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to the library '{library_name}'.") 
        
        
if __name__ == "__main__":
    books_by_author("George Orwell") 
    books_in_library("Central Library")
    librarian_for_library("Central Library")     