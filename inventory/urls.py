from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("create/", views.create_gemstone, name="create"),
    
    path("details/<slug:gemstone_id>/", views.gemstone_details, name="details"),
    path("edit/<slug:gemstone_id>/", views.edit_gemstone, name="edit"),
    path("delete/<slug:gemstone_id>/", views.delete_gemstone, name="delete"),

    path("entry/<slug:gemstone_id>/", views.entry_movement, name="entry"),
    path("adjustment/<slug:gemstone_id>/", views.adjustment_movement, name="adjustment"),
    path("exit/<slug:gemstone_id>/", views.exit_movement, name="exit"),
]