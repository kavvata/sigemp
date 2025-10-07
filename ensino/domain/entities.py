from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class CampusEntity(TimeStampableEntity):
    sigla: str
    nome: str
    id: int = None


@dataclass(kw_only=True)
class CursoEntity(TimeStampableEntity):
    sigla: str
    nome: str
    campus_id: int
    id: int = None
    campus_sigla: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.nome} ({self.campus_sigla})"


@dataclass(kw_only=True)
class FormaSelecaoEntity(TimeStampableEntity):
    descricao: str
    periodo_inicio: datetime
    periodo_fim: datetime
    id: Optional[int] = None


@dataclass(kw_only=True)
class AlunoEntity(TimeStampableEntity):
    nome: str
    nome_responsavel: Optional[str] = None
    cpf: str
    email: str
    matricula: str
    telefone: str
    forma_selecao_id: int
    curso_id: int
    curso_nome: Optional[str]
    campus_sigla: Optional[str]
    forma_selecao_descricao: Optional[str]
    id: Optional[int] = None

    def to_dict(self, exclude: list[str] = None):
        if exclude is not None:
            exclude.append("curso_nome")
            exclude.append("campus_sigla")
            exclude.append("forma_selecao_descricao")
        else:
            exclude = ["curso_nome", "forma_selecao_descricao", "campus_sigla"]

        return super().to_dict(exclude)
