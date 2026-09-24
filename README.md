# Controle de EPI

Aplicação Django para controle de equipamentos de proteção individual (EPIs),
colaboradores, gerentes e empréstimos.

## O que está incluído

- Models de colaboradores, gerentes, EPIs e empréstimos.
- Autenticação por e-mail com backend customizado.
- Grupo de permissões `Gerentes`.
- Regras de validação para estoque, datas e colaborador inativo.
- Interface web e Django Admin restrito a superusuários.
- Testes automatizados com pytest.

## Requisitos

- Python 3.11+
- SQLite para desenvolvimento local
- `pip` ou `uv`

## Instalação

```bash
git clone https://github.com/danielschia/controle_epi.git
cd controle_epi
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

O arquivo `db.sqlite3` é local e não deve ser versionado. O `.gitignore` já
protege bancos, arquivos `.env`, caches e uploads.

## Configuração segura

Copie as variáveis de ambiente do exemplo e edite localmente:

```bash
cp .env.example .env
```

O arquivo `.env` não deve ser enviado ao Git. Principalmente em produção,
defina uma chave longa e aleatória:

```bash
DJANGO_SECRET_KEY=gere-uma-chave-longa-e-aleatoria
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.local
DJANGO_SUPERUSER_PASSWORD=uma-senha-forte
DJANGO_GERENTE_PASSWORD=uma-senha-forte-diferente
```

O projeto não usa uma senha padrão para criar o superusuário. O comando de
bootstrap exige `DJANGO_SUPERUSER_PASSWORD` e encerra com erro caso ela não
esteja definida.

## Dados fictícios

O comando abaixo cria usuários de demonstração, permissões, gerentes e
colaboradores com dados sintéticos. A senha deve ser fornecida localmente:

```bash
export DJANGO_GERENTE_PASSWORD='senha-local-de-teste'
python manage.py create_test_users
```

Os e-mails gerados usam o domínio reservado `example.local`, e os CPFs são
valores fictícios. O comando é idempotente. Para gerar um novo conjunto de
credenciais de demonstração, use outra senha local; não reutilize senhas reais.

Se quiser apenas criar dados de gerente via fixture:

```bash
python manage.py loaddata epi_admin/fixtures/gerentes.json
```

## Executar

```bash
python manage.py runserver
```

Acesse:

- Aplicação: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Crie um superusuário manualmente quando necessário:

```bash
python manage.py createsuperuser
```

## Testes e verificações

```bash
python manage.py check
python -m pytest -q
```

## Estrutura

```text
controle_epi/                 projeto Django e settings
epi_admin/                    aplicação de domínio
├── management/commands/      comandos de bootstrap e dados de demonstração
├── migrations/               migrações do banco
├── templates/                templates da aplicação
└── tests/                    testes automatizados
```

## Segurança antes de publicar

- Não versione `.env`, bancos SQLite, uploads ou caches.
- Não use `DEBUG=True` em produção.
- Troque a `DJANGO_SECRET_KEY` e todas as senhas de demonstração.
- Use PostgreSQL ou outro banco gerenciado em produção.
- Não use CPFs ou e-mails reais em fixtures, commits ou issues.
- Considere adicionar CI para executar `python manage.py check` e `pytest -q`.

## Licença

Este repositório não possui uma licença específica no momento.
