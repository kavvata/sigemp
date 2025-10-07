from typing import TypedDict


class AlunoFiltro(TypedDict, total=False):
    id: int
    nome: str
    nome_responsavel: str
    cpf: str
    email: str
    matricula: str
    telefone: str
    forma_selecao_id: int
    curso: int
    campus: int
