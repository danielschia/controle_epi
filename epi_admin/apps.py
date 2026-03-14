from django.apps import AppConfig
import logging


class EpiAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'epi_admin'

    def ready(self):
        """Ensure the 'Gerentes' group exists and has the standard model permissions.

        This runs on app startup. It is idempotent and safe to call multiple times.
        If the database isn't ready (during migrations), we quietly skip creation.

        We defer database setup until the app is fully ready by using Django's
        app registry to avoid "Accessing the database during app initialization" warnings.
        """
        logger = logging.getLogger(__name__)

        # Defer database setup until Django signals that apps are ready
        from django.core.management import call_command
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def setup_groups_and_permissions(sender, **kwargs):
            """Called after migrations complete; safe to access the database."""
            try:
                from django.contrib.auth import get_user_model
                from django.contrib.auth.models import Group, Permission
                from django.db import OperationalError, ProgrammingError

                User = get_user_model()

                # Ensure the 'Gerentes' group with permissions for colaborador, epi and emprestimo only.
                models = ['colaborador', 'epi', 'emprestimo']
                actions = ['add', 'change', 'delete', 'view']
                codenames = [f"{action}_{model}" for model in models for action in actions]

                perms = Permission.objects.filter(codename__in=codenames, content_type__app_label='epi_admin')

                group, created = Group.objects.get_or_create(name='Gerentes')
                if created:
                    logger.info("Created 'Gerentes' group")
                # Assign permissions (idempotent)
                if perms.exists():
                    group.permissions.add(*perms)
                    logger.info("Assigned permissions to 'Gerentes' group")
                else:
                    logger.debug("No permissions found to assign to 'Gerentes' group (content types may not be ready yet)")
            except (OperationalError, ProgrammingError) as e:
                # Database not ready. Skip silently but log at debug level.
                logger.debug("Skipping Gerentes group creation because DB is not ready: %s", e)

        # Connect the signal only once (avoid duplicate signals on app reload)
        post_migrate.connect(setup_groups_and_permissions, weak=False)

