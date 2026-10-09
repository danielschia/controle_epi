from epi_admin.models import Emprestimo
from django.core.exceptions import ValidationError
from datetime import timedelta

def registrar_emprestimo(*, colaborador, epi, data_emprestimo) -> Emprestimo:
    if not colaborador.is_ativo:
        raise ValidationError(
            f"Colaborador {colaborador} está inativo enão pode registrar empréstimo."
        )

    if epi.quantidade <= 0:
        raise ValidationError(
            f"Não há unidades disponíveis do EPI {epi} para empréstimo."
        )
    
    emprestimo = Emprestimo.objects.create(
        colaborador=colaborador,
        epi_nome=epi,
        data_emprestimo=data_emprestimo,
        data_prevista=data_emprestimo + timedelta(days=7)
    )
    epi.quantidade -= 1
    epi.save()
    return emprestimo

def registrar_devolucao(*, emprestimo, data_devolucao, condicao_devolucao) -> Emprestimo:
    if data_devolucao is None:
        return emprestimo

    """Item só vale de volta se estiver em boas condições."""
    antes_credita = emprestimo.condicao_devolucao in ("BOA", "USAVEL")
    depois_credita = condicao_devolucao in ("BOA", "USAVEL")

    emprestimo.data_devolucao = data_devolucao
    emprestimo.condicao_devolucao = condicao_devolucao

    if depois_credita and not antes_credita:
        emprestimo.epi_nome.quantidade += 1
        emprestimo.epi_nome.save()
        
    emprestimo.save()
    return emprestimo

def excluir_emprestimo(*, emprestimo) -> None:
    if emprestimo.data_devolucao is None:
        emprestimo.epi_nome.quantidade += 1
        emprestimo.epi_nome.save()
    emprestimo.delete()