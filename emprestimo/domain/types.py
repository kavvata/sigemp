from enum import IntEnum


class EmprestimoEstadoEnum(IntEnum):
    ATIVO = (1, "Ativo")
    FINALIZADO = (2, "Finalizado")
    CANCELADO = (3, "Cancelado")

    def __new__(cls, value, label):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def choices(cls):
        return [(member.value, member.label) for member in cls]
