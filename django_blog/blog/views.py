from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


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



class ListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   
    context_object_name = 'posts'
    paginate_by = 10                         

class DetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomUserCreationForm                # or use `fields = ['title', 'content']`
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # set the author automatically to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = CustomUserCreationForm                  # or fields = [...]
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class tDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')  # adjust namespace/name as you choose

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
