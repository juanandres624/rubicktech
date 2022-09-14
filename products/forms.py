from django import forms
from .models import Product,Variation


class MngSelectDescription(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = value.instance.description
        return option


class ProductsForm(forms.ModelForm):

    class Meta:
        model = Product,Variation
        fields = ["product_code", "code", "product_name", "description", "price", "images",
                  "stock", ]
        widgets = {'mngProductCategory_id': MngSelectDescription, 'provider_id': MngSelectDescription}

    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['type'] = 'text'
        self.fields['last_name'].widget.attrs['type'] = 'text'
        self.fields['document_number'].widget.attrs['type'] = 'text'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['phone_1'].widget.attrs['type'] = 'text'
        self.fields['phone_1'].widget.attrs['class'] = 'phone-inputmask'
        self.fields['phone_1'].widget.attrs['im-insert'] = 'true'
        self.fields['phone_2'].widget.attrs['type'] = 'text'
        self.fields['phone_2'].widget.attrs['class'] = 'phone-inputmask'
        self.fields['phone_2'].widget.attrs['im-insert'] = 'true'
        self.fields['address'].widget.attrs['rows'] = 3
        self.fields['note'].widget.attrs['rows'] = 5

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

