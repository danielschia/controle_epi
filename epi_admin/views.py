from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Colaborador, Gerente, EPI, Emprestimo
from .forms import ColaboradorForm, GerenteForm, EPIForm, EmprestimoForm



# ==================== CUSTOM LOGOUT ====================
def custom_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/?logged_out=1')

# ==================== COLABORADOR ====================

class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_list.html'
    context_object_name = 'colaboradores'
    paginate_by = 10


class ColaboradorCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'epi_admin.add_colaborador'
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'epi_admin/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        messages.success(self.request, f'Colaborador {form.cleaned_data["nome"]} criado com sucesso!')
        return super().form_valid(form)


class ColaboradorUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'epi_admin.change_colaborador'
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'epi_admin/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

    def form_valid(self, form):
        messages.success(self.request, f'Colaborador {form.cleaned_data["nome"]} atualizado com sucesso!')
        return super().form_valid(form)


class ColaboradorDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_confirm_delete.html'
    success_url = reverse_lazy('colaborador_list')

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        obj = self.get_object()
        # require both ownership and delete permission
        return obj.created_by == user and user.has_perm('epi_admin.delete_colaborador')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Colaborador deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class ColaboradorDetailView(LoginRequiredMixin, DetailView):
    model = Colaborador
    template_name = 'epi_admin/colaborador_detail.html'
    context_object_name = 'colaborador'


# ==================== GERENTE ====================

class GerenteListView(LoginRequiredMixin, ListView):
    model = Gerente
    template_name = 'epi_admin/gerente_list.html'
    context_object_name = 'gerentes'
    paginate_by = 10


class GerenteCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    # Only superusers can create Gerente objects via the UI
    def test_func(self):
        return self.request.user.is_superuser
    model = Gerente
    form_class = GerenteForm
    template_name = 'epi_admin/gerente_form.html'
    success_url = reverse_lazy('gerente_list')

    def form_valid(self, form):
        messages.success(self.request, f'Gerente {form.cleaned_data["nome"]} criado com sucesso!')
        return super().form_valid(form)


class GerenteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    # Superusers can update any Gerente; regular gerentes can update only themselves
    def test_func(self):
        obj = self.get_object()
        # Allow if superuser OR if the gerente's user account matches the current user
        if self.request.user.is_superuser:
            return True
        # For non-superusers: check if obj.user exists and matches current user
        if obj.user and obj.user == self.request.user:
            return True
        return False

    model = Gerente
    form_class = GerenteForm
    template_name = 'epi_admin/gerente_form.html'
    success_url = reverse_lazy('gerente_list')

    def form_valid(self, form):
        messages.success(self.request, f'Gerente {form.cleaned_data["nome"]} atualizado com sucesso!')
        return super().form_valid(form)


class GerenteDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    # Superusers can delete any Gerente; regular gerentes can delete only themselves
    def test_func(self):
        obj = self.get_object()
        # Allow if superuser OR if the gerente's user account matches the current user
        if self.request.user.is_superuser:
            return True
        # For non-superusers: check if obj.user exists and matches current user
        if obj.user and obj.user == self.request.user:
            return True
        return False

    model = Gerente
    template_name = 'epi_admin/gerente_confirm_delete.html'
    success_url = reverse_lazy('gerente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Gerente deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class GerenteDetailView(LoginRequiredMixin, DetailView):
    model = Gerente
    template_name = 'epi_admin/gerente_detail.html'
    context_object_name = 'gerente'


# ==================== EPI ====================

class EPIListView(LoginRequiredMixin, ListView):
    model = EPI
    template_name = 'epi_admin/epi_list.html'
    context_object_name = 'epis'
    paginate_by = 10


class EPICreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'epi_admin.add_epi'
    model = EPI
    form_class = EPIForm
    template_name = 'epi_admin/epi_form.html'
    success_url = reverse_lazy('epi_list')

    def form_valid(self, form):
        messages.success(self.request, f'EPI {form.cleaned_data["nomeAparelho"]} criado com sucesso!')
        return super().form_valid(form)


class EPIUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'epi_admin.change_epi'
    model = EPI
    form_class = EPIForm
    template_name = 'epi_admin/epi_form.html'
    success_url = reverse_lazy('epi_list')

    def form_valid(self, form):
        messages.success(self.request, f'EPI {form.cleaned_data["nomeAparelho"]} atualizado com sucesso!')
        return super().form_valid(form)


class EPIDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'epi_admin.delete_epi'
    model = EPI
    template_name = 'epi_admin/epi_confirm_delete.html'
    success_url = reverse_lazy('epi_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'EPI deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class EPIDetailView(LoginRequiredMixin, DetailView):
    model = EPI
    template_name = 'epi_admin/epi_detail.html'
    context_object_name = 'epi'


# ==================== EMPRESTIMO ====================

class EmprestimoListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_list.html'
    context_object_name = 'emprestimos'
    paginate_by = 10


class EmprestimoCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'epi_admin.add_emprestimo'
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'epi_admin/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Empréstimo criado com sucesso!')
        return super().form_valid(form)


class EmprestimoUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'epi_admin.change_emprestimo'
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'epi_admin/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Empréstimo atualizado com sucesso!')
        return super().form_valid(form)


class EmprestimoDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'epi_admin.delete_emprestimo'
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_confirm_delete.html'
    success_url = reverse_lazy('emprestimo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Empréstimo deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class EmprestimoDetailView(LoginRequiredMixin, DetailView):
    model = Emprestimo
    template_name = 'epi_admin/emprestimo_detail.html'
    context_object_name = 'emprestimo'
