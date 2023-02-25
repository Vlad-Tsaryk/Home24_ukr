from django.db.models import Sum, Q, F, OuterRef, Value as V, Subquery, FloatField
from django.db.models.functions import Coalesce


class PersonalAccountBalance:

    @staticmethod
    def balance(personal_account):
        from admin_receipt.models import Receipt
        try:
            transaction_sum = personal_account.transaction_set.filter(is_complete=True) \
                                  .aggregate(Sum('sum'))['sum__sum'] or 0
            receipt_sum = personal_account.receipt_set.exclude(status=Receipt.StatusName.PAID) \
                              .filter(is_complete=True) \
                              .aggregate(total_price=Sum('total_price'))['total_price'] or 0
            print(personal_account.number, 'transaction_sum', transaction_sum, 'receipt_sum', receipt_sum, 'sum',
                  transaction_sum - receipt_sum)
            print(personal_account.receipt_set.values('total_price'))
            return transaction_sum - receipt_sum
        except:
            return 0

    @staticmethod
    def get_total_query():
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

        result = PersonalAccount.objects \
            .annotate(
            transaction_sum=Coalesce(Subquery(subquery_transaction), V(0.0)),
            receipt_sum=Coalesce(Subquery(subquery_receipt), V(0.0)),
            balance=F('transaction_sum') - F('receipt_sum'),
        ) \
            .values('number', 'balance')
        return result

    @staticmethod
    def get_total_balance():
        result = PersonalAccountBalance.get_total_query()
        return result.filter(balance__gt=0).aggregate(total=Sum('balance'))['total']

    @staticmethod
    def get_total_debt():
        result = PersonalAccountBalance.get_total_query()
        return result.filter(balance__lt=0).aggregate(total=Sum('balance'))['total']

        # print(PersonalAccount.objects.order_by('pk').annotate(
        #     transaction_sum=Sum('transaction__sum', filter=Q(transaction__is_complete=True)),
        #     receipt_sum=Sum('receipt__total_price',
        #                     filter=Q(receipt__is_complete=True) & ~Q(receipt__status=Receipt.StatusName.PAID))
        # ).annotate(
        #     balance=F('transaction_sum') - F('receipt_sum')
        # ).values('number', 'balance', 'transaction_sum', 'receipt_sum'))
        # return PersonalAccount.objects.order_by('pk').values('number') \
        #     .annotate(
        #     transaction_sum=Coalesce(Sum('transaction__sum', filter=Q(transaction__is_complete=True)), 0.0),
        #     receipt_sum=Coalesce(Sum('receipt__total_price',
        #                             filter=Q(receipt__is_complete=True) & \
        #                                    ~Q(receipt__status=Receipt.StatusName.PAID)
        #                             ), 0.0)
        # ).values('number', 'receipt_sum', 'transaction_sum')
