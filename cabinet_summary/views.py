from dateutil import rrule
from django.db.models import Sum, Avg, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, RedirectView
from datetime import date
from admin_apartment.models import Apartment
from admin_receipt.models import Receipt
from users.mixins import OwnerPermissionRequiredMixin


class ApartmentSummaryRedirect(OwnerPermissionRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        apartment = self.request.user.apartment_set.first()
        if apartment:
            url = reverse_lazy('cabinet_apartment_summary', kwargs={'pk': apartment.pk})
        else:
            url = reverse_lazy('cabinet_profile')
        return url


# Create your views here.
class ApartmentSummary(OwnerPermissionRequiredMixin, DetailView):
    model = Apartment
    template_name = 'cabinet_summary/apartment_summary.html'

    def get_context_data(self, **kwargs):
        context = super(ApartmentSummary, self).get_context_data(**kwargs)
        current_date = timezone.now()
        receipts_for_the_year = Receipt.objects.filter(apartment=self.object,
                                                       is_complete=True,
                                                       date__year=current_date.year).order_by()

        context['receipts_debt_by_month'] = receipts_for_the_year \
            .annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(sum=Sum('total_price'))
        context['receipts_agv_debt'] = context['receipts_debt_by_month'].aggregate(Avg('sum'))['sum__avg']

        context['year_services_outcome'] = receipts_for_the_year.prefetch_related('receiptservice_set') \
            .values('receiptservice__service__name') \
            .annotate(sum=Sum(F('receiptservice__price_unit') * F('receiptservice__consumption')))

        context['previous_month_services_outcome'] = Receipt.objects.filter(apartment=self.get_object()) \
            .filter(is_complete=True, date__year=current_date.year, date__month=current_date.month - 1).order_by() \
            .select_related('receiptservice_set') \
            .values('receiptservice__service__name') \
            .annotate(sum=Sum(F('receiptservice__price_unit') * F('receiptservice__consumption')))

        context['receipts_debt_by_month'] = list(context['receipts_debt_by_month'])
        start_day_of_current_year = current_date.date().replace(month=1, day=1)
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_day_of_current_year, count=12):
            if not any(d['month'] == dt.date() for d in context['receipts_debt_by_month']):
                context['receipts_debt_by_month'].append({'month': dt.date(), 'sum': 0})
        context['receipts_debt_by_month'] = sorted(context['receipts_debt_by_month'], key=lambda d: d['month'])
        return context
