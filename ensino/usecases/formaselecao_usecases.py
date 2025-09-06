from core.types import ResultError, ResultSuccess
from ensino.domain.entities import FormaSelecaoEntity
from ensino.policies.contracts import FormaSelecaoPolicy
from ensino.repositories.contracts import (
    FormaSelecaoRepository,
)


class ListarFormasSelecaoUsecase:
    def __init__(
        self, repo: FormaSelecaoRepository, policy: FormaSelecaoPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar formas de seleção.")

        try:
            resposta = self.repo.listar_formas_selecao()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar formas de seleção: {e}")


class CadastrarFormaSelecaoUsecase:
    def __init__(
        self, repo: FormaSelecaoRepository, policy: FormaSelecaoPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_forma_selecao: FormaSelecaoEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para cadastrar forma de seleção")

        try:
            resposta = self.repo.cadastrar_forma_selecao(
                novo_forma_selecao,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar forma de seleção: {e}")


class EditarFormaSelecaoUsecase:
    def __init__(
        self, repo: FormaSelecaoRepository, policy: FormaSelecaoPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, forma_selecao):
        return self.policy.pode_editar(forma_selecao)

    def get_forma_selecao(self, id: int):
        try:
            forma_selecao = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar forma_selecao: {e}")

        if not self.policy.pode_editar(forma_selecao):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(forma_selecao)

    def execute(self, forma_selecao: FormaSelecaoEntity):
        if not self.policy.pode_editar(forma_selecao):
            return ResultError("Você não tem permissão para editar forma de seleção.")

        resultado_busca_por_id = self.get_forma_selecao(forma_selecao.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_forma_selecao(forma_selecao, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar forma de seleção: {e}")


class RemoverFormaSelecaoUsecase:
    def __init__(
        self, repo: FormaSelecaoRepository, policy: FormaSelecaoPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def get_forma_selecao(self, id: int):
        try:
            forma_selecao = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar forma de seleção: {e}")

        if not self.policy.pode_remover(forma_selecao):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(forma_selecao)

    def execute(self, id):
        resultado = self.get_forma_selecao(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_forma_selecao(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover forma de seleção: {e}")
