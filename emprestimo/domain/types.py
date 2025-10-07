from enum import IntEnum
from typing import TypedDict


class EmprestimoEstadoEnum(IntEnum):
    ATIVO = 1
    FINALIZADO = 2
    CANCELADO = 3

    @property
    def label(self):
        labels = {
            EmprestimoEstadoEnum.ATIVO: "Ativo",
            EmprestimoEstadoEnum.FINALIZADO: "Finalizado",
            EmprestimoEstadoEnum.CANCELADO: "Cancelado",
        }
        return labels[self]

    @classmethod
    def choices(cls):
        return [(member.value, member.label) for member in cls]

    def __str__(self):
        return self.label


class EmprestimoFiltro(TypedDict, total=False):
    texto: str
    estado: EmprestimoEstadoEnum
    tem_ocorrencia: str
