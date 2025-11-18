from django.contrib import admin
from .models import Colaborador, Gerente, EPI, Emprestimo


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'sobrenome', 'setor', 'cpf')
	search_fields = ('nome', 'sobrenome', 'cpf', 'setor')


@admin.register(Gerente)
class GerenteAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'sobrenome', 'setor', 'cpf')
	search_fields = ('nome', 'sobrenome', 'cpf', 'setor')


@admin.register(EPI)
class EPIAdmin(admin.ModelAdmin):
	list_display = ('id', 'nomeAparelho', 'categoria', 'quantidade', 'validade')
	search_fields = ('nomeAparelho', 'categoria')
	list_filter = ('categoria',)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
	list_display = ('id', 'colaborador', 'epi_nome', 'data_emprestimo', 'data_devolucao')
	search_fields = ('colaborador__nome', 'epi_nome__nomeAparelho')
	list_filter = ('data_emprestimo',)
