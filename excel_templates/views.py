from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

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
