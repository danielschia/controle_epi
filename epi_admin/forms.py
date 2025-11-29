from django import forms
from .models import EPI, Emprestimo, Colaborador, Gerente


DATE_FORMAT = '%d/%m/%y'


# Widget customizado para exibir preview de imagens
class ImagePreviewWidget(forms.FileInput):
    template_name = 'widgets/image_preview.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value and hasattr(value, 'url'):
            context['widget']['image_url'] = value.url
        return context


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoColaborador']
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'setor': 'Setor',
            'cpf': 'CPF',
            'fotoColaborador': 'Foto do Colaborador',
        }
        widgets = {
            'fotoColaborador': ImagePreviewWidget(),
        }


class GerenteForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = ['nome', 'sobrenome', 'setor', 'cpf', 'fotoGerente']
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'setor': 'Setor',
            'cpf': 'CPF',
            'fotoGerente': 'Foto do Gerente',
        }
        widgets = {
            'fotoGerente': ImagePreviewWidget(),
        }


class EPIForm(forms.ModelForm):
    validade = forms.DateField(
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )

    class Meta:
        model = EPI
        fields = ['nomeAparelho', 'categoria', 'quantidade', 'fotoEPI', 'validade']
        labels = {
            'nomeAparelho': 'Nome do EPI',
            'categoria': 'Categoria',
            'quantidade': 'Quantidade',
            'fotoEPI': 'Foto do EPI',
            'validade': 'Validade',
        }
        widgets = {
            'fotoEPI': ImagePreviewWidget(),
        }


class EmprestimoForm(forms.ModelForm):
    data_emprestimo = forms.DateField(
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )
    data_devolucao = forms.DateField(
        required=False,
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )
    labels = {
            'colaborador': 'Colaborador',
            'epi_nome': 'EPI',
            'data_emprestimo': 'Data de Empréstimo',
            'data_devolucao': 'Data de Devolução',
            'condicao_retirada': 'Condição na Retirada',
            'condicao_devolucao': 'Condição na Devolução',
        }

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi_nome', 'data_emprestimo', 'data_devolucao', 'condicao_retirada', 'condicao_devolucao']
        labels = {
            'colaborador': 'Colaborador',
            'epi_nome': 'EPI',
            'data_emprestimo': 'Data de Empréstimo',
            'data_devolucao': 'Data de Devolução',
            'condicao_retirada': 'Condição na Retirada',
            'condicao_devolucao': 'Condição na Devolução',
        }
