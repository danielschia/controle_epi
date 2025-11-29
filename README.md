# 🛡️ Controle de EPI

Sistema de controle e gerenciamento de Equipamentos de Proteção Individual (EPI) desenvolvido com Django.

## 📋 Visão Geral

Este é um aplicativo web para gerenciar:
- **Colaboradores**: Registro de funcionários
- **Gerentes**: Usuários administradores que gerenciam colaboradores
- **EPIs**: Equipamentos de proteção individual e seu controle
- **Empréstimos**: Rastreamento de empréstimos de EPI aos colaboradores

## 🚀 Pré-requisitos

- Python 3.11+
- Django 5.2+
- SQLite3 (padrão)
- pip (gerenciador de pacotes Python)

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/controle_epi.git
cd controle_epi/controle_epi
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
# no Windows:
# .venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Se não existir `requirements.txt`, instale manualmente:

```bash
pip install Django==5.2.8 Pillow
```

### 4. Aplicar migrações do banco de dados

```bash
python manage.py makemigrations epi_admin
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

O servidor criará automaticamente:
- Superuser padrão (configure via variáveis de ambiente)
- Grupo de Gerentes com permissões
- Usuários de teste e colaboradores de exemplo

Para detalhes de configuração manual, veja [`README_DEV.md`](./README_DEV.md).

## 🏃 Executando a Aplicação

### Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará disponível em: **http://127.0.0.1:8000/**

### Acessar a interface

- **Aplicação principal**: http://127.0.0.1:8000/
- **Admin (superuser only)**: http://127.0.0.1:8000/admin/

## 🔐 Autenticação

- Use **email** para fazer login
- Configure usuários e senhas via variáveis de ambiente (veja `README_DEV.md`)

Para maiores detalhes sobre usuários, grupos, permissões e troubleshooting, veja [`README_DEV.md`](./README_DEV.md).

## 📊 Funcionalidades Principais

### Colaboradores

- Listar, criar, editar e deletar colaboradores
- Apenas o criador (ou superuser) pode editar/deletar
- Campos: nome, sobrenome, setor, CPF, foto

### EPIs

- Controle de equipamentos de proteção
- Data de validade com datepicker (formato DD/MM/YY)
- Quantidade em estoque
- Foto do equipamento

### Empréstimos

- Registrar quando um colaborador retira um EPI
- Rastrear devolução com data e condições
- Datas com datepicker (formato DD/MM/YY)

### Gerentes

- Apenas superusers podem criar/editar gerentes
- Cada gerente tem uma conta de usuário Django associada
- Pode editar apenas sua própria conta

## 🛠️ Configuração Avançada

### Variáveis de Ambiente (Desenvolvimento)

Crie um arquivo `.env` na raiz do projeto (opcional):

```env
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_SUPERUSER_USERNAME=controle_epi
DJANGO_SUPERUSER_EMAIL=controle_epi@example.local
DJANGO_SUPERUSER_PASSWORD=sua-senha-forte
DJANGO_GERENTE_PASSWORD=gerente
```

### Estrutura de Diretórios

```
controle_epi/
├── controle_epi/              # Configuração do projeto
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # Rotas do projeto
│   ├── admin_site.py          # Admin customizado
│   └── wsgi.py                # WSGI para deploy
├── epi_admin/                 # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Vistas (controllers)
│   ├── urls.py                # Rotas da app
│   ├── forms.py               # Formulários
│   ├── static/                # CSS, JS, imagens
│   ├── templates/             # Templates HTML
│   └── management/commands/   # Comandos customizados
├── manage.py                  # Script de gerenciamento Django
├── db.sqlite3                 # Banco de dados (SQLite)
└── requirements.txt           # Dependências Python
```

## 📝 Comandos Úteis

### Gerenciamento de Usuários

Veja [`README_DEV.md`](./README_DEV.md) para:
- Criar superuser
- Criar usuários de teste (gerentes e colaboradores)
- Mudar senhas
- Gerenciar permissões

### Banco de Dados

```bash
# Ver migrações pendentes
python manage.py showmigrations

# Aplicar migrações
python manage.py migrate

# Criar novas migrações
python manage.py makemigrations epi_admin

# Resetar banco (⚠️ Apaga tudo)
python manage.py flush
```

### Desenvolvimento

```bash
# Shell interativo Django
python manage.py shell

# Executar testes
python manage.py test

# Coletador de static files (necessário para produção)
python manage.py collectstatic
```

## 🎨 Customização do Admin

O Django admin foi customizado para a aplicação:

- **URL**: http://127.0.0.1:8000/admin/
- **Acesso**: Apenas superusers
- **Branding**: Logo e cores personalizadas
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
