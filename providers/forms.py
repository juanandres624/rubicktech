from django import forms
from .models import Provider


class MngSelectDescription(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-select'] = value.instance.description
        return option


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = ["provider_code", "business_reason", "social_reason", "email", "phone_1", "phone_2",
                  "mngDocumentType_id", "document_number", "address_1", "address_2", "city","web_site","note"]
        widgets = {'city': MngSelectDescription, 'mngDocumentType_id': MngSelectDescription,
                   "address_1": forms.Textarea(), "address_2": forms.Textarea(), "note": forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['provider_code'].widget.attrs['type'] = 'text'
        self.fields['business_reason'].widget.attrs['type'] = 'text'
        self.fields['social_reason'].widget.attrs['type'] = 'text'
        self.fields['document_number'].widget.attrs['type'] = 'text'
        self.fields['web_site'].widget.attrs['type'] = 'text'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['phone_1'].widget.attrs['type'] = 'text'
        self.fields['phone_1'].widget.attrs['class'] = 'phone-inputmask'
        self.fields['phone_1'].widget.attrs['im-insert'] = 'true'
        self.fields['phone_2'].widget.attrs['type'] = 'text'
        self.fields['phone_2'].widget.attrs['class'] = 'phone-inputmask'
        self.fields['phone_2'].widget.attrs['im-insert'] = 'true'
        self.fields['address_1'].widget.attrs['rows'] = 3
        self.fields['address_2'].widget.attrs['rows'] = 3
        self.fields['note'].widget.attrs['rows'] = 5

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

