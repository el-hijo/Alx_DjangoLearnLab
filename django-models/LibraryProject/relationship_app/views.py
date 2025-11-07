from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view
def list_book(request):
    """Lists all books stored in the database"""
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'relationship_app/list_book.html', context)


#  Class-based view
class BookDetailView(DetailView):
    """Displays details for a specific library and its books"""
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(library=self.object)
        return context

    
    