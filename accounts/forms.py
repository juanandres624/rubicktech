from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingresar Contraseña',
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Contraseña',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'password', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['type'] = 'text'
        self.fields['last_name'].widget.attrs['type'] = 'text'
        self.fields['phone_number'].widget.attrs['type'] = 'text'
        self.fields['phone_number'].widget.attrs['class'] = 'phone-inputmask'
        self.fields['phone_number'].widget.attrs['im-insert'] = 'true'
        self.fields['email'].widget.attrs['type'] = 'email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Contraseña no es igual al confirmar!'
            )