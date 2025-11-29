from datetime import date
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
        label='Data de Empréstimo',
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )
    data_devolucao = forms.DateField(
        label='Registrar devolução',
        required=False,
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )
    data_prevista = forms.DateField(
        required=True,
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(format=DATE_FORMAT, attrs={'placeholder': 'DD/MM/YY', 'class': 'datepicker', 'autocomplete': 'off'})
    )
    labels = {
            'colaborador': 'Colaborador',
            'epi_nome': 'EPI',
            'data_emprestimo': 'Data de Empréstimo',
            'data_prevista': 'Data Prevista',
            'data_devolucao': 'Registrar Devolução',
            'condicao_retirada': 'Condição na Retirada',
            'condicao_devolucao': 'Condição na Devolução',
        }

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi_nome', 'data_emprestimo', 'data_prevista', 'data_devolucao', 'condicao_retirada', 'condicao_devolucao']
        labels = {
            'colaborador': 'Colaborador',
            'epi_nome': 'EPI',
            'data_emprestimo': 'Data de Empréstimo',
            'data_prevista': 'Data Prevista',
            'data_devolucao': 'Registrar Devolução',
            'condicao_retirada': 'Condição na Retirada',
            'condicao_devolucao': 'Condição na Devolução',
        }
        def clean_epi_nome(self):
            """
            Valida se o EPI selecionado tem quantidade maior que zero.
            """
            epi = self.cleaned_data.get("epi_nome")

            if epi:
                # Recarrega a instância do EPI do banco de dados para garantir a quantidade atual
                epi.refresh_from_db()

                if epi.quantidade <= 0:
                    raise forms.ValidationError(
                        f"O EPI '{epi.nomeAparelho}' está indisponível no estoque (Quantidade: {epi.quantidade})."
                    )

            return epi

    def clean(self):
        cleaned_data = super().clean()

        data_emprestimo = cleaned_data.get("data_emprestimo")
        data_prevista = cleaned_data.get("data_prevista")
        data_devolucao = cleaned_data.get("data_devolucao")


        if isinstance(data_emprestimo, date) and isinstance(data_prevista, date):
            # Agora a comparação é segura
            if data_prevista <= data_emprestimo:
                raise forms.ValidationError(
                    "A data prevista para devolução deve ser posterior à data de empréstimo."
                )

        return cleaned_data