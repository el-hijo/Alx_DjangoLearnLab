
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm

# View for creating a book
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# View for editing a book
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    return render(request, 'bookshelf/edit_book.html', {'form': form})

# View for deleting a book
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Create your views here.
