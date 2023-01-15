from django.db import models
from django.db.models import Count, Sum

from users.models import User
from admin_personal_account.models import PersonalAccount
from admin_purpose.models import Purpose


# Create your models here.
class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='transaction_owner')
    personal_account = models.ForeignKey(PersonalAccount, null=True, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose, null=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='manager')
    sum = models.FloatField()
    is_complete = models.BooleanField(default=True)
    date = models.DateField()
    number = models.CharField(max_length=50, unique=True)
    comment = models.TextField()
    type = models.BooleanField()

    @staticmethod
    def count_sum(queryset, transaction_type):
        result = queryset.filter(type=transaction_type, is_complete=True).aggregate(Sum('sum'))['sum__sum']
        if result:
            return result
        else:
            return 0

    @staticmethod
    def count_income(queryset):
        return Transaction.count_sum(queryset, True)

    @staticmethod
    def count_outcome(queryset):
        return Transaction.count_sum(queryset, False)

    class Meta:
        ordering = ['-pk']
