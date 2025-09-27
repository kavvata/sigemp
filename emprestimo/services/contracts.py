from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any

from emprestimo.domain.entities import EmprestimoEntity


class PDFService(ABC):
    @abstractmethod
    def gerar_pdf_de_template(self, template_path: str, context: dict) -> BytesIO:
        pass

    @abstractmethod
    def gerar_termo_responsabilidade(
        self, emprestimo: EmprestimoEntity, user: Any
    ) -> BytesIO:
        pass

    @abstractmethod
    def gerar_termo_devolucao(self, emprestimo: EmprestimoEntity, user: Any) -> BytesIO:
        pass
