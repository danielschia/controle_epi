import logging
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create configured superuser, Gerentes group and demo data (idempotent).'

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            su_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            su_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.local')
            su_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            if not su_password:
                raise CommandError(
                    'Defina DJANGO_SUPERUSER_PASSWORD antes de executar bootstrap_initial.'
                )
            User.objects.create_superuser(
                username=su_username,
                email=su_email,
                password=su_password,
            )
            logger.info("Created configured superuser '%s'", su_username)
        else:
            logger.debug('Superuser already exists; skipping creation')

        models = ['colaborador', 'epi', 'emprestimo']
        actions = ['add', 'change', 'delete', 'view']
        codenames = [f'{action}_{model}' for model in models for action in actions]
        permissions = Permission.objects.filter(
            codename__in=codenames,
            content_type__app_label='epi_admin',
        )
        group, created = Group.objects.get_or_create(name='Gerentes')
        if created:
            logger.info("Created 'Gerentes' group")
        if permissions.exists():
            group.permissions.add(*permissions)
            logger.info("Assigned standard permissions to 'Gerentes' group")
        else:
            logger.debug('No matching model permissions found after migrations')

        try:
            call_command('create_test_users')
        except CommandError:
            raise
        except Exception:
            logger.exception('Failed to run create_test_users')
