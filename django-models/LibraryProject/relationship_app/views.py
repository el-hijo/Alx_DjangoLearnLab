from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import DetailView
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView


# Function-based view
def list_books(request):
    """Lists all books stored in the database"""
    books = Book.objects.all()
    context = {'list_book': books}
    return render(request, 'relationship_app/list_books.html', context)


#  Class-based view
class BookDetailView(DetailView):
    """Displays details for a specific library and its books"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(library=self.object)
        return context

    
    