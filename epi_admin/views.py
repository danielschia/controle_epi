from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Colaborador, Gerente, EPI, Emprestimo


# ==================== COLABORADOR ====================

class ColaboradorListView(ListView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_list.html'
    context_object_name = 'colaboradores'
    paginate_by = 10


class ColaboradorCreateView(CreateView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_form.html'
    fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoColaborador']
    success_url = reverse_lazy('colaborador_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Colaborador {form.cleaned_data["nome"]} criado com sucesso!')
        return super().form_valid(form)


class ColaboradorUpdateView(UpdateView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_form.html'
    fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoColaborador']
    success_url = reverse_lazy('colaborador_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Colaborador {form.cleaned_data["nome"]} atualizado com sucesso!')
        return super().form_valid(form)


class ColaboradorDeleteView(DeleteView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_confirm_delete.html'
    success_url = reverse_lazy('colaborador_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Colaborador deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class ColaboradorDetailView(DetailView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_detail.html'
    context_object_name = 'colaborador'


# ==================== GERENTE ====================

class GerenteListView(ListView):
    model = Gerente
    template_name = 'epi_admin/gerente_list.html'
    context_object_name = 'gerentes'
    paginate_by = 10


class GerenteCreateView(CreateView):
    model = Gerente
    template_name = 'epi_admin/gerente_form.html'
    fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoGerente']
    success_url = reverse_lazy('gerente_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Gerente {form.cleaned_data["nome"]} criado com sucesso!')
        return super().form_valid(form)


class GerenteUpdateView(UpdateView):
    model = Gerente
    template_name = 'epi_admin/gerente_form.html'
    fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoGerente']
    success_url = reverse_lazy('gerente_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Gerente {form.cleaned_data["nome"]} atualizado com sucesso!')
        return super().form_valid(form)


class GerenteDeleteView(DeleteView):
    model = Gerente
    template_name = 'epi_admin/gerente_confirm_delete.html'
    success_url = reverse_lazy('gerente_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Gerente deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class GerenteDetailView(DetailView):
    model = Gerente
    template_name = 'epi_admin/gerente_detail.html'
    context_object_name = 'gerente'


# ==================== EPI ====================

class EPIListView(ListView):
    model = EPI
    template_name = 'epi_admin/epi_list.html'
    context_object_name = 'epis'
    paginate_by = 10


class EPICreateView(CreateView):
    model = EPI
    template_name = 'epi_admin/epi_form.html'
    fields = ['nomeAparelho', 'categoria', 'quantidade', 'fotoEPI', 'validade']
    success_url = reverse_lazy('epi_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'EPI {form.cleaned_data["nomeAparelho"]} criado com sucesso!')
        return super().form_valid(form)


class EPIUpdateView(UpdateView):
    model = EPI
    template_name = 'epi_admin/epi_form.html'
    fields = ['nomeAparelho', 'categoria', 'quantidade', 'fotoEPI', 'validade']
    success_url = reverse_lazy('epi_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'EPI {form.cleaned_data["nomeAparelho"]} atualizado com sucesso!')
        return super().form_valid(form)


class EPIDeleteView(DeleteView):
    model = EPI
    template_name = 'epi_admin/epi_confirm_delete.html'
    success_url = reverse_lazy('epi_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'EPI deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class EPIDetailView(DetailView):
    model = EPI
    template_name = 'epi_admin/epi_detail.html'
    context_object_name = 'epi'


# ==================== EMPRESTIMO ====================

class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_list.html'
    context_object_name = 'emprestimos'
    paginate_by = 10


class EmprestimoCreateView(CreateView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_form.html'
    fields = ['colaborador', 'epi_nome', 'data_emprestimo', 'condicao_retirada']
    success_url = reverse_lazy('emprestimo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empréstimo criado com sucesso!')
        return super().form_valid(form)


class EmprestimoUpdateView(UpdateView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_form.html'
    fields = ['colaborador', 'epi_nome', 'data_emprestimo', 'data_devolucao', 'condicao_retirada', 'condicao_devolucao']
    success_url = reverse_lazy('emprestimo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empréstimo atualizado com sucesso!')
        return super().form_valid(form)


class EmprestimoDeleteView(DeleteView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_confirm_delete.html'
    success_url = reverse_lazy('emprestimo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Empréstimo deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class EmprestimoDetailView(DetailView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_detail.html'
    context_object_name = 'emprestimo'
