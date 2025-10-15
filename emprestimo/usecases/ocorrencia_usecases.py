from datetime import date
from typing import Optional
from core.types import ResultSuccess, ResultError
from emprestimo.domain.entities import OcorrenciaEntity
from emprestimo.domain.types import OcorrenciaFiltro
from emprestimo.policies.contracts import OcorrenciaPolicy
from emprestimo.repositories.contracts import OcorrenciaRepository


class ListarOcorrenciasUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self, filtro: Optional[OcorrenciaFiltro] = None):
        if not self.policy.pode_listar():
            return ResultError("Sem permissão para listar ocorrências")

        try:
            ocorrencias = (
                self.repo.listar_ocorrencias()
                if not filtro
                else self.repo.listar(**filtro)
            )
            return ResultSuccess(ocorrencias)
        except Exception as e:
            return ResultError(f"Erro ao listar ocorrências: {str(e)}")


class ListarOcorrenciasBemUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self, id: int):
        if not self.policy.pode_listar():
            return ResultError("Sem permissão para listar ocorrências")

        try:
            ocorrencias = self.repo.listar_ocorrencias_do_bem(id)
            return ResultSuccess(ocorrencias)
        except Exception as e:
            return ResultError(f"Erro ao listar ocorrências: {str(e)}")


class ListarOcorrenciasAlunoUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self, id: int):
        if not self.policy.pode_listar():
            return ResultError("Sem permissão para listar ocorrências")

        try:
            ocorrencias = self.repo.listar_ocorrencias_do_aluno(id)
            return ResultSuccess(ocorrencias)
        except Exception as e:
            return ResultError(f"Erro ao listar ocorrências: {str(e)}")


class ListarOcorrenciasEmprestimoUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self, id: int):
        if not self.policy.pode_listar():
            return ResultError("Sem permissão para listar ocorrências")

        try:
            ocorrencias = self.repo.listar_ocorrencias_do_emprestimo(id)
            return ResultSuccess(ocorrencias)
        except Exception as e:
            return ResultError(f"Erro ao listar ocorrências: {str(e)}")


class RegistrarOcorrenciaUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, ocorrencia: OcorrenciaEntity):
        if not self.policy.pode_criar():
            return ResultError("Sem permissão para registrar ocorrências")

        try:
            resultado = self.repo.cadastrar_ocorrencia(ocorrencia, self.policy.user)
            return ResultSuccess(resultado)
        except Exception as e:
            return ResultError(f"Erro ao registrar ocorrência: {str(e)}")


class CancelarOcorrenciaUsecase:
    def __init__(self, repo: OcorrenciaRepository, policy: OcorrenciaPolicy):
        self.repo = repo
        self.policy = policy

    def pode_remover(self, ocorrencia: OcorrenciaEntity):
        return self.policy.pode_remover(ocorrencia)

    def buscar_por_id(self, ocorrencia_id: int) -> OcorrenciaEntity:
        return self.repo.buscar_por_id(ocorrencia_id)

    def execute(self, ocorrencia_id: int, motivo: str):
        ocorrencia = self.repo.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            return ResultError("Ocorrência não encontrada")

        if not self.policy.pode_remover(ocorrencia):
            return ResultError("Sem permissão para cancelar ocorrência")

        if ocorrencia.cancelado_em:
            return ResultError("Ocorrência já está cancelada")

        try:
            ocorrencia.cancelado_em = date.today()
            ocorrencia.cancelado_por_id = self.policy.user.id
            ocorrencia.motivo_cancelamento = motivo

            resultado = self.repo.editar_ocorrencia(ocorrencia, self.policy.user)
            return ResultSuccess(resultado)
        except Exception as e:
            return ResultError(f"Erro ao cancelar ocorrência: {str(e)}")
