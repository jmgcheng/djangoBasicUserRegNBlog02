# just clone
```
git clone https://github.com/jmgcheng/djangoBasicUserRegNBlog02.git
```



# installations
```
> python -m venv env
> env\Scripts\activate
> pip install Django
> django-admin startproject core
> cd core
> code .
> python manage.py startapp pages
> python manage.py startapp accounts
> python manage.py startapp posts
> pip install crispy-bootstrap5
> pip install django-crispy-forms
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver
```



# settings
```
import os
INSTALLED_APPS = [
        ...

    'core',
    'crispy_forms',
    'crispy_bootstrap5',
    'pages',
    'accounts',
    'posts',
]
TEMPLATES = [
    {
        'BACKEND': ...
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        ...
    },
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_REDIRECT_URL = 'post-list'
LOGOUT_REDIRECT_URL = 'post-list'
LOGIN_URL = 'login'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # For testing email sending
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```



# template structure
```
core/core/templates/base.html
core/pages/templates/pages/about.html
core/accounts/templates/accounts/login.html
core/accounts/templates/accounts/password_reset_complete.html
core/accounts/templates/accounts/password_reset_confirm.html
core/accounts/templates/accounts/password_reset_done.html
core/accounts/templates/accounts/password_reset_form.html
core/accounts/templates/accounts/profile.html
core/accounts/templates/accounts/profile_update.html
core/accounts/templates/accounts/register.html
core/accounts/templates/accounts/
core/accounts/templates/accounts/
core/posts/templates/posts/post_detail.html
core/posts/templates/posts/post_form.html
core/posts/templates/posts/post_list.html
```



# core/urls.py
```
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import register, profile, profile_update
urlpatterns = [
    path('admin/', admin.site.urls),
    path("posts/", include("posts.urls")),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path('', include('pages.urls')),
]
```



# pages/urls.py
```
from django.urls import path
from pages.views import index, about
urlpatterns = [
    path('', index, name='homepage'),
    path('about-us', about, name='about-us'),
]
```



# accounts/urls.py
```
# none
```



# posts/urls.py
```
from django.urls import path
from posts.views import post_list, post_create, post_update, post_delete
urlpatterns = [
    path("", post_list, name="post-list"),
    path("<int:pk>/", post_detail, name="post-detail"),
    path("create/", post_create, name="post-create"),
    path("<int:pk>/update/", post_update, name="post-update"),
    path("<int:pk>/delete/", post_delete, name="post-delete"),
]
```



# pages/models.py
```
# none
```



# accounts/models.py
```
# none
```



# posts/models.py
```
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
```



# accounts/forms.py
```
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
```



# posts/forms.py
```
from django import forms
from posts.models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
```



# core/templates/base.html
```
{% load static %} 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <title>Document</title>
</head>
<body>
    <div class="container">
    <header class="p-3 mb-3 border-bottom">
        <div class="container">
        <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
            <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none">
            <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap"><use xlink:href="#bootstrap"></use></svg>
            </a>
            <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
            <li><a href="{% url 'homepage' %}" class="nav-link px-2 link-secondary">Home</a></li>
            <li><a href="{% url 'about-us' %}" class="nav-link px-2">About</a></li>
            </ul>
            {% if user.is_authenticated %}
            <div class="dropdown text-end">
                <a href="#" class="d-block link-body-emphasis text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                <img src="https://github.com/jmgcheng.png" width="32" height="32" class="rounded-circle">
                </a>
                <ul class="dropdown-menu text-small">
                <li><a class="dropdown-item" href="{% url 'profile' %}">Profile</a></li>
                <li><hr class="dropdown-divider"></li>
                <li>
                    <form action="{% url 'logout' %}" method="post">
                    {% csrf_token %}
                    <button type="submit" class="dropdown-item">
                        Logout
                    </button>
                    </form>
                </li>
                </ul>  
            </div>
            {% else %}
            <div class="text-end">
                <a href="{% url 'login' %}" class="btn btn-outline-primary me-2">Login</a>
                <a href="{% url 'register' %}" class="btn btn-primary">Register</a>
            </div>
            {% endif %}
        </div>
        </div>
    </header>
    <div class="row">
        <div class="col">
        {% block content %}
        {% endblock %}
        </div>
    </div>
    </div>  
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
```



