from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("Create New Page/", views.new_page, name="newPage"),
    path("Random page/", views.random_page, name="random"),
    path("<str:title>/Edit Page/", views.edit_page, name="editPage")
]
