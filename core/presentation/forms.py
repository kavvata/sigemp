from django.forms import CharField, Form, PasswordInput


class LoginForm(Form):
    username = CharField(label="Usuário", max_length=100, required=True)
    password = CharField(
        label="Senha", max_length=100, widget=PasswordInput, required=True
    )
