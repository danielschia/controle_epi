import pytest


@pytest.mark.django_db
def test_admin_login_page(client):
    """Admin login page should be reachable (200)."""
    resp = client.get('/admin/login/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_user(django_user_model):
    """Creating a Django user via django_user_model fixture increases count."""
    initial = django_user_model.objects.count()
    django_user_model.objects.create_user(username='testuser', email='testuser@example.com', password='pass')
    assert django_user_model.objects.count() == initial + 1


@pytest.mark.django_db
def test_create_test_users_command():
    """Running the `create_test_users` management command should create Gerente entries."""
    from django.core.management import call_command
    from epi_admin.models import Gerente

    # run the management command (idempotent)
    call_command('create_test_users')

    # seed should create at least two gerentes
    assert Gerente.objects.count() >= 2
