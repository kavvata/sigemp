from typing import override
from patrimonio.models import TipoBem
from patrimonio.policies.contracts import TipoBemPolicy
from django.contrib.auth.models import User


class DjangoTipoBemPolicy(TipoBemPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("patrimonio:view_tipobem")

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("patrimonio:add_tipobem")

    @override
    def pode_editar(self, tipo_bem: TipoBem) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:change_tipobem")
            and tipo_bem.removido_em is None
        )

    @override
    def pode_remover(self, tipo_bem) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:delete_tipobem")
            and tipo_bem.removido_em is None
        )

    @override
    def pode_visualizar(self, tipo_bem) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:view_tipobem")
            and tipo_bem.removido_em is None
        )
