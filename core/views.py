from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from core.forms import LoginForm
from core.usecases import login_usecase


# Create your views here.
def login_view(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            repo = DjUserRepository()
            result = login_usecase(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
                repo,
            )

            if not result:
                messages.error(request, "Usuario ou senha incorretos.")
                return redirect("login")

            user: User = result.data
            login(request, user)
            return redirect("home")

    return render(request, "registration/login.html", {"form": LoginForm})
