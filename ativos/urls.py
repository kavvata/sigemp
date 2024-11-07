from django.urls import path

from . import views

app_name = "ativos"
urlpatterns = [
    path("", views.fetch, name="index"),
    path("inventory/", views.InventoryView.as_view(), name="inventory"),
]
