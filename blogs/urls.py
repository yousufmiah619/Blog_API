from django.urls import path
from .views import blog_list_create

urlpatterns = [
    path('blogs/', blog_list_create),
]
