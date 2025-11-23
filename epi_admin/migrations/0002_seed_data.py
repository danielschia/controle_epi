from django.db import migrations


def create_seed_data(apps, schema_editor):
    import os
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group, Permission

    User = get_user_model()

    # Create superuser if none exists
    if not User.objects.filter(is_superuser=True).exists():
        su_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'controle_epi')
        su_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'controle_epi@senai.sc.com')
        su_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
        try:
            User.objects.create_superuser(username=su_username, email=su_email, password=su_password)
        except Exception:
            # If creation fails, continue without raising to avoid blocking migrations
            pass

    # Create Gerentes group with permissions for colaborador, epi and emprestimo
    models = ['colaborador', 'epi', 'emprestimo']
    actions = ['add', 'change', 'delete', 'view']
    codenames = [f"{action}_{model}" for model in models for action in actions]

    perms = Permission.objects.filter(codename__in=codenames, content_type__app_label='epi_admin')
    group, created = Group.objects.get_or_create(name='Gerentes')
    if perms.exists():
        group.permissions.add(*perms)

    # Note: test users are supplied via fixtures in epi_admin/fixtures/ (load with loaddata)


def remove_seed_data(apps, schema_editor):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    User = get_user_model()

    # Remove test gerente users if they exist
    for email in ['gerente1@senai.sc.com', 'gerente2@senai.sc.com']:
        try:
            user = User.objects.filter(email__iexact=email).first()
            if user:
                user.delete()
        except Exception:
            pass

    # Remove Gerentes group (only if exists)
    try:
        Group.objects.filter(name='Gerentes').delete()
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('epi_admin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_seed_data, remove_seed_data),
    ]
