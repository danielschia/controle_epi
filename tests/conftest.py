import datetime
import pytest

from epi_admin.models import Colaborador, EPI


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
