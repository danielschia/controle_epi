# 🛡️ Controle de EPI — Guia Completo

Este repositório contém um aplicativo Django para controlar Equipamentos de Proteção Individual (EPI), colaboradores, gerentes e empréstimos.

Este README foi consolidado para incluir tudo necessário para configurar e rodar o projeto tanto em macOS quanto em Windows (PowerShell / CMD). Para detalhes exclusivamente de desenvolvimento (dicas, fixtures, comandos extras) veja também `README_DEV.md`.

Índice rápido
- Pré-requisitos
- Instalação (macOS / Linux e Windows)
- Variáveis de ambiente
- Migrações e banco de dados
- Criar usuário(s) e seed/test data
- Rodar servidor
- Resetar banco (opções)
- Media/Uploads
- Testes
- Problemas comuns / Troubleshooting
- Desenvolvimento e contribuições

---

## 🚀 Pré-requisitos

- Python 3.11+ (recomendado)
- pip
- (opcional) virtualenv / venv
- SQLite (já incluído no Python padrão — usado por padrão neste projeto)

Recomendado: use um ambiente virtual para isolar dependências.

---

## 📦 Instalação e first-run (macOS / Linux)

Abra um terminal e execute:

```bash
# clone (se ainda não clonou)
git clone <REPO_URL>
cd controle_epi/controle_epi

# criar e ativar venv (bash/zsh)
python -m venv .venv
source .venv/bin/activate

# instalar dependências
pip install -r requirements.txt

# aplicar migrações
python manage.py migrate

# criar superuser (interativo)
python manage.py createsuperuser

# (opcional) criar usuários de teste e colaboradores
python manage.py create_test_users

# iniciar servidor de desenvolvimento
python manage.py runserver
```

Em seguida, acesse: http://127.0.0.1:8000/ (aplicação) e http://127.0.0.1:8000/admin/ (admin).

---

## � Instalação e first-run (Windows — PowerShell)

Abra PowerShell e execute:

```powershell
git clone <REPO_URL>
cd .\controle_epi\controle_epi

# criar e ativar venv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# instalar dependências
pip install -r requirements.txt

# aplicar migrações
python manage.py migrate

# criar superuser
python manage.py createsuperuser

# (opcional) criar usuários de teste
python manage.py create_test_users

# iniciar servidor
python manage.py runserver
```

No CMD (Prompt) o comando para ativar o venv é:

```cmd
.venv\Scripts\activate
```

---

## 🔧 Variáveis de ambiente úteis

Você pode definir as seguintes variáveis (ex.: em `.env` ou no ambiente):

- `DJANGO_SECRET_KEY` — chave secreta Django (produção)
- `DJANGO_SUPERUSER_USERNAME` — username do superuser criado automaticamente
- `DJANGO_SUPERUSER_EMAIL` — email do superuser
- `DJANGO_SUPERUSER_PASSWORD` — senha do superuser
- `DJANGO_GERENTE_PASSWORD` — senha padrão de gerentes de teste (usado por scripts)

Exemplo `.env` (não comite este arquivo em repositórios públicos):

```
DJANGO_SECRET_KEY=troque-por-uma-chave-secreta
DJANGO_SUPERUSER_USERNAME=controle_epi
DJANGO_SUPERUSER_EMAIL=controle_epi@senai.sc.com
DJANGO_SUPERUSER_PASSWORD=senhaSegura123
DJANGO_GERENTE_PASSWORD=gerente
```

---

## 🗂️ Migrações e banco de dados

- Criar novas migrações (após mudanças em models):

```bash
python manage.py makemigrations
python manage.py migrate
```

- Verificar migrações pendentes:

```bash
python manage.py showmigrations
```

Observação: o projeto usa SQLite por padrão (`db.sqlite3` no diretório do projeto). Em produção recomendamos usar Postgres ou outro serviço de banco e configurar `DATABASES` em `controle_epi/settings.py`.

---

## 👥 Usuários, grupos e seed data

- O projeto cria automaticamente o grupo `Gerentes` com permissões essenciais.
- Para criar contas de teste (gerente1 e gerente2) execute:

```bash
python manage.py create_test_users
# --force para resetar senhas
python manage.py create_test_users --force
```

- Você também pode carregar fixtures (se presente):

```bash
python manage.py loaddata epi_admin/fixtures/gerentes.json
```

Notas importantes:
- `create_test_users` é idempotente: não criará duplicatas.
- O sistema foi configurado para usar email como `username` quando criamos usuários automaticamente — o fluxo de login usa email.