# pages/templates/pages/about.html
```
{% extends "base.html" %}
{% block content %}
<h2>About Us</h2>
{% endblock %}
```



# accounts/templates/accounts/login.html
```
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form | crispy }}
    <hr>
    <button class="btn btn-primary btn-block" type="submit">Login</button>
    <a href="{% url 'password_reset' %}" class="btn btn-secondary">Forgot Password?</a>
</form>
{% endblock %}
```



# accounts/templates/accounts/password_reset_complete.html
```
{% extends "base.html" %}
{% block content %}
<p>Your password has been successfully reset. You may now <a href="{% url 'login' %}">login</a>.</p>
{% endblock %}
```



# accounts/templates/accounts/password_reset_confirm.html
```
{% extends "base.html" %}
{% block content %}
<h2>Set New Password</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Reset Password</button>
</form>
{% endblock %}
```



# accounts/templates/accounts/password_reset_done.html
```
{% extends "base.html" %}
{% block content %}
<p>An email has been sent with instructions to reset your password.</p>
{% endblock %}
```



# accounts/templates/accounts/password_reset_form.html
```
{% extends "base.html" %}
{% block content %}
<h2>Reset Password</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Reset Password</button>
</form>
{% endblock %}
```



# accounts/templates/accounts/profile.html
```
{% extends "base.html" %}
{% block content %}
<h2>Profile</h2>
<p>Username: {{ user.username }}</p>
<p>Email: {{ user.email }}</p>
<p><a href="{% url 'profile_update' %}">Update Profile</a></p>
{% endblock %}
```



# accounts/templates/accounts/profile_update.html
```
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<h2>Update Profile</h2>
<form method="post">
    {% csrf_token %}
    {{ form | crispy }}
    <hr>
    <button class="btn btn-primary btn-block" type="submit">Save Changes</button>
</form>
{% endblock %}
```



# accounts/templates/accounts/register.html
```
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<h2>Register</h2>
<form method="post">
    {% csrf_token %}
    {{ form | crispy }}
    <hr>
    <button class="btn btn-primary btn-block" type="submit">Register</button>
</form>
{% endblock %}
```



# posts/templates/posts/post_detail.html
```
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<h2>{{ post.title }}</h2>
<p>{{ post.content }}</p>
<p><small>By {{ post.author.username }} on {{ post.created_at }}</small></p>
{% if post.author == request.user %}
    <form action="{% url 'post-delete' post.pk %}" method="post" style="display:inline;">
        {% csrf_token %}
        <a href="{% url 'post-update' post.pk %}" class="btn btn-primary">Edit</a>
        <button class="btn btn-danger" type="submit">Delete</button>
    </form>
{% endif %}
<a href="{% url 'post-list' %}" class="btn btn-secondary">Back to Posts</a>
{% endblock %}
```



# posts/templates/posts/post_form.html
```
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<h2>{% if form.instance.pk %}Edit Post{% else %}Create Post{% endif %}</h2>
<form method="post">
    {% csrf_token %}
    {{ form | crispy }}
    <hr>
    <button class="btn btn-primary" type="submit">Save</button>
    <a href="{% url 'post-list' %}" class="btn btn-secondary">Back to Posts</a>
</form>
{% endblock %}
```



# posts/templates/posts/post_list.html
```
{% extends "base.html" %}
{% block content %}
<h2>All Posts</h2>
<a href="{% url 'post-create' %}">Create New Post</a>
<ul>
    {% for post in posts %}
        <li>
            <a href="{% url 'post-detail' post.pk %}">{{ post.title }}</a> by {{ post.author.username }} | {{ post.created_at }}
        </li>
    {% endfor %}
</ul>
{% endblock %}
```



# pages/views.py
```
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, reverse, render
def index(request):
    return HttpResponseRedirect(reverse('post-list'))
def about(request):
    # return HttpResponse('About Us')
    return render(request, "pages/about.html")
```



# accounts/views.py
```
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
@login_required
def profile(request):
    return render(request, "accounts/profile.html")
@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/profile_update.html", {"form": form})
```



# posts/views.py
```
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from posts.forms import PostForm
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("post-list")
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect("post-list")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("post-detail", pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect("post-list")
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect("post-list")
```