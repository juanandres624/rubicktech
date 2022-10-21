from django import forms
from .models import Invoice,InvoiceDetail


class CustomerBillingSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = value.instance.__str__
        return option

class CustomerShippingSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = 'empty'
        return option
        
class PaymentMethodSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = 'empty'
        return option

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ["Invoice_no", "is_final_customer", "referral_guide", "payment_method", "subtotal_tax", "subtotal_0",
                  "subtotal_no_sub_taxes","subtotal_no_taxes","subtotal_discount","subtotal_ice","subtotal_tax_percentage",
                  "subtotal_tip","subtotal_gran_total","billing_customer_id","shipping_customer_id","payment_method","user","created_date"]
        widgets = {'billing_customer_id': CustomerBillingSelect, 'shipping_customer_id': CustomerShippingSelect
                    ,'payment_method': PaymentMethodSelect}

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['Invoice_no'].widget.attrs['type'] = 'text'
        self.fields['referral_guide'].widget.attrs['type'] = 'text'

        self.fields['billing_customer_id'].widget.attrs['class'] = 'select-2-billing-customer'

        self.fields['subtotal_tax'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_tax'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_0'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_0'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_no_sub_taxes'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_no_sub_taxes'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_no_taxes'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_no_taxes'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_discount'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_discount'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_tax_percentage'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_tax_percentage'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_tip'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_tip'].widget.attrs['im-insert'] = 'true'
        self.fields['subtotal_gran_total'].widget.attrs['class'] = 'percentage-inputmask'
        self.fields['subtotal_gran_total'].widget.attrs['im-insert'] = 'true'

        self.fields['is_final_customer'].widget.attrs['class'] = 'custom-control-input'
        self.fields['is_final_customer'].widget.attrs['class'] += ' is-valid'
        self.fields['is_final_customer'].widget.attrs['type'] = 'checkbox'

        self.fields['user'].widget.attrs['disabled'] = True
        self.fields['Invoice_no'].widget.attrs['readonly'] = True
        self.fields['created_date'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') != 'custom-control-input is-valid' :
                if field.widget.attrs.get('class'):
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'