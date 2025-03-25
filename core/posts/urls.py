from django.urls import path
from posts.views import post_list, post_create, post_update, post_detail, post_delete


urlpatterns = [
    path("", post_list, name="post-list"),
    path("<int:pk>/", post_detail, name="post-detail"),
    path("create/", post_create, name="post-create"),
    path("<int:pk>/update/", post_update, name="post-update"),
    path("<int:pk>/delete/", post_delete, name="post-delete"),
]
