import pandas as pd
import pdfkit
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from admin_receipt.models import Receipt
from excel_templates.models import ExcelTemplate
from excel_templates.views import ReceiptToExcel


# Create your views here.
class ReceiptList(ListView):
    model = Receipt
    template_name = 'cabinet_receipts/receipt_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceiptList, self).get_context_data(**kwargs)
        context['status_list'] = Receipt.StatusName.values
        return context

    def get_queryset(self):
        if self.kwargs.get('apartment_id'):
            return Receipt.objects.filter(apartment_id=self.kwargs.get('apartment_id'),
                                          apartment__owner=self.request.user)
        else:
            return Receipt.objects.filter(apartment__owner=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            # result = {}
            order_by = self.request.GET.get('order_by')
            filter_fields = {
                'status': self.request.GET.get('status'),
                'date': self.request.GET.get('date'),
            }
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 5))
            print(filter_fields)
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            # total_records = filtered_qs.count()
            # result['recordsTotal'] = total_records
            # result['recordsFiltered'] = total_records
            filtered_qs = filtered_qs
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)

            filtered_qs = filtered_qs.values('id', 'date', 'status', 'number', 'total_price')
            paginator = Paginator(filtered_qs, self.request.GET.get('length', 5))
            page = (start//length) + 1
            data = list(paginator.get_page(page))
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'draw': self.request.GET.get('draw', 1),
                'pages': paginator.num_pages,
            }
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class ReceiptView(DetailView):
    model = Receipt
    template_name = 'cabinet_receipts/receipt_view.html'


class ReceiptToPDF(SingleObjectMixin, View):
    model = Receipt

    def get(self, request, *args, **kwargs):
        ex_tmpl = ExcelTemplate.objects.get(default=True)
        response = ReceiptToExcel(receipt_object=self.get_object(),
                                  response_type='action_download',
                                  excel_template=ex_tmpl).get_excel()
        filename = ''
        content_disposition = response.get('Content-Disposition')
        if content_disposition:
            filename_pos = content_disposition.index('filename=')
            if filename_pos >= 0:
                filename = content_disposition[filename_pos + len('filename='):].strip('"')[:-5]

        df = pd.read_excel(response.content)

        columns = []
        for column in df.columns:
            if 'Unnamed' in column:
                column = ''
            columns.append(column)
        df.columns = columns
        html = df.to_html(na_rep='', index=False, border=0)
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8'
        }
        pdf_data = pdfkit.from_string(html, False, options=options)
        response = HttpResponse(pdf_data, content_type='application/pdf')
        action = self.kwargs.get('action')
        if action == 'print':
            response['Content-Disposition'] = f'inline; filename="{filename}.pdf"'
        else:
            response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        return response
