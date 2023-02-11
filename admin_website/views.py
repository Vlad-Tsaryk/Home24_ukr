from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from admin_website.forms import MainPageForm, SeoForm, BlockFormSet
from admin_website.models import MainPage
from users.mixins import RolePermissionRequiredMixin


# Create your views here.
class MainPageUpdate(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'website'
    template_name = 'admin_website/main_page.html'
    success_url = reverse_lazy('website_main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_obj = MainPage.objects.first()
        if self.request.POST:
            context['main_page_form'] = MainPageForm(self.request.POST, self.request.FILES, instance=main_page_obj,
                                                     prefix='main_page')
            context['seo_form'] = SeoForm(self.request.POST, instance=main_page_obj.seo, prefix='seo')
            context['block_formset'] = BlockFormSet(self.request.POST, self.request.FILES,
                                                    queryset=main_page_obj.block_set.all(), prefix='block')
        else:
            context['main_page_form'] = MainPageForm(instance=main_page_obj, prefix='main_page')
            context['seo_form'] = SeoForm(instance=main_page_obj.seo, prefix='seo')
            context['block_formset'] = BlockFormSet(queryset=main_page_obj.block_set.all(), prefix='block')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        main_page_form = context['main_page_form']
        seo_form = context['seo_form']
        block_formset = context['block_formset']
        if main_page_form.is_valid() and seo_form.is_valid() and block_formset.is_valid():
            seo_form.save()
            main_page_form.save()
            block_formset.save()
            return redirect(self.success_url)
        else:
            return super().render_to_response(context)
