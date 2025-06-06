from typing import override
from patrimonio.policies.contracts import TipoBemPolicy
from django.contrib.auth.models import User


class DjangoTipoBemPolicy(TipoBemPolicy):
    def __init__(self, user: User) -> None:
        super().__init__()
        self.user = user

    @override
    def pode_listar(self) -> bool:
        return True

    @override
    def pode_criar(self) -> bool:
        return True

    @override
    def pode_editar(self, tipo_bem) -> bool:
        return True

    @override
    def pode_remover(self, tipo_bem) -> bool:
        return True

    @override
    def pode_visualizar(self, tipo_bem) -> bool:
        return True
