from abc import ABC, abstractmethod

from typing import Any

from ensino.domain.entities import CampusEntity


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
    def remover_campus(self, campus: CampusEntity, user: Any):
        pass
