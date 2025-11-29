from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from epi_admin.models import Colaborador
import random



class Command(BaseCommand):
    help = "Create test gerente users and add them to the 'Gerentes' group (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            dest="password",
            help="Password to set for the test users (default: gerente)",
            default="gerente",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            dest="force",
            help="If set, reset password for existing users",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        password = options.get("password") or "gerente"
        force = options.get("force")

        test_users = [
            ("gerente1", "gerente1@senai.sc.com"),
            ("gerente2", "gerente2@senai.sc.com"),
        ]

        group_name = "Gerentes"
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created group '{group_name}'"))
        else:
            self.stdout.write(f"Using existing group '{group_name}'")

        # Ensure the group has model permissions for Colaborador, EPI and Emprestimo
        app_label = "epi_admin"
        model_names = ["colaborador", "epi", "emprestimo"]
        perms_to_add = []
        for model in model_names:
            for action in ("add", "change", "delete", "view"):
                codename = f"{action}_{model}"
                try:
                    perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    perms_to_add.append(perm)
                except Permission.DoesNotExist:
                    # Skip silently; migrations/bootstrapping should create permissions
                    self.stdout.write(self.style.WARNING(f"Permission not found: {codename} (skipping)"))

        if perms_to_add:
            group.permissions.add(*perms_to_add)
            self.stdout.write(self.style.SUCCESS(f"Assigned permissions for models: {', '.join(model_names)} to group '{group_name}'"))

        created_any = False
        for username, email in test_users:
            user_qs = User.objects.filter(username=username)
            if user_qs.exists():
                user = user_qs.first()
                if force:
                    user.set_password(password)
                    user.is_staff = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated password for existing user: {username}"))
                else:
                    self.stdout.write(f"User exists: {username} (use --force to reset password)")
            else:
                user = User(username=username, email=email, is_staff=True)
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} / {email}"))
                created_any = True

            # Add user to group if not already
            if not user.groups.filter(name=group_name).exists():
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f"Added {username} to group '{group_name}'"))

            # Create up to 3 Colaborador records for this gerente (idempotent)
            try:
                existing = Colaborador.objects.filter(created_by=user).count()
            except Exception:
                existing = 0

            needed = max(0, 3 - existing)
            if needed > 0:
                first_names = ['Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gustavo', 'Helena', 'Igor', 'Julia']
                last_names = ['Silva', 'Souza', 'Oliveira', 'Santos', 'Pereira', 'Costa', 'Almeida', 'Gomes', 'Ribeiro', 'Fernandes']
                created = 0
                attempts = 0
                while created < needed and attempts < 20:
                    attempts += 1
                    fn = random.choice(first_names)
                    ln = random.choice(last_names)
                    # avoid exact duplicates for this user
                    if Colaborador.objects.filter(nome=fn, sobrenome=ln, created_by=user).exists():
                        continue
                    # create collaborator with a random cpf-like string
                    cpf = ''.join(str(random.randint(0, 9)) for _ in range(11))
                    col = Colaborador.objects.create(
                        nome=fn,
                        sobrenome=ln,
                        setor='Geral',
                        cpf=cpf,
                        created_by=user,
                    )
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"Created Colaborador {fn} {ln} for {username}"))
                if created < needed:
                    self.stdout.write(self.style.WARNING(f"Could only create {created} of {needed} colaboradores for {username}"))

        if not created_any:
            self.stdout.write(self.style.NOTICE("No new test users were created."))

        self.stdout.write(self.style.SUCCESS("create_test_users finished."))
