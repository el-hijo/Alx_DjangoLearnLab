from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Book
from .models import Library
from .models import UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import UserProfile


def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# ✅ Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ✅ Function-based view: Book list
@login_required
def list_books(request):
    """Lists all books stored in the database"""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'list_books': books})


# ✅ Class-based view for Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ✅ Admin-only view
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# ✅ Librarian-only view
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


# ✅ Member-only view
@login_required
@user_passes_test(is_member)
def member_view(request):


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('relationship_app.can_add_book')
def add_book(request):
    # Placeholder for now
    pass

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    pass

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    pass
