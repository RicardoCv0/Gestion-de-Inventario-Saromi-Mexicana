from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("create/", views.create_gemstone, name="create"),
    
    path("details/<slug:gemstone_id>/", views.gemstone_details, name="details"),
    path("edit/<slug:gemstone_id>/", views.edit_gemstone, name="edit"),
    path("delete/<slug:gemstone_id>/", views.delete_gemstone, name="delete"),
]