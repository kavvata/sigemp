import random
from faker import Faker
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError, CommandParser

from emprestimo.domain.entities import EmprestimoEntity, TipoOcorrenciaEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import Emprestimo, TipoOcorrencia
from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)
from ensino.models import Aluno, Campus, Curso, FormaSelecao
from patrimonio.domain.entities import BemEntity
from patrimonio.models import (
    Bem,
    EstadoConservacao,
    GrauFragilidade,
    MarcaModelo,
    TipoBem,
)


class Command(BaseCommand):
    help = "Realiza cadastros auxiliares ao banco com dados da Instrução Normativa PROAD/IFPR nº 03/2022, com registros falsos para demonstracao"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "registros",
            type=int,
        )

    def handle(self, *args, **options):
        N = options.get("registros", 100)

        self.stdout.write("Iniciando população do banco...")
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

        lista_cursos = [
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

        base_date = datetime(2020, 1, 1)
        lista_entities = [
            FormaSelecaoEntity(
                descricao="Edital N°01/2020",
                periodo_inicio=base_date,
                periodo_fim=base_date + timedelta(days=180),
            ),
            FormaSelecaoEntity(
                descricao="Edital N°02/2020",
                periodo_inicio=base_date + timedelta(days=200),
                periodo_fim=base_date + timedelta(days=365),
            ),
            FormaSelecaoEntity(
                descricao="Edital N°03/2021",
                periodo_inicio=base_date.replace(year=2021, month=3, day=15),
                periodo_fim=base_date.replace(year=2021, month=9, day=15),
            ),
            FormaSelecaoEntity(
                descricao="Edital N°04/2021",
                periodo_inicio=base_date.replace(year=2021, month=10, day=1),
                periodo_fim=base_date.replace(year=2022, month=3, day=1),
            ),
            FormaSelecaoEntity(
                descricao="Edital N°05/2022",
                periodo_inicio=base_date.replace(year=2022, month=4, day=10),
                periodo_fim=base_date.replace(year=2023, month=4, day=10),
            ),
        ]

        formas_selecao_models = [
            FormaSelecao.objects.get_or_create(**e.to_dict())[0] for e in lista_entities
        ]

        faker = Faker("pt-BR")
        for i in range(N):
            curso = random.choice(lista_cursos)
            forma_selecao = random.choice(formas_selecao_models)
            is_menor = random.choice([True, False])

            if not is_menor:
                entity = AlunoEntity(
                    nome=faker.name(),
                    cpf=faker.ssn(),
                    email=faker.email(),
                    matricula=faker.numerify("2025####"),
                    telefone=faker.phone_number(),
                    forma_selecao_id=forma_selecao.id,
                    curso_id=curso.id,
                )
            else:
                entity = AlunoEntity(
                    nome=faker.name(),
                    nome_responsavel=faker.name(),
                    cpf=faker.ssn(),
                    email=faker.email(),
                    matricula=faker.numerify("2025####"),
                    telefone=faker.phone_number(),
                    forma_selecao_id=forma_selecao.id,
                    curso_id=curso.id,
                )
            Aluno.objects.get_or_create(
                **entity.to_dict(
                    [
                        "timestamps",
                        "id",
                    ]
                )
            )

        def generate_realistic_equipment():
            equipment_data = {
                "Projetor": {
                    "brands": ["Epson", "BenQ", "Optoma", "NEC", "ViewSonic"],
                    "models": [
                        "PowerLite",
                        "Business",
                        "Home Cinema",
                        "Workplace",
                        "Education",
                    ],
                    "suffixes": ["X49", "S500", "HD26", "W1070", "EB-U05"],
                },
                "Notebook": {
                    "brands": ["Dell", "Lenovo", "HP", "Acer", "Asus"],
                    "models": ["Latitude", "ThinkPad", "Pavilion", "Aspire", "Zenbook"],
                    "suffixes": ["5420", "T14", "15-eh", "A515", "UX425"],
                },
                "Microscópio": {
                    "brands": ["Optika", "Olympus", "Nikon", "Leica", "Zeiss"],
                    "models": [
                        "Biological",
                        "Stereo",
                        "Digital",
                        "Research",
                        "Student",
                    ],
                    "suffixes": ["B-150", "CX23", "Eclipse", "DM750", "Primo Star"],
                },
                "Equipamento de Laboratório": {
                    "brands": ["Minipa", "Instrutherm", "Tecnal", "Quimis", "Marconi"],
                    "models": [
                        "Analytical",
                        "Precision",
                        "Digital",
                        "Professional",
                        "Basic",
                    ],
                    "suffixes": ["ET-1002", "MA-100", "TE-100", "Q-100", "FE-100"],
                },
            }

            equipment_type = random.choice(list(equipment_data.keys()))
            brand = random.choice(equipment_data[equipment_type]["brands"])
            model = random.choice(equipment_data[equipment_type]["models"])
            suffix = random.choice(equipment_data[equipment_type]["suffixes"])

            templates = [
                f"{equipment_type} {brand} {model} {suffix}",
                f"{brand} {model} {suffix}",
                f"{equipment_type} {brand} {suffix}",
                f"{brand} {equipment_type} {model}",
            ]

            return random.choice(templates)

        for i in range(N):
            e = BemEntity(
                patrimonio=faker.numerify("###.###.###.###"),
                descricao=generate_realistic_equipment(),
                tipo_id=random.choice(TipoBem.objects.all()).id,
                grau_fragilidade_id=random.choice(GrauFragilidade.objects.all()).id,
                estado_conservacao_id=random.choice(EstadoConservacao.objects.all()).id,
                marca_modelo_id=random.choice(MarcaModelo.objects.all()).id,
            )

            Bem.objects.get_or_create(**e.to_dict())[0]

        entities = []
        for i in range(N):
            alunos_disponiveis = Aluno.objects.exclude(emprestimo__estado=1).distinct()

            bens_disponiveis = Bem.objects.exclude(emprestimo__estado=1).distinct()

            if not alunos_disponiveis.exists() or not bens_disponiveis.exists():
                print("Not enough available alunos or bens to create more empréstimos")
                break

            aluno = random.choice(alunos_disponiveis)
            bem = random.choice(bens_disponiveis)
            estado = random.choice(EmprestimoEstadoEnum.choices())[0]
            entity = EmprestimoEntity(
                aluno_id=aluno.id,
                aluno_nome=aluno.nome,
                aluno_matricula=aluno.matricula,
                bem_id=bem.id,
                bem_descricao=bem.descricao,
                bem_patrimonio=bem.patrimonio,
                data_emprestimo=datetime.now().date() - timedelta(days=i),
                data_devolucao_prevista=datetime.now().date() + timedelta(days=365),
                data_devolucao=datetime.now().date() + timedelta(days=365 - i)
                if estado == EmprestimoEstadoEnum.FINALIZADO
                else None,
                estado=estado,
                observacoes=f"Empréstimo {i + 1} para atividades acadêmicas. {faker.paragraph()}",
            )
            entities.append(entity)

        _models = [Emprestimo.objects.get_or_create(**e.to_dict())[0] for e in entities]

        self.stdout.write("... Banco populado!")
