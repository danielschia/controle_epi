import os
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from epi_admin.models import Colaborador, Gerente


class Command(BaseCommand):
    help = "Create demo users and add them to the 'Gerentes' group (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            dest='password',
            help='Password for demo users (or set DJANGO_GERENTE_PASSWORD)',
            default=None,
        )
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Reset passwords for existing demo users',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        password = options.get('password') or os.environ.get('DJANGO_GERENTE_PASSWORD')
        if not password:
            raise CommandError(
                'Informe --password ou defina DJANGO_GERENTE_PASSWORD para criar usuários de teste.'
            )
        force = options.get('force')
        test_users = [
            ('gerente1', 'gerente1@example.local'),
            ('gerente2', 'gerente2@example.local'),
        ]

        group, created = Group.objects.get_or_create(name='Gerentes')
        if created:
            self.stdout.write(self.style.SUCCESS("Created group 'Gerentes'"))
        else:
            self.stdout.write("Using existing group 'Gerentes'")

        model_names = ['colaborador', 'epi', 'emprestimo']
        permissions = []
        for model in model_names:
            for action in ('add', 'change', 'delete', 'view'):
                permission = Permission.objects.filter(
                    content_type__app_label='epi_admin',
                    codename=f'{action}_{model}',
                ).first()
                if permission:
                    permissions.append(permission)
        if permissions:
            group.permissions.add(*permissions)
            self.stdout.write(self.style.SUCCESS("Assigned standard model permissions"))

        created_any = False
        for username, email in test_users:
            user = User.objects.filter(
                Q(username=username) | Q(username=email)
            ).first()
            if user is None:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                )
                user.is_staff = True
                user.save()
                created_any = True
                self.stdout.write(self.style.SUCCESS(f'Created demo user: {email}'))
            elif force:
                user.set_password(password)
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Updated demo user: {email}'))
            else:
                self.stdout.write(f'Demo user already exists: {email}')

            if not user.groups.filter(name=group.name).exists():
                user.groups.add(group)

            cpf_candidate = ''.join(str(random.randint(0, 9)) for _ in range(11))
            while Gerente.objects.filter(cpf=cpf_candidate).exists():
                cpf_candidate = ''.join(str(random.randint(0, 9)) for _ in range(11))

            gerente, gerente_created = Gerente.objects.get_or_create(
                user=user,
                defaults={
                    'nome': username.capitalize(),
                    'sobrenome': 'Demonstração',
                    'setor': 'Geral',
                    'cpf': cpf_candidate,
                    'email': user.email,
                },
            )
            if gerente_created:
                self.stdout.write(self.style.SUCCESS(f'Created Gerente for {email}'))
            elif gerente.email != user.email:
                gerente.email = user.email
                gerente.save()

            existing = Colaborador.objects.filter(created_by=user).count()
            first_names = ['Ana', 'Bruno', 'Carla', 'Diego', 'Elisa', 'Felipe', 'Sofia']
            last_names = ['Exemplo', 'Demonstração', 'Teste']
            for index in range(max(0, 3 - existing)):
                Colaborador.objects.create(
                    nome=first_names[index % len(first_names)],
                    sobrenome=last_names[index % len(last_names)],
                    setor='Geral',
                    cpf=''.join(str(random.randint(0, 9)) for _ in range(11)),
                    created_by=user,
                )

        if not created_any:
            self.stdout.write(self.style.NOTICE('No new demo users were created.'))
        self.stdout.write(self.style.SUCCESS('create_test_users finished.'))
