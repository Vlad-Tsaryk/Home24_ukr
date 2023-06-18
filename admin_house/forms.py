from django import forms
from django.forms import modelformset_factory
from PIL import Image
from .models import House, Section, Floor, HouseUser
from users.models import User, Role


class RoleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.role.role


class HouseForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(HouseForm, self).__init__(*args, **kwargs)
        self.fields["image1"].required = False
        self.fields["image1"].widget = forms.FileInput(attrs={"accept": "image/*"})
        self.fields["image2"].required = False
        self.fields["image2"].widget = forms.FileInput(attrs={"accept": "image/*"})
        self.fields["image3"].required = False
        self.fields["image3"].widget = forms.FileInput(attrs={"accept": "image/*"})
        self.fields["image4"].required = False
        self.fields["image4"].widget = forms.FileInput(attrs={"accept": "image/*"})
        self.fields["image5"].required = False
        self.fields["image5"].widget = forms.FileInput(attrs={"accept": "image/*"})

    class Meta:
        model = House
        fields = "__all__"
        exclude = ["users"]


class SectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields["house"].required = False

    class Meta:
        model = Section
        fields = "__all__"


SectionFormSet = modelformset_factory(
    model=Section, form=SectionForm, extra=0, can_delete=True
)


class FloorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(FloorForm, self).__init__(*args, **kwargs)
        self.fields["house"].required = False

    class Meta:
        model = Floor
        fields = "__all__"


FloorFormSet = modelformset_factory(
    model=Floor, form=FloorForm, extra=0, can_delete=True
)


class HouseUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=User.objects.exclude(role__role=Role.RoleName.OWNER),
        required=True,
    )
    role = RoleModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control", "disabled": ""}),
        queryset=User.objects.exclude(role__role=Role.RoleName.OWNER),
        required=False,
    )

    class Meta:
        model = HouseUser
        fields = [
            "user",
        ]
        exclude = ["role"]


HouseUserFormSet = modelformset_factory(
    model=HouseUser, form=HouseUserForm, extra=0, can_delete=True
)
