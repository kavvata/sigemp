from abc import ABC, abstractmethod

from typing import Any, Unpack

from ensino.domain.entities import (
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
    AlunoEntity,
)
from ensino.repositories.filters import AlunoFiltro


class CampusRepository(ABC):
    @abstractmethod
    def listar_campi(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_campus(self, campus: CampusEntity, user: Any):
        pass

    @abstractmethod
    def editar_campus(self, campus: CampusEntity, user: Any):
        pass

    @abstractmethod
    def remover_campus(self, id: int, user: Any):
        pass


class CursoRepository(ABC):
    @abstractmethod
    def listar_cursos(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_curso(self, curso: CursoEntity, user: Any):
        pass

    @abstractmethod
    def editar_curso(self, curso: CursoEntity, user: Any):
        pass

    @abstractmethod
    def remover_curso(self, id: int, user: Any):
        pass


class FormaSelecaoRepository(ABC):
    @abstractmethod
    def listar_formas_selecao(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_forma_selecao(self, forma_selecao: FormaSelecaoEntity, user: Any):
        pass

    @abstractmethod
    def editar_forma_selecao(self, forma_selecao: FormaSelecaoEntity, user: Any):
        pass

    @abstractmethod
    def remover_forma_selecao(self, id: int, user: Any):
        pass


class AlunoRepository(ABC):
    @abstractmethod
    def listar_alunos(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def buscar(self, **filtros: Unpack[AlunoFiltro]):
        pass

    @abstractmethod
    def cadastrar_aluno(self, aluno: AlunoEntity, user: Any):
        pass

    @abstractmethod
    def editar_aluno(self, aluno: AlunoEntity, user: Any):
        pass

    @abstractmethod
    def remover_aluno(self, id: int, user: Any):
        pass
