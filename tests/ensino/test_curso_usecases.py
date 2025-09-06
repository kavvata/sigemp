from unittest import mock

import pytest

from core.types import ResultError, ResultSuccess
from ensino.domain.entities import CursoEntity
from ensino.usecases import (
    CadastrarCursoUsecase,
    EditarCursoUsecase,
    ListarCursosUsecase,
    RemoverCursoUsecase,
)


@pytest.fixture
def curso():
    return CursoEntity(
        sigla="TADS",
        nome="Técnologo em Análise e Desenvolvimento de Sistemas",
        campus_id=1,
    )


@pytest.fixture
def lista_cursos():
    return [
        CursoEntity(
            sigla="TMI",
            nome="Tecnologia em Manutenção Industrial",
            campus_id=1,
        ),
        CursoEntity(
            sigla="LFIS",
            nome="Licenciatura em Física",
            campus_id=1,
        ),
        CursoEntity(
            sigla="LCS",
            nome="Licenciatura em Ciências Sociais",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TADS",
            nome="Tecnologia em Análise e Desenvolvimento de Sistemas",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TGA",
            nome="Tecnologia em Gestão Ambiental",
            campus_id=1,
        ),
        CursoEntity(
            sigla="MEC",
            nome="Técnico em Mecânica",
            campus_id=1,
        ),
        CursoEntity(
            sigla="INFO",
            nome="Técnico em Informática",
            campus_id=1,
        ),
        CursoEntity(
            sigla="MAMB",
            nome="Técnico em Meio Ambiente",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TPC",
            nome="Técnico em Produção Cultural",
            campus_id=1,
        ),
    ]


def test_listar_cursos(lista_cursos):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_cursos.return_value = lista_cursos
    policy.pode_listar.return_value = True

    usecase = ListarCursosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_cursos.assert_called()
    policy.pode_listar.assert_called()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_cursos


def test_nao_pode_listar_cursos(lista_cursos):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_cursos.return_value = lista_cursos
    policy.pode_listar.return_value = False

    usecase = ListarCursosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_cursos.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_curso.return_value = curso
    policy.pode_criar.return_value = True

    usecase = CadastrarCursoUsecase(repo, policy)
    result = usecase.execute(curso)

    repo.cadastrar_curso.assert_called_with(curso, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == curso


def test_nao_pode_cadastrar_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_curso.return_value = curso
    policy.pode_criar.return_value = False

    usecase = CadastrarCursoUsecase(repo, policy)
    result = usecase.execute(curso)

    repo.cadastrar_curso.assert_not_called()
    assert isinstance(result, ResultError)


def test_editar_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = curso
    repo.editar_curso.return_value = curso

    usecase = EditarCursoUsecase(repo, policy)
    result = usecase.execute(curso)

    repo.buscar_por_id.assert_called_with(curso.id)
    repo.editar_curso.assert_called_with(curso, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == curso


def test_nao_pode_editar_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_editar.return_value = False
    repo.buscar_por_id.return_value = curso
    repo.editar_curso.return_value = curso

    usecase = EditarCursoUsecase(repo, policy)
    result = usecase.execute(curso)

    repo.editar_curso.assert_not_called()
    assert isinstance(result, ResultError)


def test_remover_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = curso
    repo.remover_curso.return_value = curso

    usecase = RemoverCursoUsecase(repo, policy)
    result = usecase.execute(curso.id)

    repo.remover_curso.assert_called_with(curso.id, policy.user)
    assert isinstance(result, ResultSuccess)


def test_nao_pode_remover_curso(curso):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_remover.return_value = False
    repo.buscar_por_id.return_value = curso
    repo.remover_curso.return_value = curso

    usecase = RemoverCursoUsecase(repo, policy)
    result = usecase.execute(curso.id)

    repo.remover_curso.assert_not_called()
    assert isinstance(result, ResultError)
