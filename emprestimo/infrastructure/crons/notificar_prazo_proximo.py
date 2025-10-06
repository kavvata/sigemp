from datetime import timedelta
from django.utils import timezone
from emprestimo.infrastructure.services.mail_django import DjangoMailService
from emprestimo.repositories.django import DjangoEmprestimoRepository
from emprestimo.usecases.emprestimo_usecases import NotificarDevolucaoUsecase
from ensino.repositories.django import DjangoAlunoRepository


def cron_notificar_prazo_proximo():
    repo = DjangoEmprestimoRepository()
    aluno_repo = DjangoAlunoRepository()
    service = DjangoMailService()

    usecase = NotificarDevolucaoUsecase(
        repo,
        aluno_repo,
        service,
    )

    resultado = usecase.execute(
        timezone.now() + timedelta(days=7),
    )

    if not resultado:
        print(f"[CRON] Erro ao notificar prazos: {resultado.mensagem}")
    else:
        print(f"[CRON] Notificações de devolução enviadas: {resultado.value}")
