from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.infrastructure.services.contracts import PDFService

from django.utils import timezone
from django.template.loader import render_to_string
from django_weasyprint import WeasyTemplateResponse
from io import BytesIO


class DjangoWeasyPDFService(PDFService):
    def gerar_pdf_de_template(self, template_path: str, context: dict) -> BytesIO:
        html_string = render_to_string(template_path, context)

        response = WeasyTemplateResponse(
            request=None,
            template=template_path,
            context=context,
            content_type="application/pdf",
        )

        pdf_buffer = BytesIO()
        response.render_to_response(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer

    def gerar_termo_responsabilidade(self, emprestimo: EmprestimoEntity) -> BytesIO:
        from emprestimo.models import Emprestimo

        model = Emprestimo.objects.get(id=emprestimo.id)

        context = {
            "emprestimo": model,
            "data_geracao": timezone.now().strftime("%d/%m/%Y às %H:%M"),
        }

        return self.generate_pdf_from_template(
            "emprestimo/emprestimo/termo_responsabilidade.html", context
        )

    def gerar_termo_devolucao(self, emprestimo: EmprestimoEntity) -> BytesIO:
        from emprestimo.models import Emprestimo

        model = Emprestimo.objects.get(id=emprestimo.id)

        context = {
            "emprestimo": model,
            "data_geracao": timezone.now().strftime("%d/%m/%Y às %H:%M"),
        }

        return self.generate_pdf_from_template(
            "emprestimo/emprestimo/termo_devolucao.html", context
        )
