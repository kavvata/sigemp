from core.types import ResultError, ResultSuccess
from ensino.domain.entities import CursoEntity
from ensino.policies.contracts import CursoPolicy
from ensino.repositories.contracts import (
    CursoRepository,
)


class ListarCursosUsecase:
    def __init__(self, repo: CursoRepository, policy: CursoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar cursos.")

        try:
            resposta = self.repo.listar_cursos()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar cursos: {e}")


class CadastrarCursoUsecase:
    def __init__(self, repo: CursoRepository, policy: CursoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_curso: CursoEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para cadastrar curso.")

        try:
            resposta = self.repo.cadastrar_curso(
                novo_curso,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar curso: {e}")


class EditarCursoUsecase:
    def __init__(self, repo: CursoRepository, policy: CursoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, curso):
        return self.policy.pode_editar(curso)

    def get_curso(self, id: int):
        try:
            curso = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar curso: {e}")

        if not self.policy.pode_editar(curso):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(curso)

    def execute(self, curso: CursoEntity):
        if not self.policy.pode_editar(curso):
            return ResultError("Você não tem permissão para editar curso.")

        resultado_busca_por_id = self.get_curso(curso.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_curso(curso, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar curso: {e}")


class RemoverCursoUsecase:
    def __init__(self, repo: CursoRepository, policy: CursoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def get_curso(self, id: int):
        try:
            curso = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar curso: {e}")

        if not self.policy.pode_remover(curso):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(curso)

    def execute(self, id):
        resultado = self.get_curso(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_curso(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover curso: {e}")
