from core.types import ResultError, ResultSuccess
from ensino.domain.entities import AlunoEntity
from ensino.policies.contracts import AlunoPolicy
from ensino.repositories.contracts import AlunoRepository


class ListarAlunosUsecase:
    def __init__(self, repo: AlunoRepository, policy: AlunoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar alunos.")

        try:
            resposta = self.repo.listar_alunos()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar alunos: {e}")


class CadastrarAlunoUsecase:
    def __init__(self, repo: AlunoRepository, policy: AlunoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_aluno: AlunoEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para cadastrar aluno.")

        try:
            resposta = self.repo.cadastrar_aluno(
                novo_aluno,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar aluno: {e}")


class EditarAlunoUsecase:
    def __init__(self, repo: AlunoRepository, policy: AlunoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, aluno):
        return self.policy.pode_editar(aluno)

    def get_aluno(self, id: int):
        try:
            aluno = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar aluno: {e}")

        if not self.policy.pode_editar(aluno):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(aluno)

    def execute(self, aluno: AlunoEntity):
        if not self.policy.pode_editar(aluno):
            return ResultError("Você não tem permissão para editar aluno.")

        resultado_busca_por_id = self.get_aluno(aluno.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_aluno(aluno, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar aluno: {e}")


class RemoverAlunoUsecase:
    def __init__(self, repo: AlunoRepository, policy: AlunoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def get_aluno(self, id: int):
        try:
            aluno = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar aluno: {e}")

        if not self.policy.pode_remover(aluno):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(aluno)

    def execute(self, id):
        resultado = self.get_aluno(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_aluno(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover aluno: {e}")
