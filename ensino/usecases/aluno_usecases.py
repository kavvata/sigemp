from typing import Optional
from core.types import ResultError, ResultSuccess
from ensino.domain.entities import AlunoEntity
from ensino.policies.contracts import AlunoPolicy
from ensino.repositories.contracts import AlunoRepository
from ensino.repositories.filters import AlunoFiltro


class ListarAlunosUsecase:
    def __init__(self, repo: AlunoRepository, policy: AlunoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self, filtro: Optional[AlunoFiltro] = None):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar alunos.")

        try:
            resposta = (
                self.repo.listar_alunos() if not filtro else self.repo.listar(**filtro)
            )
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

        existente = self.repo.buscar(matricula=novo_aluno.matricula)
        if existente:
            return ResultError(f"Matricula {novo_aluno.matricula} já cadastrada.")

        existente = self.repo.buscar(cpf=novo_aluno.cpf)
        if existente:
            return ResultError(f"CPF {novo_aluno.cpf} já cadastrado.")

        existente = self.repo.buscar(email=novo_aluno.email)
        if existente:
            return ResultError(f"Email {novo_aluno.email} já cadastrado.")

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
            aluno = self.repo.buscar(id=id)
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

        encontrados = self.repo.buscar(matricula=aluno.matricula)
        if encontrados and aluno.id not in [aluno.id for aluno in encontrados]:
            return ResultError(f"Matricula {aluno.matricula} já cadastrada.")

        encontrados = self.repo.buscar(cpf=aluno.cpf)
        if encontrados and aluno.id not in [aluno.id for aluno in encontrados]:
            return ResultError(f"CPF {aluno.cpf} já cadastrado.")

        encontrados = self.repo.buscar(email=aluno.email)
        if encontrados and aluno.id not in [aluno.id for aluno in encontrados]:
            return ResultError(f"Email {aluno.email} já cadastrado.")

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
