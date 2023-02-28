from django.db.models import Sum, Q, F, OuterRef, Value as V, Subquery, FloatField
from django.db.models.functions import Coalesce


class PersonalAccountBalance:

    @staticmethod
    def balance(personal_account):
        try:
            return PersonalAccountBalance.get_total_query(
                filters={'id': personal_account.pk}).aggregate(total=Sum('balance'))['total']
        except:
            return 0

    @staticmethod
    def get_total_query(filters=None):
        if filters is None:
            filters = {}
        from admin_receipt.models import Receipt, PersonalAccount
        from admin_transaction.models import Transaction
        subquery_transaction = Transaction.objects \
                                   .filter(is_complete=True, personal_account=OuterRef('pk')) \
                                   .order_by() \
                                   .values('personal_account_id') \
                                   .annotate(total_sum=Coalesce(Sum('sum'), V(0.0))) \
                                   .values('total_sum')[:1]

        subquery_receipt = Receipt.objects \
                               .filter(Q(is_complete=True, personal_account=OuterRef('pk')) &
                                       ~Q(status=Receipt.StatusName.PAID)) \
                               .order_by() \
                               .values('personal_account_id') \
                               .annotate(total_price=Coalesce(Sum('total_price'), V(0.0))) \
                               .values('total_price')[:1]

        result = PersonalAccount.objects.filter(**filters) \
            .annotate(
            transaction_sum=Coalesce(Subquery(subquery_transaction), V(0.0)),
            receipt_sum=Coalesce(Subquery(subquery_receipt), V(0.0)),
            balance=F('transaction_sum') - F('receipt_sum'),
        )
        return result

    @staticmethod
    def get_total_balance():
        result = PersonalAccountBalance.get_total_query()
        return result.filter(balance__gt=0).aggregate(total=Sum('balance'))['total'] or 0

    @staticmethod
    def get_total_debt():
        result = PersonalAccountBalance.get_total_query()
        return result.filter(balance__lt=0).aggregate(total=Sum('balance'))['total'] or 0
