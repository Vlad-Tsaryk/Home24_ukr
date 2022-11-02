from django import forms
from .models import Service, Unit
from django.forms import modelformset_factory


class UnitModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UnitForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Unit
        fields = '__all__'


UnitFormSet = modelformset_factory(model=Unit, form=UnitForm, extra=0)


class ServiceForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    is_counter = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    unit = UnitModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Unit.objects.all(),
                                required=False)

    class Meta:
        model = Service
        fields = ['name', 'unit', 'is_counter']


ServiceFormSet = modelformset_factory(model=Service, form=ServiceForm, extra=0, can_delete=True)
