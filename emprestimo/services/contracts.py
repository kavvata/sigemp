from abc import ABC, abstractmethod
from io import BytesIO


class PDFService(ABC):
    @abstractmethod
    def generate_pdf_from_template(self, template_path: str, context: dict) -> BytesIO:
        pass

    @abstractmethod
    def generate_termo_responsabilidade(self, emprestimo_id: int) -> BytesIO:
        pass

    @abstractmethod
    def generate_termo_devolucao(self, emprestimo_id: int) -> BytesIO:
        pass
