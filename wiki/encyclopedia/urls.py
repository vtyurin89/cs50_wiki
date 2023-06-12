from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.show_entry, name="show_entry"),
    path("search/", views.search, name='search'),
    path("random_page/", views.random_page, name='random_page'),
    path('create_page/', views.create_page, name='create_page'),
    path('edit_page/<str:entry_name>', views.edit_page, name='edit_page'),
]
