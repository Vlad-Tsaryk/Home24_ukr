from django import forms
from users.models import User, Role
from admin_transaction.models import Transaction
from admin_application.forms import MasterModelChoiceField
from admin_personal_account.models import PersonalAccount
from admin_purpose.models import Purpose


class TransactionForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control datetimepicker-input"})
    )
    manager = MasterModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="",
        queryset=User.objects.filter(
            role__role__in=[
                Role.RoleName.DIRECTOR,
                Role.RoleName.MANAGER,
                Role.RoleName.ACCOUNTANT,
            ]
        ),
        required=False,
    )
    owner = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="",
        queryset=User.objects.filter(role__role=Role.RoleName.OWNER),
        required=False,
    )
    personal_account = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="",
        queryset=PersonalAccount.objects.filter(apartment__isnull=False),
    )
    purpose = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="",
        queryset=None,
        required=False,
    )
    sum = forms.FloatField(
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        transaction_type = kwargs.pop("transaction_type", None)
        user_id = kwargs.pop("user_id", None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if not self.initial.get("manager"):
            self.initial["manager"] = user_id
        if not self.initial.get("number"):
            try:
                self.initial["number"] = str(Transaction.objects.first().pk + 1).zfill(
                    11
                )
            except:
                self.initial["number"] = "1".zfill(11)
        if transaction_type == "income" or self.initial.get("type"):
            self.fields["purpose"].queryset = Purpose.objects.filter(
                transaction_type=Purpose.TransactionType.INCOME
            )
            self.initial["type"] = True
        else:
            self.fields["personal_account"].required = False
            self.fields["purpose"].queryset = Purpose.objects.filter(
                transaction_type=Purpose.TransactionType.OUTCOME
            )
            self.initial["type"] = False

    def clean_type(self):
        return self.initial["type"]

    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionUpdateForm(TransactionForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if self.initial["type"]:
            self.fields["purpose"].queryset = Purpose.objects.filter(
                transaction_type=Purpose.TransactionType.INCOME
            )
