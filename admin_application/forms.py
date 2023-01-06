from django import forms
from admin_apartment.models import Apartment
from .models import Application
from users.models import User, Role


class ApplicationForm(forms.ModelForm):
    master = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                    queryset=User.objects.filter(
                                        role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN]),
                                    required=False)
    owner = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                   queryset=User.objects.filter(role__role=Role.RoleName.OWNER),
                                   required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'compose-textarea form-control', 'rows': 8}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}))
    apartment = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                       queryset=Apartment.objects.all(), required=False)
    master_types = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                          empty_label='Любой специалист', queryset=Role.objects.filter(
                                              role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN]),
                                          required=False)
    status = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Application.StatusName.choices))
    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input",
               'data-target': '#date_input'}))
    time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': "form-control timepicker-input",
               'data-target': '#time_input'}))

    class Meta:
        model = Application
        fields = ['master', 'status', 'comment', 'date', 'time',
                  'description', 'owner', 'apartment']
