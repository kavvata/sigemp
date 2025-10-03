from typing import override
from django.contrib.auth.models import User

from emprestimo.policies.contracts import (
    EmprestimoPolicy,
    OcorrenciaPolicy,
    TipoOcorrenciaPolicy,
)


class DjangoTipoOcorrenciaPolicy(TipoOcorrenciaPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "emprestimo:view_tipoocorrencia"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "emprestimo:add_tipoocorrencia"
        )

    @override
    def pode_editar(self, tipoocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:change_tipoocorrencia")
            and tipoocorrencia.removido_em is None
        )

    @override
    def pode_remover(self, tipoocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:delete_tipoocorrencia")
            and tipoocorrencia.removido_em is None
        )

    @override
    def pode_visualizar(self, tipoocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:view_tipoocorrencia")
            and tipoocorrencia.removido_em is None
        )


class DjangoEmprestimoPolicy(EmprestimoPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "emprestimo:view_emprestimo"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("emprestimo:add_emprestimo")

    @override
    def pode_editar(self, emprestimo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:change_emprestimo")
            and emprestimo.removido_em is None
        )

    @override
    def pode_remover(self, emprestimo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:delete_emprestimo")
            and emprestimo.removido_em is None
        )

    @override
    def pode_visualizar(self, emprestimo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:view_emprestimo")
            and emprestimo.removido_em is None
        )

    def pode_gerar_termos(self, emprestimo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:change_emprestimo")
            and emprestimo.removido_em is None
        )


class DjangoOcorrenciaPolicy(OcorrenciaPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "emprestimo:view_ocorrencia"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm("emprestimo:add_ocorrencia")

    @override
    def pode_editar(self, ocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:change_ocorrencia")
            and ocorrencia.removido_em is None
        )

    @override
    def pode_remover(self, ocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:delete_ocorrencia")
            and ocorrencia.removido_em is None
        )

    @override
    def pode_visualizar(self, ocorrencia) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("emprestimo:view_ocorrencia")
            and ocorrencia.removido_em is None
        )
