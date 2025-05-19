from django.contrib import messages
from django.contrib.auth import login
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse

from core.presentation.forms import LoginForm
from core.repositories.django import DjUserRepository
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
                messages.error(request, result.mensagem)
                return redirect(reverse("core:login"))

            user: User = result.value
            login(request, user)
            return redirect(reverse("core:home"))

    return render(request, "registration/login.html", {"form": LoginForm})
