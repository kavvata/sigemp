from core.types import ResultError, ResultSuccess
from patrimonio.repositories.contracts import TipoBemRepository


def listar_tipos_bem_usecase(repo: TipoBemRepository):
    try:
        resposta = repo.listar_tipos_bem()
        return ResultSuccess(resposta)
    except:
        return ResultError("Erro ao listar tipos bem: ??")


def cadastrar_tipo_bem_usecase(descricao: str, repo: TipoBemRepository):
    try:
        resposta = repo.cadastrar_tipo_bem(descricao)
        return ResultSuccess(resposta)
    except:
        return ResultError("Erro ao cadastrar tipo bem: ??")


def editar_tipo_bem_usecase(id: int, descricao: str, repo: TipoBemRepository):
    try:
        resposta = repo.editar_tipo_bem(id, descricao)
        return ResultSuccess(resposta)
    except:
        return ResultError("Erro ao editar tipo bem: ??")


def remover_tipo_bem_usecase(id: int, repo: TipoBemRepository):
    try:
        resposta = repo.remover_tipo_bem(id)
        return ResultSuccess(resposta)
    except:
        return ResultError("Erro ao remover tipo bem: ??")
