import datetime

import pytest

from epi_admin.models import Colaborador


@pytest.mark.django_db
def test_deletar_colaborador_com_emprestimo_registrado_e_bloqueado(estoque, colaborador):
    from django.db.models import ProtectedError

    from epi_admin.services import registrar_emprestimo

    registrar_emprestimo(colaborador=colaborador, epi=estoque,
                         data_emprestimo=datetime.date.today())

    with pytest.raises(ProtectedError):
        colaborador.delete()

@pytest.mark.django_db
def test_view_delete_colaborador_bloqueado_mostra_mensagem(client, django_user_model, estoque, colaborador):
    from epi_admin.services import registrar_emprestimo
    registrar_emprestimo(colaborador=colaborador, epi=estoque,
                         data_emprestimo=datetime.date.today())

    user = django_user_model.objects.create_user(username="admin", password="Abcdef123!")
    user.is_superuser = True
    user.save()
    client.force_login(user)

    resp = client.post(f"/epi_admin/colaboradores/{colaborador.pk}/deletar/")

    assert resp.status_code == 302
    assert Colaborador.objects.filter(pk=colaborador.pk).exists()

@pytest.mark.django_db
def test_view_editar_emprestimo_com_devolucao_restaura_estoque(client, django_user_model, estoque, colaborador):
    from epi_admin.services import registrar_emprestimo

    emprestimo = registrar_emprestimo(colaborador=colaborador, epi=estoque,
                                      data_emprestimo=datetime.date.today())
    estoque.refresh_from_db()
    assert estoque.quantidade == 9

    user = django_user_model.objects.create_user(username="admin", password="Abcdef123!")
    user.is_superuser = True
    user.save()
    client.force_login(user)

    hoje = datetime.date.today()
    resp = client.post(
        f"/epi_admin/emprestimos/{emprestimo.pk}/editar/",
        data={
            "colaborador": colaborador.pk,
            "epi_nome": estoque.pk,
            "data_emprestimo": hoje.strftime("%d/%m/%y"),
            "data_prevista": (hoje + datetime.timedelta(days=7)).strftime("%d/%m/%y"),
            "data_devolucao": hoje.strftime("%d/%m/%y"),
            "condicao_retirada": "BOA",
            "condicao_devolucao": "BOA",
        },
    )

    assert resp.status_code == 302
    estoque.refresh_from_db()
    assert estoque.quantidade == 10
