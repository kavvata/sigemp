from typing import TypedDict


class BemFiltro(TypedDict, total=False):
    texto: str
    tipo: str
    eh_disponivel: bool
