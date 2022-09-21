from django import forms
from .models import Product,Variation
from django.forms import inlineformset_factory


class MngSelectDescription(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = value.instance.description
        return option

class MngSelectProvider(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = value.instance.__str__
        return option


class ProductsForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["product_code", "code", "product_name", "description", "price", "boughtPrice",
                  "is_discount","discountPorcentage","mngProductCategory_id","provider_id",
                  "mngProductBrand_id"]
        widgets = {'mngProductCategory_id': MngSelectDescription, 'provider_id': MngSelectProvider,
            'mngProductBrand_id': MngSelectDescription,"description": forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        self.fields['product_code'].widget.attrs['type'] = 'text'
        self.fields['code'].widget.attrs['type'] = 'text'
        self.fields['product_name'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['price'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['price'].widget.attrs['im-insert'] = 'true'
        self.fields['is_discount'].widget.attrs['class'] = 'custom-control-input'
        self.fields['is_discount'].widget.attrs['class'] += ' is-valid'
        self.fields['is_discount'].widget.attrs['type'] = 'checkbox'

 

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') != 'custom-control-input is-valid' :
                if field.widget.attrs.get('class'):
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

class VariationForm(forms.ModelForm):

    class Meta:
        model = Variation
        fields = ["variation_category", "stock"]
        # widgets = {'mngProductCategory_id': MngSelectDescription, 'provider_id': MngSelectDescription,
        #     'mngProductBrand_id': MngSelectDescription,"description": forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs['type'] = 'text'

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


