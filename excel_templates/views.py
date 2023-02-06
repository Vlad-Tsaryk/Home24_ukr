from copy import copy, deepcopy
from datetime import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from openpyxl.reader.excel import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.cell import Cell, MergedCell

from admin_purpose.models import PaymentDetails
from admin_receipt.models import Receipt, ReceiptService
from excel_templates.models import ExcelTemplate
from .forms import ExcelTemplateCreateForm


# Create your views here.
class ExcelTemplateCreate(SuccessMessageMixin, CreateView):
    model = ExcelTemplate
    form_class = ExcelTemplateCreateForm
    template_name = 'excel_templates/excel_template_create.html'
    success_message = 'Шаблон %(name)s успешно добавлен'
    success_url = reverse_lazy('excel-template-create')

    def get_context_data(self, **kwargs):
        context = super(ExcelTemplateCreate, self).get_context_data(**kwargs)
        context['excel_template_list'] = ExcelTemplate.objects.all().order_by('-pk')
        return context


class ExcelTemplateDelete(DeleteView):
    model = ExcelTemplate

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Шаблон {obj.name} успешно удален')
        if obj.default and ExcelTemplate.objects.count() > 1:

            self.success_url = reverse_lazy('excel-template-set-default',
                                            kwargs={'pk': ExcelTemplate.objects.exclude(pk=obj.pk).last().pk})
        else:
            self.success_url = reverse_lazy('excel-template-create')
        return super(ExcelTemplateDelete, self).delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ExcelTemplateSetDefault(SingleObjectMixin, View):
    model = ExcelTemplate

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            previous_default_obj = ExcelTemplate.objects.get(default=True)
            previous_default_obj.default = False
            previous_default_obj.save()
        except:
            pass
        obj.default = True
        obj.save()
        messages.info(self.request, f'Шаблон {obj.name} задан по умолчанию')
        return redirect('excel-template-create')


