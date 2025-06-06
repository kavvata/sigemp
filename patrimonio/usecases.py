from core.types import ResultError, ResultSuccess
from patrimonio.repositories.contracts import TipoBemRepository
from patrimonio.policies.contracts import TipoBemPolicy


class ListarTiposBemUsecase:
    def __init__(self, repo: TipoBemPolicy, policy: TipoBemPolicy) -> None:
        self.repo = repo
        self.policy = policy

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
    def __init__(self, repo: TipoBemPolicy, policy: TipoBemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, descricao: str):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.cadastrar_tipo_bem(descricao)
            return ResultSuccess(resposta)
        except:
            return ResultError("Erro ao cadastrar tipo bem: ??")


class EditarTipoBemUsecase:
    def __init__(self, repo: TipoBemPolicy, policy: TipoBemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def get_tipo_bem(self, id: int):
        if not self.policy.pode_editar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            tipo_bem = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")
        else:
            return ResultSuccess(tipo_bem)

    def execute(self, id: int, descricao: str):
        if not self.policy.pode_editar():
            return ResultError("Você não tem permissão para realizar esta ação.")
        try:
            resposta = self.repo.editar_tipo_bem(id, descricao)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")


class RemoverTipoBemUsecase:
    def __init__(self, repo: TipoBemPolicy, policy: TipoBemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def execute(self, id: int):
        if not self.policy.pode_remover():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.remover_tipo_bem(id)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover tipo bem: {e}")
