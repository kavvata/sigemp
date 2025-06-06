from django import forms


class TipoBemForm(forms.Form):
    descricao = forms.CharField(max_length=255)
