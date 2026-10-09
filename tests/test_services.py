import datetime
import pytest

from epi_admin.models import Colaborador, EPI
from django.core.exceptions import ValidationError

@pytest.fixture
def estoque():
    epi = EPI.objects.create(
            nomeAparelho="Capacete",
            categoria="Proteção",
            quantidade=10,
            validade=datetime.date.today() + datetime.timedelta(days=365)
        )
    return epi

@pytest.fixture
def colaborador():
    colaborador = Colaborador.objects.create(
        nome="João",
        sobrenome="Silva",
        setor="Engenharia",
        cpf="12345678901"
    )
    return colaborador

@pytest.mark.django_db
def test_registrar_emprestimo_decrementa_estoque_em_um(estoque, colaborador):
    epi = estoque
    colaborador = colaborador

    from epi_admin.services import registrar_emprestimo
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=epi,
        data_emprestimo=datetime.date.today())

    epi.refresh_from_db()
    assert epi.quantidade == 9
    assert emprestimo.data_prevista == datetime.date.today() + datetime.timedelta(days=7)

@pytest.mark.django_db
def test_devolucao_boa_devolve_item_ao_estoque(estoque, colaborador):
    epi = estoque
    colaborador = colaborador

    from epi_admin.services import registrar_emprestimo, registrar_devolucao
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=epi,
        data_emprestimo=datetime.date.today())

    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date.today(),
        condicao_devolucao="BOA"
    )
    epi.refresh_from_db()
    assert epi.quantidade == 10

@pytest.mark.django_db
def test_devolucao_ruim_nao_devolve_item_ao_estoque(estoque, colaborador):
    epi = estoque
    colaborador = colaborador

    from epi_admin.services import registrar_emprestimo, registrar_devolucao
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=epi,
        data_emprestimo=datetime.date.today())

    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date.today(),
        condicao_devolucao="RUIM"
    )
    epi.refresh_from_db()
    assert epi.quantidade == 9

@pytest.mark.django_db
def test_excluir_emprestimo_restaura_estoque(estoque, colaborador):
    from epi_admin.services import registrar_emprestimo, excluir_emprestimo
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=estoque,
        data_emprestimo=datetime.date.today())

    excluir_emprestimo(emprestimo=emprestimo)

    estoque.refresh_from_db()
    assert estoque.quantidade == 10

@pytest.mark.django_db
def test_excluir_emprestimo_devolvido_nao_credita_de_novo(estoque, colaborador):
    from epi_admin.services import registrar_emprestimo, registrar_devolucao, excluir_emprestimo
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=estoque,
        data_emprestimo=datetime.date.today())

    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date.today(),
        condicao_devolucao="BOA"
    )
    estoque.refresh_from_db()
    assert estoque.quantidade == 10

    excluir_emprestimo(emprestimo=emprestimo)

    estoque.refresh_from_db()
    assert estoque.quantidade == 10

@pytest.mark.django_db
def test_registrar_devolucao_sem_data_nao_apaga_devolucao_existente(estoque, colaborador):
    from epi_admin.services import registrar_emprestimo, registrar_devolucao
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=estoque,
        data_emprestimo=datetime.date.today())

    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date.today(),
        condicao_devolucao="BOA"
    )
    estoque.refresh_from_db()
    assert estoque.quantidade == 10

    # Tentativa de registrar devolução sem data
    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=None,
        condicao_devolucao=None
    )
    emprestimo.refresh_from_db()
    assert emprestimo.data_devolucao is not None
    assert emprestimo.condicao_devolucao == "BOA"
    estoque.refresh_from_db()
    assert estoque.quantidade == 10

@pytest.mark.django_db
def test_registrar_devolucao_nao_credita_de_novo_quando_corrige_data(estoque, colaborador):
    from epi_admin.services import registrar_emprestimo, registrar_devolucao
    emprestimo = registrar_emprestimo(
        colaborador=colaborador, epi=estoque,
        data_emprestimo=datetime.date.today()
    )

    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date(2026, 1, 18),
        condicao_devolucao="BOA"
    )

    # Corrigindo a data de devolução
    registrar_devolucao(
        emprestimo=emprestimo,
        data_devolucao=datetime.date(2026, 1, 15),
        condicao_devolucao="BOA"
    )
    estoque.refresh_from_db()
    assert estoque.quantidade == 10

@pytest.mark.django_db
def test_registrar_emprestimo_bloqueia_colaborar_inativo(estoque):
    from epi_admin.services import registrar_emprestimo
    inativo = Colaborador.objects.create(
        nome="Ana",
        sobrenome="Silva",
        setor="RH",
        cpf="123.456.789-00",
        is_ativo=False
    )
    with pytest.raises(ValidationError):
        registrar_emprestimo(
            colaborador=inativo,
            epi=estoque,
            data_emprestimo=datetime.date.today()
        )

    estoque.refresh_from_db()
    assert estoque.quantidade == 10