---

## ▶️ Rodar servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

Se preferir executar em background/porta diferente:

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## ♻️ Resetar o banco de dados (duas opções)

ATENÇÃO: esses comandos são destrutivos. Faça backup antes de prosseguir.

Opção A — reset simples (recomendado para dev):

```bash
# pare o servidor
cp db.sqlite3 db.sqlite3.bak   # backup
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py create_test_users
```

Opção B — reset completo (apaga também histórico de migrations):

```bash
git checkout -b reset-migrations-backup
cp db.sqlite3 db.sqlite3.bak
# remover arquivos de migrations (mantendo __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py create_test_users
```

Windows (PowerShell) equivalente para remover migrations:

```powershell
# execute com cuidado
Get-ChildItem -Path . -Recurse -Include "migrations" | ForEach-Object {
	Get-ChildItem $_.FullName -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
}
```

Se algo der errado, restaure com:

```bash
cp db.sqlite3.bak db.sqlite3
```

---

## 📁 Media / uploads

Uploads são gravados na pasta `media/` (ver `settings.py`).

Para apagar arquivos de upload ao resetar o projeto:

```bash
rm -rf media/
mkdir media
```

No Windows (PowerShell):

```powershell
Remove-Item -Recurse -Force .\media\
New-Item -ItemType Directory -Path .\media\
```

---

## ✅ Testes

Existem duas formas comuns de executar os testes neste projeto.

1) Usando o runner padrão do Django:

```bash
python manage.py test
```

2) Usando pytest (recomendado para desenvolvimento):

```bash
# ative seu venv (bash/zsh)
source .venv/bin/activate

# instale dependências (inclui pytest/pytest-django)
python -m pip install -r requirements.txt

# executar pytest
pytest -q
```

Observações:
- `requirements.txt` já inclui `pytest` e `pytest-django` para facilitar a execução local e em CI.
- Os testes usam fixtures do `pytest-django` (ex.: `django_user_model`, `client`).
- Há uma fixture autouse que isola `MEDIA_ROOT` durante os testes para evitar poluir a árvore do projeto.

CI / integração contínua

- Recomendo adicionar um workflow que execute `pip install -r requirements.txt` e `pytest -q` em cada PR.

---

## 🐞 Troubleshooting (comuns)

- Erro `no such table`: rode `python manage.py migrate` antes de executar comandos que acessam o DB.
- Erro `UNIQUE constraint failed: ...`: podem existir registros duplicados; revisar a tabela e remover/ajustar manualmente ou restaurar do backup.
- Problemas com ambiente virtual: verifique se ativou o venv correto (`.venv/bin/activate` no macOS, `.venv\Scripts\activate` no Windows).

Se precisar de ajuda, cole a saída do terminal e eu ajudo a diagnosticar.

---

## 🛠️ Desenvolvimento & contribuições

1. Crie uma branch para sua feature: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git add -A && git commit -m 'Adiciona sua feature'`
3. Push para o branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

Para desenvolvedores: veja `README_DEV.md` para detalhes de fixtures, scripts de bootstrap e recomendações de fluxo de trabalho.

---

## 📚 Links úteis

- Django: https://docs.djangoproject.com/
- Django Admin: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/

---

Última atualização: 2026-02-28
- **CSS customizado**: `epi_admin/static/admin/css/custom_admin.css`

## 📅 Formato de Datas

Todas as datas usam o formato **DD/MM/YY**:

- Campo "Validade" (EPI)
- Campo "Data de Empréstimo"
- Campo "Data de Devolução"

Um datepicker JS (flatpickr) é fornecido para facilitar a entrada de datas.

## 🔒 Segurança e Produção

Veja a seção "Aviso de segurança" em [`README_DEV.md`](./README_DEV.md) para checklist de produção.

## 🐛 Troubleshooting e Desenvolvimento

Para questões de setup, troubleshooting, segurança, permissões e desenvolvimento, consulte [`README_DEV.md`](./README_DEV.md).

## 📚 Documentação Adicional

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)
- [Forms Django](https://docs.djangoproject.com/en/5.2/topics/forms/)

## 🤝 Contribuindo

1. Crie um branch para sua feature: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m 'Adiciona sua feature'`
3. Push para o branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

## 📄 Licença

Este projeto é fornecido sem licença específica. Use conforme necessário.

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.

---

**Última atualização**: Novembro de 2025
