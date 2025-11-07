from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# ✅ Function-based view
def book_list(request):
    """Lists all books stored in the database"""
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


# ✅ Class-based view
class BookDetailView(DetailView):
    """Displays details for a specific library and its books"""
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(library=self.object)
        return context

    
    