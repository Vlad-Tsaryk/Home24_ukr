from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import modelformset_factory

from .models import User, Role
from phonenumber_field.formfields import PhoneNumberField


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                                 , required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'})
                               , required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=True)
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'})
                             , required=True)
    phone.error_messages['invalid'] = "Введите корректный номер телефона."
    role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Role.RoleName.choices[:5]
                             , required=True)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=User.StatusName.choices
                               , required=True)

    def clean_role(self):
        print(self.cleaned_data['role'])
        return Role.objects.get(role=self.cleaned_data['role'])

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'role', 'status',
            'username', 'password1', 'password2']


class CustomUserUpdateForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                                 , required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'})
                               , required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=False)
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'})
                             , required=True)
    phone.error_messages['invalid'] = "Введите корректный номер телефона."

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone',
            'username', 'password1', 'password2']


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RoleForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        # self.fields['role'].required = False

    class Meta:
        model = Role
        fields = '__all__'
        exclude = ['role']


RoleFormSet = modelformset_factory(model=Role, form=RoleForm, extra=0)
