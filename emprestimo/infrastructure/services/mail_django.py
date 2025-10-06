from typing import Optional, Sequence
from django.core.mail import send_mail
from emprestimo.domain.contracts.mail import MailService
from sigemp import settings


class DjangoMailService(MailService):
    def enviar_email(
        self,
        mensagem: str,
        destinatarios: Sequence[str],
        assunto: str = "SIGEMP - Aviso",
        mensagem_html: Optional[str] = None,
    ) -> Sequence[str]:
        email_de = settings.DEFAULT_FROM_EMAIL
        email_para = (
            [settings.EMAIL_RECIPIENT_DEBUG] if settings.DEBUG else destinatarios
        )
        return send_mail(
            assunto,
            mensagem,
            email_de,
            recipient_list=email_para,
        )
