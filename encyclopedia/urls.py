from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.page, name="page"),
    path("<str:title>/edit", views.edit, name="edit")
]
