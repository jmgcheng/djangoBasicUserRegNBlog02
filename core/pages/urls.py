from django.urls import path
from pages.views import index, about
urlpatterns = [
    path('', index, name='homepage'),
    path('about-us', about, name='about-us'),
]