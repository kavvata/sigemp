from core.types import ResultError, ResultSuccess
from patrimonio.domain.entities import BemEntity
from patrimonio.policies.contracts import (
    BemPolicy,
    EstadoConservacaoPolicy,
    GrauFragilidadePolicy,
    MarcaModeloPolicy,
    TipoBemPolicy,
)
from patrimonio.repositories.contracts import (
    BemRepository,
    EstadoConservacaoRepository,
    GrauFragilidadeRepository,
    MarcaModeloRepository,
    TipoBemRepository,
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
            return ResultError(f"Erro ao listar tipos de bem: {e}")


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
            return ResultError(f"Erro ao cadastrar tipo de bem : {e}")


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
            return ResultError(f"Erro ao listar estados de conservação: {e}")


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
            return ResultError(f"Erro ao cadastrar estado de conservação: {e}")


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
            return ResultError(f"Erro ao listar graus de fragilidade: {e}")


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


class ListarMarcaModeloUsecase:
    def __init__(self, repo: MarcaModeloRepository, policy: MarcaModeloPolicy) -> None:
        self.repo: MarcaModeloRepository = repo
        self.policy: MarcaModeloPolicy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.listar_marca_modelo()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar marca/modelos: {e}")


class CadastrarMarcaModeloUsecase:
    def __init__(self, repo: MarcaModeloRepository, policy: MarcaModeloPolicy) -> None:
        self.repo: MarcaModeloRepository = repo
        self.policy: MarcaModeloPolicy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, marca: str, modelo: str):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.cadastrar_marca_modelo(marca, modelo, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar marca/modelo: {e}")


class EditarMarcaModeloUsecase:
    def __init__(self, repo: MarcaModeloRepository, policy: MarcaModeloPolicy) -> None:
        self.repo: MarcaModeloRepository = repo
        self.policy: MarcaModeloPolicy = policy

    def pode_editar(self, marca_modelo):
        return self.policy.pode_editar(marca_modelo)

    def get_marca_modelo(self, id: int):
        try:
            marca_modelo = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao editar marca/modelo: {e}")
        else:
            if not self.policy.pode_editar(marca_modelo):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(marca_modelo)

    def execute(self, id: int, marca: str, modelo: int):
        resposta = self.get_marca_modelo(id)
        if not resposta:
            return resposta

        if not self.policy.pode_editar(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.editar_marca_modelo(
                id, marca, modelo, self.policy.user
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar marca/modelo: {e}")


class RemoverMarcaModeloUsecase:
    def __init__(self, repo: MarcaModeloRepository, policy: MarcaModeloPolicy) -> None:
        self.repo: MarcaModeloRepository = repo
        self.policy: MarcaModeloPolicy = policy

    def get_marca_modelo(self, id: int):
        try:
            marca_modelo = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao remover marca/modelo: {e}")
        else:
            if not self.policy.pode_remover(marca_modelo):
                return ResultError("Você não tem permissão para realizar esta ação.")

            return ResultSuccess(marca_modelo)

    def execute(self, id: int):
        resposta = self.get_marca_modelo(id)

        if not resposta:
            return resposta

        if not self.policy.pode_remover(resposta.value):
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.remover_marca_modelo(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover marca/modelo: {e}")


class ListarBensUsecase:
    def __init__(self, repo: BemRepository, policy: BemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            resposta = self.repo.listar_bens()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar bens: {e}")


class CadastrarBemUsecase:
    def __init__(self, repo: BemRepository, policy: BemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_bem: BemEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para realizar esta ação.")

        try:
            bem_existente = self.repo.buscar_por_patrimonio(novo_bem.patrimonio)
            if bem_existente:
                return ResultError("Já existe um bem com esse número de patrimônio.")
        except Exception:
            pass

        try:
            resposta = self.repo.cadastrar_bem(
                novo_bem,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar bem: {e}")


class EditarBemUsecase:
    def __init__(self, repo: BemRepository, policy: BemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, bem):
        return self.policy.pode_editar(bem)

    def get_bem(self, id):
        try:
            bem = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar bem: {e}")

        if not self.policy.pode_editar(bem):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(bem)

    def execute(self, bem: BemEntity):
        resultado = self.get_bem(bem.id)
        if not resultado:
            return resultado

        try:
            bem_com_mesmo_patrimonio = self.repo.buscar_por_patrimonio(bem.patrimonio)
            if bem_com_mesmo_patrimonio and bem_com_mesmo_patrimonio.id != bem.id:
                return ResultError("Já existe outro bem com esse patrimônio.")
        except Exception:
            pass

        try:
            resposta = self.repo.editar_bem(
                bem,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar bem: {e}")


class RemoverBemUsecase:
    def __init__(self, repo: BemRepository, policy: BemPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def get_bem(self, id):
        try:
            bem = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar bem: {e}")

        if not self.policy.pode_remover(bem):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(bem)

    def execute(self, id):
        resultado = self.get_bem(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_bem(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover bem: {e}")
