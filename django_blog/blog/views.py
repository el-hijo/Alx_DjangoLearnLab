from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = "blog/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("blog:login")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optional: log the user in immediately after registering
            login(request, user)
            return redirect("blog:profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    # simple profile view that renders current user information
    return render(request, "blog/profile.html", {"user": request.user})

