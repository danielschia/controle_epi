from django.conf import settings
from django.db import models
from datetime import date, timedelta
from django.db.models import CheckConstraint, Q

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

    def __str__(self):
        # mostra "Colaborador - EPI" usando o nome do aparelho
        epi_nome = getattr(self.epi_nome, 'nomeAparelho', str(self.epi_nome))
        return f"{self.colaborador.nome} - {epi_nome}"

    class Meta:
        # Define a restrição que o DB irá impor
        constraints = [
            CheckConstraint(
                condition=Q(data_prevista__gt=models.F('data_emprestimo')),
                name='data_prevista_maior_que_emprestimo'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.id: # Apenas se for um novo objeto (primeiro save)
            if not self.data_prevista and self.data_emprestimo:
                self.data_prevista = self.data_emprestimo + timedelta(days=7)
        super().save(*args, **kwargs)