from abc import ABC, abstractmethod
from typing import Optional, Sequence


class MailService(ABC):
    @abstractmethod
    def enviar_email(
        self,
        mensagem: str,
        destinatarios: Sequence[str],
        assunto: str = "SIGEMP - Aviso",
        mensagem_html: Optional[str] = None,
    ) -> Sequence[str]:
        pass
