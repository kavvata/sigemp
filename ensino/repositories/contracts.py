from abc import ABC, abstractmethod

from ensino.domain.entities import CampusEntity


class CampusRepository(ABC):
    @abstractmethod
    def listar_campi(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_campus(self, campus: CampusEntity):
        pass

    @abstractmethod
    def editar_campus(self, campus: CampusEntity):
        pass

    @abstractmethod
    def remover_campus(self, campus: CampusEntity):
        pass
