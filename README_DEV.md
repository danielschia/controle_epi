# Guia de desenvolvimento

## Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

O banco `db.sqlite3`, caches e uploads são artefatos locais. Não os versione.

## Configuração

Use `.env` local, baseado em `.env.example`. Nunca coloque senhas reais em
arquivos versionados, na documentação ou em commits.

Variáveis relevantes:

- `DJANGO_SECRET_KEY`: chave de assinatura da aplicação.
- `DJANGO_SUPERUSER_USERNAME`: usuário administrativo inicial.
- `DJANGO_SUPERUSER_EMAIL`: e-mail administrativo inicial.
- `DJANGO_SUPERUSER_PASSWORD`: senha administrativa inicial.
- `DJANGO_GERENTE_PASSWORD`: senha usada apenas pelo comando de dados fictícios.

## Dados fictícios

O comando `create_test_users` cria usuários de demonstração com o domínio
reservado `example.local`, dados fictícios e senhas fornecidas localmente:

```bash
export DJANGO_GERENTE_PASSWORD='senha-local-de-teste'
python manage.py create_test_users
```

O comando é idempotente. Para atualizar senhas de usuários de demonstração
existentes, execute com `--force` e uma senha local diferente:

```bash
python manage.py create_test_users --password='outra-senha-local' --force
```

Também é possível carregar somente os gerentes fictícios:

```bash
python manage.py loaddata epi_admin/fixtures/gerentes.json
```

Nunca coloque CPFs reais, e-mails reais ou senhas em fixtures.

## Verificações

```bash
python manage.py check
python -m pytest -q
```

## Checklist de publicação

1. Confirmar que `git status` não mostra `.env`, `db.sqlite3`, `media/` ou caches.
2. Executar os testes.
3. Revisar `git grep -n -I -E 'senha|password|token|secret|@'` antes do commit.
4. Não publicar branches, tags ou arquivos de backup antigos.
5. Após publicar, verificar o conteúdo da branch pública e o histórico acessível.

## Segurança de produção

- Definir `DJANGO_SECRET_KEY` e senhas exclusively no ambiente/secret manager.
- Desativar `DEBUG`.
- Configurar `ALLOWED_HOSTS` e HTTPS.
- Usar banco gerenciado e migrações controladas.
- Não usar os comandos de demonstração em produção.
