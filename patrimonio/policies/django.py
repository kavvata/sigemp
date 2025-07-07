from typing import override

from django.contrib.auth.models import User

from patrimonio.models import TipoBem
from patrimonio.policies.contracts import (
    EstadoConservacaoPolicy,
    GrauFragilidadePolicy,
    MarcaModeloPolicy,
    TipoBemPolicy,
)


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


class DjangoEstadoConservacaoPolicy(EstadoConservacaoPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:view_estadoconservacao"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:add_estadoconservacao"
        )

    @override
    def pode_editar(self, estado_conservacao) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:change_estadoconservacao")
            and estado_conservacao.removido_em is None
        )

    @override
    def pode_remover(self, estado_conservacao) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:delete_estadoconservacao")
            and estado_conservacao.removido_em is None
        )

    @override
    def pode_visualizar(self, estado_conservacao) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:view_estadoconservacao")
            and estado_conservacao.removido_em is None
        )


class DjangoGrauFragilidadePolicy(GrauFragilidadePolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:view_graufragilidade"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:add_graufragilidade"
        )

    @override
    def pode_editar(self, grau_fragilidade) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:change_graufragilidade")
            and grau_fragilidade.removido_em is None
        )

    @override
    def pode_remover(self, grau_fragilidade) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:delete_graufragilidade")
            and grau_fragilidade.removido_em is None
        )

    @override
    def pode_visualizar(self, grau_fragilidade) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:view_graufragilidade")
            and grau_fragilidade.removido_em is None
        )


class DjangoMarcaModeloPolicy(MarcaModeloPolicy):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    @override
    def pode_listar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:view_marcamodelo"
        )

    @override
    def pode_criar(self) -> bool:
        return self.user.is_superuser or self.user.has_perm(
            "patrimonio:add_marcamodelo"
        )

    @override
    def pode_editar(self, marca_modelo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:change_marcamodelo")
            and marca_modelo.removido_em is None
        )

    @override
    def pode_remover(self, marca_modelo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:delete_marcamodelo")
            and marca_modelo.removido_em is None
        )

    @override
    def pode_visualizar(self, marca_modelo) -> bool:
        return (
            self.user.is_superuser
            or self.user.has_perm("patrimonio:view_marcamodelo")
            and marca_modelo.removido_em is None
        )
