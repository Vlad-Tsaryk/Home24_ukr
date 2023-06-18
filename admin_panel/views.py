from dateutil import rrule
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.views.generic import TemplateView

from admin_apartment.models import Apartment
from admin_application.models import Application
from admin_house.models import House
from admin_personal_account.models import PersonalAccount
from admin_personal_account.utils import PersonalAccountBalance
from admin_receipt.models import Receipt
from admin_transaction.models import Transaction
from users.mixins import AdminPermissionRequiredMixin
from users.models import User, Role
from django.utils import timezone


# Create your views here.


class StatisticView(AdminPermissionRequiredMixin, TemplateView):
    permission_required = "statistics"
    template_name = "admin_panel/statistic.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticView, self).get_context_data(**kwargs)
        context["houses_count"] = House.objects.count()
        context["apartments_count"] = Apartment.objects.count()
        context["personal_accounts_count"] = PersonalAccount.objects.count()
        context["owners_active_count"] = User.objects.filter(
            role=Role.objects.get(role=Role.RoleName.OWNER),
            status=User.StatusName.ACTIVE,
        ).count()
        context["application_in_progress"] = Application.objects.filter(
            status=Application.StatusName.IN_PROGRESS
        ).count()
        context["application_new"] = Application.objects.filter(
            status=Application.StatusName.NEW
        ).count()
        context[
            "accounts_total_debt"
        ] = PersonalAccountBalance.get_total_debt().__neg__()
        context["account_total_balance"] = PersonalAccountBalance.get_total_balance()
        context["transactions_total_balance"] = Transaction.total_balance()

        current_date = timezone.now()
        context["transactions_income"] = (
            Transaction.objects.filter(
                type=True, is_complete=True, date__year=current_date.year
            )
            .order_by()
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("sum"))
        )
        context["transactions_outcome"] = (
            Transaction.objects.filter(
                type=False, is_complete=True, date__year=current_date.year
            )
            .order_by()
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("sum"))
        )
        receipts = Receipt.objects.filter(
            date__year=current_date.year, is_complete=True
        ).order_by()
        context["receipts_debt_by_month"] = (
            receipts.exclude(status=Receipt.StatusName.PAID)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("total_price"))
        )
        context["receipts_paid_by_month"] = (
            receipts.filter(status=Receipt.StatusName.PAID)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("total_price"))
        )
        print("receipts_debt_by_month", context["receipts_debt_by_month"])
        context["transactions_income"] = list(context["transactions_income"])
        context["transactions_outcome"] = list(context["transactions_outcome"])
        context["receipts_debt_by_month"] = list(context["receipts_debt_by_month"])
        context["receipts_paid_by_month"] = list(context["receipts_paid_by_month"])
        start_day_of_current_year = current_date.date().replace(month=1, day=1)
        for dt in rrule.rrule(
            rrule.MONTHLY, dtstart=start_day_of_current_year, count=12
        ):
            if not any(d["month"] == dt.date() for d in context["transactions_income"]):
                context["transactions_income"].append({"month": dt.date(), "sum": 0})
            if not any(
                d["month"] == dt.date() for d in context["transactions_outcome"]
            ):
                context["transactions_outcome"].append({"month": dt.date(), "sum": 0})
            if not any(
                d["month"] == dt.date() for d in context["receipts_debt_by_month"]
            ):
                context["receipts_debt_by_month"].append({"month": dt.date(), "sum": 0})
            if not any(
                d["month"] == dt.date() for d in context["receipts_paid_by_month"]
            ):
                context["receipts_paid_by_month"].append({"month": dt.date(), "sum": 0})
        context["transactions_income"] = sorted(
            context["transactions_income"], key=lambda d: d["month"]
        )
        context["transactions_outcome"] = sorted(
            context["transactions_outcome"], key=lambda d: d["month"]
        )
        context["receipts_debt_by_month"] = sorted(
            context["receipts_debt_by_month"], key=lambda d: d["month"]
        )
        context["receipts_paid_by_month"] = sorted(
            context["receipts_paid_by_month"], key=lambda d: d["month"]
        )
        return context


def error_404(request, exception):
    return render(request, "admin_panel/error_404.html")


def error_403(request, exception):
    return render(request, "admin_panel/error_403.html")
