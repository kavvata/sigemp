from abc import ABC, abstractmethod


class CampusPolicy(ABC):
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
    def pode_editar(self, campus) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, campus) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, campus) -> bool:
        pass


class CursoPolicy(ABC):
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
    def pode_editar(self, curso) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, curso) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, curso) -> bool:
        pass


class FormaSelecaoPolicy(ABC):
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
    def pode_editar(self, forma_selecao) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, forma_selecao) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, forma_selecao) -> bool:
        pass


class AlunoPolicy(ABC):
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
    def pode_editar(self, aluno) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, aluno) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, aluno) -> bool:
        pass
