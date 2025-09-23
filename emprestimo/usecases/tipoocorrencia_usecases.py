from core.types import ResultError, ResultSuccess
from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.policies.contracts import TipoOcorrenciaPolicy
from emprestimo.repositories.contracts import TipoOcorrenciaRepository


class ListarTiposOcorrenciaUsecase:
    def __init__(
        self, repo: TipoOcorrenciaRepository, policy: TipoOcorrenciaPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError(
                "Você não tem permissão para listar tipos de ocorrência."
            )

        try:
            resposta = self.repo.listar_tipos_ocorrencia()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar tipos de ocorrência: {e}")


class CadastrarTipoOcorrenciaUsecase:
    def __init__(
        self, repo: TipoOcorrenciaRepository, policy: TipoOcorrenciaPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_tipo_ocorrencia: TipoOcorrenciaEntity):
        if not self.policy.pode_criar():
            return ResultError(
                "Você não tem permissão para cadastrar tipo de ocorrência"
            )

        try:
            resposta = self.repo.cadastrar_tipo_ocorrencia(
                novo_tipo_ocorrencia,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar tipo de ocorrência: {e}")


class EditarTipoOcorrenciaUsecase:
    def __init__(
        self, repo: TipoOcorrenciaRepository, policy: TipoOcorrenciaPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, tipo_ocorrencia):
        return self.policy.pode_editar(tipo_ocorrencia)

    def get_tipo_ocorrencia(self, id: int):
        try:
            tipo_ocorrencia = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar tipo_ocorrencia: {e}")

        if not self.policy.pode_editar(tipo_ocorrencia):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(tipo_ocorrencia)

    def execute(self, tipo_ocorrencia: TipoOcorrenciaEntity):
        if not self.policy.pode_editar(tipo_ocorrencia):
            return ResultError("Você não tem permissão para editar tipo de ocorrência.")

        resultado_busca_por_id = self.get_tipo_ocorrencia(tipo_ocorrencia.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_tipo_ocorrencia(
                tipo_ocorrencia, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo de ocorrência: {e}")


class RemoverTipoOcorrenciaUsecase:
    def __init__(
        self, repo: TipoOcorrenciaRepository, policy: TipoOcorrenciaPolicy
    ) -> None:
        self.repo = repo
        self.policy = policy

    def get_tipo_ocorrencia(self, id: int):
        try:
            tipo_ocorrencia = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar tipo de ocorrência: {e}")

        if not self.policy.pode_remover(tipo_ocorrencia):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(tipo_ocorrencia)

    def execute(self, id):
        resultado = self.get_tipo_ocorrencia(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_tipo_ocorrencia(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover tipo de ocorrência: {e}")
