from django.core.management.base import BaseCommand, CommandError

from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.models import TipoOcorrencia
from ensino.domain.entities import CampusEntity, CursoEntity
from ensino.models import Campus, Curso
from patrimonio.models import EstadoConservacao, GrauFragilidade, MarcaModelo, TipoBem


class Command(BaseCommand):
    help = "Realiza cadastros auxiliares ao banco com dados da Instrução Normativa PROAD/IFPR nº 03/2022"

    def handle(self, *args, **options):
        marcas_modelos_dict = [
            {"marca": "Epson", "modelo": "PowerLite X49"},
            {"marca": "Dell", "modelo": "Latitude 5420"},
            {"marca": "Optika", "modelo": "B-150R"},
            {"marca": "Minipa", "modelo": "ET-1002"},
            {"marca": "Canon", "modelo": "EOS Rebel T7"},
        ]
        marcas_modelos_models = [
            MarcaModelo.objects.get_or_create(marca=mm["marca"], modelo=mm["modelo"])[0]
            for mm in marcas_modelos_dict
        ]

        estados_conservacao_dict = [
            {"descricao": "Péssimo", "nivel": 1},
            {"descricao": "Mau", "nivel": 2},
            {"descricao": "Médio", "nivel": 3},
            {"descricao": "Bom", "nivel": 4},
            {"descricao": "Excelente", "nivel": 5},
        ]
        estados_conservacao_models = [
            EstadoConservacao.objects.get_or_create(
                descricao=ec["descricao"], nivel=ec["nivel"]
            )[0]
            for ec in estados_conservacao_dict
        ]

        tipos_de_bem = [
            {"descricao": "Projetor"},
            {"descricao": "Notebook Dell"},
            {"descricao": "Frasco laboratorio"},
        ]
        tipos_de_bem_models = [
            TipoBem.objects.get_or_create(descricao=tp["descricao"])[0]
            for tp in tipos_de_bem
        ]

        graus = [
            GrauFragilidade(id=1, descricao="Baixo", nivel=1),
            GrauFragilidade(id=2, descricao="Médio", nivel=2),
            GrauFragilidade(id=3, descricao="Alto", nivel=3),
        ]

        GrauFragilidade.objects.bulk_create(graus)

        entity = CampusEntity(id=1, sigla="PNG", nome="Paranaguá")
        model, _criado = Campus.objects.get_or_create(
            **entity.to_dict(
                exclude=[
                    "timestamps",
                    "campus_sigla",
                ]
            )
        )
        lista_entities = [
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

        lista_models = [
            Curso.objects.get_or_create(
                **e.to_dict(
                    [
                        "timestamps",
                        "id",
                        "campus_sigla",
                    ]
                )
            )[0]
            for e in lista_entities
        ]

        lista_entities = [
            TipoOcorrenciaEntity(id=1, descricao="Perda"),
            TipoOcorrenciaEntity(id=2, descricao="Roubo"),
            TipoOcorrenciaEntity(id=3, descricao="Extravio"),
            TipoOcorrenciaEntity(id=4, descricao="Dano"),
        ]

        tipos_ocorrencia_models = [
            TipoOcorrencia.objects.get_or_create(**e.to_dict())[0]
            for e in lista_entities
        ]

        self.stdout.write("... Banco populado!")
