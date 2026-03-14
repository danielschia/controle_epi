import pytest
from django.core.exceptions import ValidationError

from epi_admin.models import Colaborador, Emprestimo, EPI, Gerente

@pytest.mark.django_db
def test_create_user(django_user_model: Gerente):
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

@pytest.mark.django_db
def test_cannot_create_emprestimo_for_inactive_colaborador():
    colaborador = Colaborador.objects.create(nome='Inativo', is_ativo=False, sobrenome='Colaborador', setor='TI', cpf='12345678901')
    epi = EPI.objects.create(nomeAparelho='Capacete', categoria='Proteção', quantidade=10, validade='2027-12-31')

    emprestimo = Emprestimo(colaborador=colaborador, epi_nome=epi, data_emprestimo='2026-03-14')
    with pytest.raises(ValidationError):
        # If you implemented model.full_clean/save blocking:
        emprestimo.full_clean()  # triggers model.clean() and raises ValidationError
        # or empr.save() if save() calls full_clean()