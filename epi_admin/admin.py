from django.contrib import admin as django_admin
from controle_epi.admin_site import admin_site
from .models import Colaborador, Gerente, EPI, Emprestimo


class ColaboradorAdmin(django_admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'setor', 'cpf')
    search_fields = ('nome', 'sobrenome', 'cpf', 'setor')


class GerenteAdmin(django_admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'setor', 'cpf')
    search_fields = ('nome', 'sobrenome', 'cpf', 'setor')


class EPIAdmin(django_admin.ModelAdmin):
    list_display = ('id', 'nomeAparelho', 'categoria', 'quantidade', 'validade')
    search_fields = ('nomeAparelho', 'categoria')
    list_filter = ('categoria',)


class EmprestimoAdmin(django_admin.ModelAdmin):
    list_display = ('id', 'colaborador', 'epi_nome', 'data_emprestimo', 'data_devolucao')
    search_fields = ('colaborador__nome', 'epi_nome__nomeAparelho')
    list_filter = ('data_emprestimo', 'data_devolucao', 'data_prevista',)


# Register models with the custom admin site (so only superusers can access it)
admin_site.register(Colaborador, ColaboradorAdmin)
admin_site.register(Gerente, GerenteAdmin)
admin_site.register(EPI, EPIAdmin)
admin_site.register(Emprestimo, EmprestimoAdmin)
