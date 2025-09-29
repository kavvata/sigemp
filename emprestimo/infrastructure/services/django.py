from django.contrib.auth.models import User
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.infrastructure.services.contracts import PDFService

from django.utils import timezone
from django.template.loader import render_to_string
from django_weasyprint import WeasyTemplateResponse
from io import BytesIO


class DjangoWeasyPDFService(PDFService):
    def __init__(self, request) -> None:
        self._request = request

    def gerar_pdf_de_template(self, template_path: str, context: dict) -> BytesIO:
        html_string = render_to_string(template_path, context)

        response = WeasyTemplateResponse(
            request=self._request,
            template=template_path,
            context=context,
            content_type="application/pdf",
        )

        return response

    def gerar_termo_responsabilidade(
        self, emprestimo: EmprestimoEntity, user: User
    ) -> BytesIO:
        from emprestimo.models import Emprestimo

        model = Emprestimo.objects.get(id=emprestimo.id)

        context = {
            "emprestimo": model,
            "data_geracao": timezone.now().strftime("%d/%m/%Y às %H:%M"),
        }

        return self.gerar_pdf_de_template(
            "emprestimo/emprestimo/termo_responsabilidade.html", context
        )

    def gerar_termo_devolucao(
        self, emprestimo: EmprestimoEntity, user: User
    ) -> BytesIO:
        from emprestimo.models import Emprestimo

        model = Emprestimo.objects.get(id=emprestimo.id)

        context = {
            "emprestimo": model,
            "data_geracao": timezone.now().strftime("%d/%m/%Y às %H:%M"),
        }

        return self.gerar_pdf_de_template(
            "emprestimo/emprestimo/termo_devolucao.html", context
        )
