from enum import IntEnum


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
