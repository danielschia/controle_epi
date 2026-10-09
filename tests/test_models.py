import pytest

from epi_admin.models import Colaborador, Gerente


@pytest.mark.django_db
def test_create_user(django_user_model: Gerente):
    initial = django_user_model.objects.count()
    django_user_model.objects.create_user(username='testuser', email='testuser@example.com', password='pass')
    assert django_user_model.objects.count() == initial + 1


@pytest.mark.django_db
def test_create_test_users_command():
    from django.core.management import call_command

    from epi_admin.models import Gerente

    call_command('create_test_users', password='local-test-password')

    assert Gerente.objects.count() >= 2

@pytest.mark.django_db
def test_create_test_users_command_is_idempotent():
    from django.core.management import call_command

    from epi_admin.models import Gerente

    call_command('create_test_users', password='local-test-password')
    count_after_first_run = Gerente.objects.count()
    call_command('create_test_users', password='local-test-password')

    assert Gerente.objects.count() == count_after_first_run


@pytest.mark.django_db
def test_create_test_users_command_requires_password():
    from django.core.management import call_command
    from django.core.management.base import CommandError

    with pytest.raises(CommandError):
        call_command('create_test_users')


@pytest.mark.django_db
def test_colaborador_creation():
    colaborador = Colaborador.objects.create(
        nome='Test Colaborador',
        sobrenome='Example',
        setor='TI',
        cpf='12345678900'
    )
    assert colaborador.id is not None
    assert colaborador.nome == 'Test Colaborador'
    assert colaborador.sobrenome == 'Example'
    assert colaborador.setor == 'TI'
    assert colaborador.cpf == '12345678900'