class ExcelTemplatePrint(SingleObjectMixin, TemplateView):
    model = Receipt
    template_name = 'excel_templates/excel_template_print.html'

    def get_context_data(self, **kwargs):
        context = super(SingleObjectMixin, self).get_context_data(**kwargs)
        context['excel_template_list'] = ExcelTemplate.objects.all().order_by('-pk')
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        print('hello')
        excel_template = ExcelTemplate.objects.get(pk=self.request.POST.get('template_id')).file
        print(excel_template)
        print(obj)
        ru_months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                     'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        account_balance = obj.apartment.personalaccount.balance
        receipt_selectors = {
            '$payCompany$': PaymentDetails.objects.first().name,
            '$receiptAddress$': obj.address_for_excel,
            '$receiptNumber$': obj.number,
            '$accountNumber$': obj.apartment.personalaccount.number,
            '$receiptDate$': obj.date.strftime('%d.%m.%Y'),
            '$receiptMonth$': f'{ru_months[obj.date.month - 1]} {obj.date.year}',
            '$accountBalance$': account_balance,
            '$receiptPayable$': account_balance - obj.total_price,
            '$total$': obj.total_price,
        }
        receipt_services = obj.receiptservice_set.all()

        def get_receipt_service_selectors(selector, receipt_service):
            receipt_service_selectors = {
                '$serviceName$': receipt_service.service.name,
                '$servicePrice$': receipt_service.price_unit,
                '$serviceAmount$': receipt_service.consumption,
                '$serviceUnit$': receipt_service.service.unit.name,
                '$serviceTotal$': receipt_service.price_unit * receipt_service.consumption,
            }
            return receipt_service_selectors.get(selector) or selector

        wb = load_workbook(excel_template)
        ws = wb.active
        loop_coord = None
        for row in ws.iter_rows():
            for cell in row:
                val = cell.value
                if val in receipt_selectors:
                    cell.value = receipt_selectors[val]
                elif val == '$LOOP 1$':
                    loop_coord = cell.row
        aaa = ws[loop_coord + 1]
        # ws.move_range("A10:O10", rows=5, cols=1, translate=True)
        print(aaa)
        row_number = receipt_services.count()
        ws.insert_rows(loop_coord + 2, amount=row_number-1)
        cell_to_marge = None
        merged_cell = None
        print(aaa)
        ws.delete_rows(loop_coord)
        for row in range(1, row_number):
            for index, cell in enumerate(aaa):
                new_cell = ws.cell(row=cell.row + row, column=cell.column, value=cell.value)
                if cell.has_style:
                    new_cell._style = copy(cell._style)
                if isinstance(cell, MergedCell):
                    merged_cell = f'{get_column_letter(cell.column)}{cell.row + row}'
                    if index == len(aaa) - 1:
                        ws.merge_cells(f'{cell_to_marge}:{merged_cell}')
                else:
                    if cell_to_marge and merged_cell:
                        print(f'{cell_to_marge}:{merged_cell}')
                        ws.merge_cells(f'{cell_to_marge}:{merged_cell}')
                    cell_to_marge = f'{get_column_letter(cell.column)}{cell.row + row}'

        for row, receipt_service in zip(ws.iter_rows(min_row=loop_coord, max_row=loop_coord + row_number),
                                        receipt_services):
            for cell in row:
                if isinstance(cell, Cell):
                    cell.value = get_receipt_service_selectors(cell.value, receipt_service)

                # print(merged_cell.coordinate)
        # area = CellRange("A1:O1")  # area being copied
        # for row, copy_cell in zip(ws.iter_rows(min_row=15, max_col=len(aaa), max_row=15), aaa):
        #     for cell_a in row:
        #         print(copy_cell.value)
        #         cell_a = deepcopy(copy_cell)
        #         cell_a.row = 15
        #         # ws.margedcell
        #         print(cell_a)

        # def copy_cell(source_cell, coord, tgt):
        #     tgt[coord].value = source_cell.value
        #     if source_cell.has_style:
        #         tgt[coord]._style = deepcopy(source_cell._style)
        #     return tgt[coord]
        #
        # copy_cell(ws['B10'], 'A15', ws)
        # for mcr in ws.merged_cells:
        #     if mcr.coord not in area:
        #         continue
        #     print(mcr)
        #     cr = CellRange(mcr.coord)
        #     cr.shift(row_shift=10)
        #     ws.merge_cells(cr.coord)
        if loop_coord:
            a = ws[loop_coord + 1]
            # ws.insert_rows(loop_coord + 2, loop_coord + 5)
            # ws.insert_rows(10, amount=5)
            # merged_cells_range = ws.merged_cell_ranges
            # print(merged_cells_range)
            # test_merg = []
            # for marg in merged_cells_range:
            #     test_merg.append(marg.format)
            # for merged_cell in a:
            #     print(type(merged_cell))
            #     if isinstance(merged_cell, MergedCell):
            #         # if merged_cell in merged_cells_range:
            #         #     print('asdasd')
            #         print(merged_cell)
            #         print(merged_cell.column)
            #         print(merged_cell.row)
            #         copy(merged_cell)
            #         MergedCell(ws, row=merged_cell.row+5, column=merged_cell.column)
            #         print('--------------------')
            #     print(isinstance(merged_cell, MergedCell))
            #     print(merged_cell)
            #     merged_cell.shift(0, 3)
            # ws.insert_rows(loop_coord+3, 3)
            # for row in range(4):
            #     # ws.insert_rows(loop_coord + row)
            #     print('hello')
            #     for c, cell in zip(range(1, ws.max_column + 1), a):
            #         new_cell = ws.cell(row=loop_coord+row, column=c, value=cell.value)
            #         if cell.has_style:
            #             new_cell._style = copy(cell._style)
            # ws[loop_coord].append(ws[loop_coord])
            print(loop_coord)
            # ws[loop_coord + 1] = ws[loop_coord]
        response = HttpResponse(save_virtual_workbook(wb),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=receipt__{receipt_selectors["$receiptNumber$"]}_' \
                                          f'{receipt_selectors["$receiptDate$"]}.xlsx'
        print(response['Content-Disposition'])
        return response
