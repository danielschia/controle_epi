from django.apps import AppConfig
import logging


class EpiAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'epi_admin'

    def ready(self):
        """Ensure the 'Gerentes' group exists and has the standard model permissions.

        This runs on app startup. It is idempotent and safe to call multiple times.
        If the database isn't ready (during migrations), we quietly skip creation.
        """
        logger = logging.getLogger(__name__)
        try:
            import os
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group, Permission
            from django.db import OperationalError, ProgrammingError

            # Only ensure the 'Gerentes' group and its permissions exist here. Creation
            # of the superuser and test accounts is handled by the management command
            # `bootstrap_initial`, which can be invoked at server start.
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
            # 3) Create some test gerente user accounts and corresponding Gerente entries
            try:
                from .models import Gerente as GerenteModel
                gerente_password = os.environ.get('DJANGO_GERENTE_PASSWORD', 'gerente')
                test_gerentes = [
                    {'username': 'gerente1', 'email': 'gerente1@senai.sc.com', 'nome': 'Gerente', 'sobrenome': 'Um', 'setor': 'RH', 'cpf': '00000000001'},
                    {'username': 'gerente2', 'email': 'gerente2@senai.sc.com', 'nome': 'Gerente', 'sobrenome': 'Dois', 'setor': 'Produção', 'cpf': '00000000002'},
                ]
                for g in test_gerentes:
                    user_qs = User.objects.filter(email__iexact=g['email'])
                    if not user_qs.exists():
                        user = User.objects.create_user(username=g['username'], email=g['email'], password=gerente_password)
                        # give staff status so they can login to admin if needed
                        user.is_staff = True
                        user.save()
                        logger.info("Created test gerente user %s", g['email'])
                    else:
                        user = user_qs.first()
                    # Add to Gerentes group
                    group.user_set.add(user)
                    # Create or update Gerente model entry
                    gerente_obj, created = GerenteModel.objects.get_or_create(nome=g['nome'], sobrenome=g['sobrenome'], cpf=g['cpf'], defaults={'setor': g['setor'], 'fotoGerente': None})
                    if created:
                        logger.info("Created Gerente model entry for %s %s", g['nome'], g['sobrenome'])
            except Exception as e:
                # if models aren't ready yet or other DB issues, just log
                logger.debug("Skipping creation of test gerentes: %s", e)
        except (OperationalError, ProgrammingError) as e:
            # Database not ready (e.g., during migrate). Skip silently but log at debug level.
            logger.debug("Skipping automatic Gerentes group creation because DB is not ready: %s", e)
        except Exception as e:
            # Catch-all to avoid crashing app startup; log the error.
            logger.exception("Unexpected error while creating 'Gerentes' group: %s", e)
