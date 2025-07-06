from core.types import ResultError, ResultSuccess
from patrimonio.repositories.contracts import (
    TipoBemRepository,
    EstadoConservacaoRepository,
    GrauFragilidadeRepository,
)
from patrimonio.policies.contracts import (
    TipoBemPolicy,
    EstadoConservacaoPolicy,
    GrauFragilidadePolicy,
)


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

    def pode_editar(self, tipo_bem):
        return self.policy.pode_editar(tipo_bem)

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


class ListarEstadosConservacaoUsecase:
    def __init__(
        self, repo: EstadoConservacaoRepository, policy: EstadoConservacaoPolicy
    ) -> None:
        self.repo: EstadoConservacaoRepository = repo
        self.policy: EstadoConservacaoPolicy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.listar_estados_conservacao()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar tipos de bem bem: {e}")


class CadastrarEstadoConservacaoUsecase:
    def __init__(
        self, repo: EstadoConservacaoRepository, policy: EstadoConservacaoPolicy
    ) -> None:
        self.repo: EstadoConservacaoRepository = repo
        self.policy: EstadoConservacaoPolicy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, descricao: str, nivel: int):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.cadastrar_estado_conservacao(
                descricao, nivel, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar tipos de bem bem: {e}")


class EditarEstadoConservacaoUsecase:
    def __init__(
        self, repo: EstadoConservacaoRepository, policy: EstadoConservacaoPolicy
    ) -> None:
        self.repo: EstadoConservacaoRepository = repo
        self.policy: EstadoConservacaoPolicy = policy

    def pode_editar(self, estado_conservacao):
        return self.policy.pode_editar(estado_conservacao)

    def get_estado_conservacao(self, id: int):
        try:
            estado_conservacao = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")
        else:
            if not self.policy.pode_editar(estado_conservacao):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(estado_conservacao)

    def execute(self, id: int, descricao: str, nivel: int):
        resposta = self.get_estado_conservacao(id)
        if not resposta:
            return resposta

        if not self.policy.pode_editar(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.editar_estado_conservacao(
                id, descricao, nivel, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar tipo bem: {e}")


class RemoverEstadoConservacaoUsecase:
    def __init__(
        self, repo: EstadoConservacaoRepository, policy: EstadoConservacaoPolicy
    ) -> None:
        self.repo: EstadoConservacaoRepository = repo
        self.policy: EstadoConservacaoPolicy = policy

    def get_estado_conservacao(self, id: int):
        try:
            estado_conservacao = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao remover estado de conservacao: {e}")
        else:
            if not self.policy.pode_remover(estado_conservacao):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(estado_conservacao)

    def execute(self, id: int):
        resposta = self.get_estado_conservacao(id)

        if not resposta:
            return resposta

        if not self.policy.pode_remover(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.remover_estado_conservacao(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover estado de conservacao: {e}")


class ListarGrauFragilidadeUsecase:
    def __init__(
        self, repo: GrauFragilidadeRepository, policy: GrauFragilidadePolicy
    ) -> None:
        self.repo: GrauFragilidadeRepository = repo
        self.policy: GrauFragilidadePolicy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.listar_grau_fragilidade()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar grais de fragilidade: {e}")


class CadastrarGrauFragilidadeUsecase:
    def __init__(
        self, repo: GrauFragilidadeRepository, policy: GrauFragilidadePolicy
    ) -> None:
        self.repo: GrauFragilidadeRepository = repo
        self.policy: GrauFragilidadePolicy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, descricao: str, nivel: int):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.cadastrar_grau_fragilidade(
                descricao, nivel, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar grau de fragilidade: {e}")


class EditarGrauFragilidadeUsecase:
    def __init__(
        self, repo: GrauFragilidadeRepository, policy: GrauFragilidadePolicy
    ) -> None:
        self.repo: GrauFragilidadeRepository = repo
        self.policy: GrauFragilidadePolicy = policy

    def pode_editar(self, grau_fragilidade):
        return self.policy.pode_editar(grau_fragilidade)

    def get_grau_fragilidade(self, id: int):
        try:
            grau_fragilidade = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar grau de fragilidade: {e}")
        else:
            if not self.policy.pode_editar(grau_fragilidade):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(grau_fragilidade)

    def execute(self, id: int, descricao: str, nivel: int):
        resposta = self.get_grau_fragilidade(id)
        if not resposta:
            return resposta

        if not self.policy.pode_editar(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.editar_grau_fragilidade(
                id, descricao, nivel, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar grau de fragilidade: {e}")


class RemoverGrauFragilidadeUsecase:
    def __init__(
        self, repo: GrauFragilidadeRepository, policy: GrauFragilidadePolicy
    ) -> None:
        self.repo: GrauFragilidadeRepository = repo
        self.policy: GrauFragilidadePolicy = policy

    def get_grau_fragilidade(self, id: int):
        try:
            grau_fragilidade = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao remover grau de fragilidade: {e}")
        else:
            if not self.policy.pode_remover(grau_fragilidade):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(grau_fragilidade)

    def execute(self, id: int):
        resposta = self.get_grau_fragilidade(id)

        if not resposta:
            return resposta

        if not self.policy.pode_remover(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.remover_grau_fragilidade(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover grau de fragilidade: {e}")
