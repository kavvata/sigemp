from core.types import ResultError, ResultSuccess
from ensino.domain.entities import CampusEntity
from ensino.policies.contracts import CampusPolicy
from ensino.repositories.contracts import CampusRepository


class ListarCampiUsecase:
    def __init__(self, repo: CampusRepository, policy: CampusPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar campi.")

        try:
            resposta = self.repo.listar_campi()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar campi: {e}")


class CadastrarCampusUsecase:
    def __init__(self, repo: CampusRepository, policy: CampusPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_campus: CampusEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para cadastrar campus.")

        try:
            resposta = self.repo.cadastrar_campus(
                novo_campus,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar campus: {e}")


class EditarCampusUsecase:
    def __init__(self, repo: CampusRepository, policy: CampusPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self):
        return self.policy.pode_editar()

    def get_campus(self, id: int):
        try:
            campus = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar campus: {e}")

        if not self.policy.pode_editar(campus):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(campus)

    def execute(self, campus: CampusEntity):
        if not self.policy.pode_editar():
            return ResultError("Você não tem permissão para editar campus.")

        resultado_busca_por_id = self.get_campus(campus.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_campus(campus, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar campus: {e}")


