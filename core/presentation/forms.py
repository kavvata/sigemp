from django.forms import CharField, Form, PasswordInput


class LoginForm(Form):
    username = CharField(label="usuario", max_length=100, required=True)
    password = CharField(
        label="senha", max_length=100, widget=PasswordInput, required=True
    )
