from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User, Role
from phonenumber_field.formfields import PhoneNumberField
from home24.settings import DATE_INPUT_FORMATS


class OwnerCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                                 , required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                                , required=False)
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                                  , required=False)
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'})
                               , required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=True)
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'})
                             , required=False)
    phone.error_messages['invalid'] = "Введите корректный номер телефона."
    # role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Role.RoleName.choices[:5]
    #                          , required=True)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=User.StatusName.choices
                               , required=True)
    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input",
               'data-target': '#reservationdate'}),
        input_formats=DATE_INPUT_FORMATS, required=False)
    viber = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'})
                             , required=False)
    viber.error_messages['invalid'] = "Введите корректный номер телефона."
    telegram = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
                               , required=False)
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '10', 'style': "height: 256px"})
        , required=False)
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}), required=False)

    role = forms.CharField(widget=forms.HiddenInput(), required=False)

    uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(OwnerCreateForm, self).__init__(*args, **kwargs)
        if not self.initial.get('uid'):
            try:
                self.initial['uid'] = str(User.get_owners().order_by('-pk').first().pk + 1).zfill(6)
            except:
                self.initial['uid'] = '1'.zfill(6)

    def clean_role(self):
        return Role.objects.get(role=Role.RoleName.OWNER)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'role', 'status',
            'username', 'password1', 'password2', 'middle_name',
            'telegram', 'viber', 'birth_date', 'notes', 'profile_image', 'uid']


class OwnerChangeForm(UserChangeForm, OwnerCreateForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'})
                                , required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'role', 'status',
            'username', 'password1', 'password2', 'middle_name',
            'telegram', 'viber', 'birth_date', 'notes', 'profile_image', 'uid']


class OwnerInviteForm(forms.Form):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380731234567'}),
                             required=False)
    phone.error_messages['invalid'] = "Введите корректный номер телефона."
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'your_email@gmail.com'}))
