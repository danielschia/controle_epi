from django import forms
from .models import EPI, Emprestimo


DATE_FORMAT = '%d/%m/%y'


class EPIForm(forms.ModelForm):
    validade = forms.DateField(
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )

    class Meta:
        model = EPI
        fields = ['nomeAparelho', 'categoria', 'quantidade', 'fotoEPI', 'validade']


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

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi_nome', 'data_emprestimo', 'data_devolucao', 'condicao_retirada', 'condicao_devolucao']
