from django import forms
from .models import Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            'code', 'name', 'capacity',
            'address', 'phone_number', 'email'
        ]


    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'
            field.widget.attrs['class'] = 'form-control mb-3 mt-2'
            field.widget.attrs['placeholder'] = f'Enter warehouse {field.label.lower()}'

            if field_name == 'address':
                field.widget.attrs['rows'] = 3

        # Prefill tanggal kontrak jika instance dan kontraknya ada
        """if instance:
            kontrak = instance.masa_kontrak.order_by('-tgl_mulai_kontrak').first()
            if kontrak:
                self.fields['tgl_mulai_kontrak'].initial = kontrak.tgl_mulai_kontrak.strftime('%d-%m-%Y')
                self.fields['tgl_akhir_kontrak'].initial = kontrak.tgl_akhir_kontrak.strftime('%d-%m-%Y')
        """

'''class SearchForm(forms.Form):
    search = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'class': 'form-control pe-5',
                'placeholder': 'Search...',
                'aria-label': 'Search',
            }
        )
    )'''

class SearchForm(forms.Form):
    search = forms.CharField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search"].widget.attrs.update({
            'class': 'form-control pe-5',
            'placeholder': 'Search...',
            'hx-get': '/warehouse/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target':'#form-area',
            'hx-include': '[name="search"]'
        })