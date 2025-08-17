from django import forms

from ensino.models import Campus, Curso


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["nome", "sigla"]


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "sigla", "campus"]
