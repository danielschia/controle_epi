# Configuração de desenvolvimento — Controle de EPI

Este arquivo descreve o fluxo recomendado para configurar o ambiente de desenvolvimento e carregar dados de teste (seed) em Django.

Aviso de segurança
------------------
As contas criadas por padrão (superuser e contas de gerente de teste) usam senhas padrão para facilitar o desenvolvimento. Nunca exponha essas contas em produção. Troque as senhas imediatamente após criar o superuser.

Passos iniciais
---------------
1. Crie e ative o ambiente virtual (opcional, recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Execute migrações:

```bash
python manage.py migrate
```

3. (Opcional) Se quiser usar as contas de teste (Gerente) como fixtures, carregue as fixtures:

```bash
python manage.py loaddata epi_admin/fixtures/gerentes.json
```

4. Crie o superuser (se ainda não foi criado automaticamente):

```bash
python manage.py createsuperuser --username=controle_epi --email=controle_epi@senai.sc.com
```

5. (Opcional) Crie as contas de gerente de teste (usuários Django) com senhas via shell — isso garante que as senhas sejam corretamente hasheadas:

```bash
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()
password = 'gerente'  # ou use DJANGO_GERENTE_PASSWORD via envvar
for username, email in [('gerente1','gerente1@senai.sc.com'), ('gerente2','gerente2@senai.sc.com')]:
    u, created = User.objects.get_or_create(username=username, email=email)
    if created:
        u.set_password(password)
        u.is_staff = True
        u.save()
        print('Created', username)
    else:
        print('User exists:', username)

# Depois disso, associe os usuários ao grupo Gerentes (o grupo é criado automaticamente):
from django.contrib.auth.models import Group
g = Group.objects.get(name='Gerentes')
for email in ['gerente1@senai.sc.com','gerente2@senai.sc.com']:
    u = User.objects.get(email=email)
    g.user_set.add(u)

quit()
```

Alternativa: usar o comando de bootstrap automático em desenvolvimento
---------------------------------------------------------------
Ao executar `python manage.py runserver`, o script chama automaticamente o comando `bootstrap_initial` que cria um superuser padrão (se nenhum existir) e garante que o grupo `Gerentes` exista e contenha as permissões necessárias.

Variáveis de ambiente úteis
---------------------------
- `DJANGO_SUPERUSER_USERNAME` — username do superuser criado automaticamente (padrão: `controle_epi`).
- `DJANGO_SUPERUSER_EMAIL` — email do superuser (padrão: `controle_epi@senai.sc.com`).
- `DJANGO_SUPERUSER_PASSWORD` — senha do superuser (padrão: `admin`).
- `DJANGO_GERENTE_PASSWORD` — senha utilizada no exemplo do shell para gerentes (padrão: `gerente`).

Comandos úteis
--------------
- Rodar servidor: `python manage.py runserver`
- Carregar fixtures: `python manage.py loaddata epi_admin/fixtures/gerentes.json`
- Criar superuser: `python manage.py createsuperuser --username=controle_epi --email=controle_epi@senai.sc.com`
- Trocar senha do superuser: `python manage.py changepassword controle_epi`

Fluxo recomendado para a equipe
------------------------------
1. Puxar as últimas alterações do repositório.
2. Rodar `pip install -r requirements.txt` (se necessário).
3. Rodar `python manage.py migrate`.
4. Rodar `python manage.py loaddata epi_admin/fixtures/gerentes.json` (opcional — fixtures com dados de Gerente).
5. Rodar `python manage.py create_test_users` para criar contas de teste (usuários Django) com senhas hasheadas e adicioná-las ao grupo `Gerentes`.

Exemplos de uso do comando `create_test_users`
---------------------------------------------

```bash
# criar usuários com a senha padrão 'gerente'
python manage.py create_test_users

# criar usuários com uma senha personalizada
python manage.py create_test_users --password='minhaSenha123'

# resetar a senha de usuários já existentes
python manage.py create_test_users --password='novaSenha' --force
```

Observações:
- O comando é idempotente: não criará duplicatas se os usuários já existirem.
- Por padrão ele cria `gerente1` e `gerente2` com emails `gerente1@senai.sc.com` e `gerente2@senai.sc.com`.
- O comando tenta associar ao grupo `Gerentes` e atribuir permissões de `add/change/delete/view` para os modelos `Colaborador`, `EPI` e `Emprestimo` (essas permissões devem existir após as migrações).

Se quiser que eu adicione mais opções (por exemplo, nomes/emails customizáveis ou criação de mais usuários), eu posso estender o comando.
