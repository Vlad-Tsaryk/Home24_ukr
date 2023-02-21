from django import forms
from admin_apartment.models import Apartment
from .models import Application
from users.models import User, Role


class ApartmentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.info()


class MasterModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.role} - {obj}'


class ApplicationForm(forms.ModelForm):
    master = MasterModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                    queryset=User.objects.filter(
                                        role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN]),
                                    required=False)
    owner = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                   queryset=User.objects.filter(role__role=Role.RoleName.OWNER),
                                   required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'compose-textarea form-control', 'rows': 8}),
                              required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=False)
    apartment = ApartmentModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                          queryset=Apartment.objects.all(), required=False)
    master_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=Application.MasterType.choices,
                                    required=False)
    status = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Application.StatusName.choices))
    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control"}))
    time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        try:
            if self.instance.master:
                self.initial['master_type'] = self.instance.master.role.role
                print(self.instance.master.role.role)
        except:
            pass

    class Meta:
        model = Application
        fields = ['master', 'status', 'comment', 'date', 'time',
                  'description', 'owner', 'apartment', 'master_type']
