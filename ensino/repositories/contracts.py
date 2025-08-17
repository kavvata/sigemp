from abc import ABC, abstractmethod

from typing import Any

from ensino.domain.entities import CampusEntity, CursoEntity


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
