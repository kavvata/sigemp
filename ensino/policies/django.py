from typing import override
from django.contrib.auth.models import User
from ensino.policies.contracts import CampusPolicy


class DjangoCampusPolicy(CampusPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("ensino:view_campus")

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("ensino:add_campus")

    @override
    def pode_editar(self, campus) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("ensino:change_campus")
            and campus.removido_em is None
        )

    @override
    def pode_remover(self, campus) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("ensino:delete_campus")
            and campus.removido_em is None
        )

    @override
    def pode_visualizar(self, campus) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("ensino:view_campus")
            and campus.removido_em is None
        )
