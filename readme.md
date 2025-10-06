<h1 align="center" id="title">Sistema web para gestão de empréstimo de bens móveis - IFPR</h1>

<p align="center"><img src="https://socialify.git.ci/kavvata/sigemp/image?logo=https%3A%2F%2Fraw.githubusercontent.com%2Fkavvata%2Fsigemp%2F15c9fcb0295c11faf4129d9e97485ca20f137e1d%2Flogo%2Fsigemp-logo.svg&amp;name=1&amp;owner=1&amp;pattern=Plus&amp;theme=Light" alt="project-image"></p>

<p id="description">Solução web voltada à gestão de empréstimo de equipamentos para estudantes do IFPR, automatizando o fluxo de empréstimo digitalização de termos e garantindo auditoria das atividades.</p>

<p align="center"><img src="https://img.shields.io/github/issues/kavvata/sigemp" alt="shields"><img src="https://img.shields.io/github/stars/kavvata/sigemp?style=flat" alt="shields"><img src="https://img.shields.io/github/license/kavvata/sigemp" alt="shields"><img src="https://img.shields.io/github/check-runs/kavvata/sigemp/main" alt="shields"></p>

<h2>Imagens do projeto</h2>

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_login.png" alt="project-screenshot" width="1670" >

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_painel.png" alt="project-screenshot" width="1670" >

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_painel_modo_escuro.png" alt="project-screenshot" width="1670" >

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_listar_emprestimos.png" alt="project-screenshot" width="1670" >

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_emprestimo_detalhes.png" alt="project-screenshot" width="1670">

<img src="https://raw.githubusercontent.com/kavvata/sigemp/refs/heads/docs/resources/screenshots/sigemp_listar_ocorrencias.png" alt="project-screenshot" width="1670" >

<h2>🧐 Funcionalidades</h2>

Principais recursos do sistema:

- Gestão e auditoria de empréstimos;
- Gestão e auditoria de ocorrências;
- Geração de termos em PDF;
- Notificação via e-mail de prazos (TODO).

<h2>🛠️ Passos de instalação</h2>

Para levantar o **SIGEMP** localmente:

<p>1. Configurar variáveis de ambiente:</p>

```
cp .env-example .env
```

<p>2. Compilar imagens docker:</p>

```
make build
```

<p>3. Levantar containers:</p>

```
make up
```

<p>4. Iniciar node com  tailwind:</p>

```
make tailwind
```

<p>4. Coletar estáticos:</p>

```
make collectstatic
```

<h2>🧪 Testes</h2>

Executar testes com `pytest` e gerar cobertura:

```
pytest --maxfail=1 --disable-warnings -q
pytest --cov=src --cov-report=term-missing
```

<h2>📁 Estrutura</h2>

- `[modulo]/domain/`: entidades e tipos utilizados em casos de uso;
- `[modulo]/infrastructure/`: ferramentas para mapeamento entre dados de borda e dados de domínio;
- `[modulo]/models.py`: modelos ORM;
- `[modulo]/repositories/`: contratos e implementação de classes repositório;
- `[modulo]/policies/`: contratos e implementação de classes policy;
- `[modulo]/presentation/`: roteamento, processamento de requisições, validação de formulários;
- `[modulo]/usecases/`: validação de regras de negócio;
- `[modulo]/templates/`: templates HTML para renderização das telas;

<h2>💻 Construido com</h2>

Tecnologias usadas no projeto:

- Django
- Weazyprint
- Alpine.js
- Tailwind CSS
