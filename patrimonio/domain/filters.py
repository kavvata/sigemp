from typing import TypedDict


class BemFiltro(TypedDict, total=False):
    texto: str
    tipo: int
    estado_conservacao: int
    eh_disponivel: bool
