from abc import ABC, abstractmethod


class TipoBemPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, tipo_bem) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, tipo_bem) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, tipo_bem) -> bool:
        pass


class EstadoConservacaoPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, estado_conservacao) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, estado_conservacao) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, estado_conservacao) -> bool:
        pass


class GrauFragilidadePolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, grau_fragilidade) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, grau_fragilidade) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, grau_fragilidade) -> bool:
        pass


class MarcaModeloPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, marca_modelo) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, marca_modelo) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, marca_modelo) -> bool:
        pass
