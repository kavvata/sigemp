from django.urls import path, include

from . import views

app_name = "core"
urlpatterns = [
    path("login/", views.login_view, name="login"),
]
