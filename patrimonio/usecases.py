from core.types import ResultError, ResultSuccess
from patrimonio.repositories.contracts import TipoBemRepository
from patrimonio.policies.contracts import TipoBemPolicy


class ListarTiposBemUsecase:
    def __init__(self, repo: TipoBemRepository, policy: TipoBemPolicy) -> None:
        self.repo: TipoBemRepository = repo
        self.policy: TipoBemPolicy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.listar_tipos_bem()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar tipos de bem bem: {e}")


class CadastrarTipoBemUsecase:
    def __init__(self, repo: TipoBemRepository, policy: TipoBemPolicy) -> None:
        self.repo: TipoBemRepository = repo
        self.policy: TipoBemPolicy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, descricao: str):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.cadastrar_tipo_bem(descricao, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar tipos de bem bem: {e}")


class EditarTipoBemUsecase:
    def __init__(self, repo: TipoBemRepository, policy: TipoBemPolicy) -> None:
        self.repo: TipoBemRepository = repo
        self.policy: TipoBemPolicy = policy

    def get_tipo_bem(self, id: int):
        try:
            tipo_bem = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")
        else:
            if not self.policy.pode_editar(tipo_bem):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(tipo_bem)

    def execute(self, id: int, descricao: str):
        resposta = self.get_tipo_bem(id)
        if not resposta:
            return resposta

        if not self.policy.pode_editar(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.editar_tipo_bem(id, descricao, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")


class RemoverTipoBemUsecase:
    def __init__(self, repo: TipoBemRepository, policy: TipoBemPolicy) -> None:
        self.repo: TipoBemRepository = repo
        self.policy: TipoBemPolicy = policy

    def get_tipo_bem(self, id: int):
        try:
            tipo_bem = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")
        else:
            if not self.policy.pode_editar(tipo_bem):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(tipo_bem)

    def execute(self, id: int):
        resposta = self.get_tipo_bem(id)

        if not resposta:
            return resposta

        if not self.policy.pode_remover(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.remover_tipo_bem(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover tipo bem: {e}")
