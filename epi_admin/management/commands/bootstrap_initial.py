from django.core.management.base import BaseCommand
import logging
import os
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create default superuser, Gerentes group and test gerente accounts (idempotent).'

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group, Permission
            from django.db import transaction
            User = get_user_model()

            # Create superuser if none exists
            if not User.objects.filter(is_superuser=True).exists():
                su_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'controle_epi')
                su_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'controle_epi@senai.sc.com')
                su_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
                try:
                    User.objects.create_superuser(username=su_username, email=su_email, password=su_password)
                    logger.warning("Created default superuser '%s'", su_username)
                except Exception as e:
                    logger.exception("Failed to create default superuser: %s", e)
            else:
                logger.debug('Superuser already exists; skipping creation')

            # Ensure Gerentes group and permissions
            models = ['colaborador', 'epi', 'emprestimo']
            actions = ['add', 'change', 'delete', 'view']
            codenames = [f"{action}_{model}" for model in models for action in actions]
            perms = Permission.objects.filter(codename__in=codenames, content_type__app_label='epi_admin')
            group, created = Group.objects.get_or_create(name='Gerentes')
            if created:
                logger.info("Created 'Gerentes' group")
            if perms.exists():
                group.permissions.add(*perms)
                logger.info("Assigned permissions to 'Gerentes' group")
            else:
                logger.debug("No permissions found to assign to 'Gerentes' group (content types may not be ready yet)")

            # Test gerente users are provided via fixtures. Developers can load them
            # with 'python manage.py loaddata epi_admin/fixtures/gerentes.json'.
            # Additionally, create test users and sample colaboradores automatically.
            try:
                call_command('create_test_users')
                logger.info('Ran create_test_users to ensure test gerentes and colaboradores exist')
            except Exception:
                logger.exception('Failed to run create_test_users')

        except Exception as e:
            logger.exception('bootstrap_initial failed: %s', e)