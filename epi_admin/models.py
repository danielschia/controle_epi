from django.conf import settings
from django.db import models
from datetime import date, timedelta
from django.db.models import CheckConstraint, Q, F
from django.core.exceptions import ValidationError

CONDICAO_CHOICES = (
    ('BOA', 'Boa'),
    ('USAVEL', 'Usável'),
    ('RUIM', 'Ruim'),
)

# Create your models here.
class Colaborador(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    setor = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11)
    fotoColaborador = models.ImageField(upload_to='static/fotos_colaboradores/', blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='colaboradores_created'
    )

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class Gerente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    setor = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11)
    fotoGerente = models.ImageField(upload_to='static/fotos_gerentes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class EPI(models.Model):
    nomeAparelho = models.CharField(max_length=50)
    categoria = models.CharField(max_length=30)
    quantidade = models.IntegerField()
    fotoEPI = models.ImageField(upload_to='static/fotos_epi/', blank=True, null=True)
    validade = models.DateField()

    def __str__(self):
        return self.nomeAparelho

class Emprestimo (models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    epi_nome = models.ForeignKey(EPI, on_delete=models.CASCADE)
    data_emprestimo = models.DateField()
    data_prevista = models.DateField(blank=True, null=True)
    data_devolucao = models.DateField("Registrar Devolução", blank=True, null=True)
    condicao_retirada = models.CharField(max_length=10,
                                        choices=CONDICAO_CHOICES,
                                        default='BOA'
                                        )
    condicao_devolucao = models.CharField(max_length=10,
                                        choices=CONDICAO_CHOICES,
                                        blank=True,
                                        null=True
                                        )

    def clean(self):
        """
        Validação de modelo para garantir estoque e datas. Chamado por full_clean().
        """
        super().clean()
        # Validação de estoque (apenas para novos registros, pois o save() gerencia updates)
        if self.epi_nome and self.epi_nome.quantidade <= 0 and not self.pk:
            raise ValidationError(
                f"Não é possível criar um empréstimo. O EPI '{self.epi_nome.nomeAparelho}' não tem estoque disponível."
            )

        # Validação de data (se a data de devolução for informada no modelo)
        if self.data_emprestimo and self.data_devolucao:
             if self.data_devolucao <= self.data_emprestimo:
                 raise ValidationError(
                    "A data de devolução deve ser posterior à data de empréstimo."
                )


    def __str__(self):
        # mostra "Colaborador - EPI" usando o nome do aparelho
        epi_nome = getattr(self.epi_nome, 'nomeAparelho', str(self.epi_nome))
        return f"{self.colaborador.nome} - {epi_nome}"

    class Meta:
        # Define a restrição que o DB irá impor para garantir a data (opcional, mas robusto)
        constraints = [
            CheckConstraint(
                condition=Q(data_prevista__gt=models.F('data_emprestimo')),
                name='data_prevista_maior_que_emprestimo'
            )
        ]

    def save(self, *args, **kwargs):
        # Chama full_clean() antes de salvar para aplicar validações do método clean()
        if not self.pk:
            self.full_clean()

        # --- Lógica de Data Prevista (Existente) ---
        if not self.pk:
            if not self.data_prevista and self.data_emprestimo:
                self.data_prevista = self.data_emprestimo + timedelta(days=7)

        # --- Lógica de Controle de Estoque (Redução e Devolução) ---

        if not self.pk:
            # 1. Verificar se é um novo empréstimo (reduzir estoque)
            # A validação de estoque já ocorreu no full_clean() acima
            self.epi_nome.quantidade = F('quantidade') - 1
            self.epi_nome.save()
        else:
            # 2. Verificar se uma devolução foi registrada (adicionar estoque de volta)
            # Carregamos a versão anterior do objeto para comparação
            try:
                old_instance = Emprestimo.objects.get(pk=self.pk)
                if not old_instance.data_devolucao and self.data_devolucao:
                    # Verifica a condição de devolução antes de adicionar
                    if self.condicao_devolucao in ['BOA', 'USAVEL']:
                        self.epi_nome.quantidade = F('quantidade') + 1
                        self.epi_nome.save()
            except Emprestimo.DoesNotExist:
                pass # Objeto novo, já tratado acima

        # Salva o objeto Emprestimo no banco de dados
        super().save(*args, **kwargs)

    # MÉTODO DELETE MOVIDO PARA O NÍVEL CORRETO DA CLASSE (FORA DO SAVE)
    def delete(self, *args, **kwargs):
        """
        Devolve um item ao estoque quando o registro de empréstimo é deletado.
        """
        epi = self.epi_nome

        if epi:
            # Usamos F() para uma atualização segura no DB
            epi.quantidade = F('quantidade') + 1
            epi.save(update_fields=['quantidade'])

        # Chama o método delete() original para finalmente excluir o objeto Emprestimo
        super().delete(*args, **kwargs)