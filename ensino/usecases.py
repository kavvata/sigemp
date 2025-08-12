from core.types import ResultError, ResultSuccess
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
