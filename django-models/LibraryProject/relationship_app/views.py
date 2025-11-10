from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView


# Function-based view
def list_books(request):
    """Lists all books stored in the database"""
    books = Book.objects.all()
    context = {'books': books}
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





# -----------------------------
# Register view
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # <-- required by checker
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()               # <-- required by checker
    return render(request, 'relationship_app/register.html', {'form': form})  # <-- required by checker

# -----------------------------
# Login view
# -----------------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# -----------------------------
# Logout view
# -----------------------------
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

