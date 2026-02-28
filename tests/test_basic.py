import pytest
from epi_admin.models import Colaborador


@pytest.mark.django_db
def test_admin_login_page(client):
    resp = client.get('/admin/login/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_user(django_user_model):
    initial = django_user_model.objects.count()
    django_user_model.objects.create_user(username='testuser', email='testuser@example.com', password='pass')
    assert django_user_model.objects.count() == initial + 1


@pytest.mark.django_db
def test_create_test_users_command():
    from django.core.management import call_command
    from epi_admin.models import Gerente

    call_command('create_test_users')

    assert Gerente.objects.count() >= 2

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