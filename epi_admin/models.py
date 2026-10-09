from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, F, Q

CONDICAO_CHOICES = (
    ('BOA', 'Boa'),
    ('USAVEL', 'Usável'),
    ('RUIM', 'Ruim'),
)

class Colaborador(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    setor = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11)
    fotoColaborador = models.ImageField(upload_to='static/fotos_colaboradores/', blank=True, null=True)
    is_ativo = models.BooleanField(default=True)

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
    # email do gerente; será usado como username para login quando possível
    # email do gerente; será usado como username para login.
    # Tornaremos este campo obrigatório (não nulo) via migrações controladas.
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
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
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
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
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)