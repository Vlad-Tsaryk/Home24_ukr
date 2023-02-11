from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from admin_website.forms import MainPageForm, SeoForm, BlockFormSet, ContactPageForm, ServicePageForm, \
    ServiceBlockFormSet, TariffPageForm, TariffBlockFormSet
from admin_website.models import MainPage, ContactPage, ServicePage, TariffPage
from users.mixins import RolePermissionRequiredMixin


# Create your views here.
class MainPageUpdate(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'website'
    template_name = 'admin_website/main_page.html'
    success_url = reverse_lazy('website_main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = MainPage.objects.first()
        if self.request.POST:
            context['main_page_form'] = MainPageForm(self.request.POST, self.request.FILES, instance=self.object,
                                                     prefix='main_page')
            context['seo_form'] = SeoForm(self.request.POST, instance=self.object.seo, prefix='seo')
            context['block_formset'] = BlockFormSet(self.request.POST, queryset=self.object.block_set.all(),
                                                    prefix='block')
        else:
            context['main_page_form'] = MainPageForm(instance=self.object, prefix='main_page')
            context['seo_form'] = SeoForm(instance=self.object.seo, prefix='seo')
            context['block_formset'] = BlockFormSet(queryset=self.object.block_set.all(), prefix='block')
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


class ContactPageUpdate(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'website'
    template_name = 'admin_website/contact_page.html'
    success_url = reverse_lazy('website_contact_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = ContactPage.objects.first()
        if self.request.POST:
            context['contact_page_form'] = ContactPageForm(self.request.POST, instance=self.object,
                                                           prefix='contact_page')
            context['seo_form'] = SeoForm(self.request.POST, instance=self.object.seo, prefix='seo')
        else:
            context['contact_page_form'] = ContactPageForm(instance=self.object, prefix='contact_page')
            context['seo_form'] = SeoForm(instance=self.object.seo, prefix='seo')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_page_form = context['contact_page_form']
        seo_form = context['seo_form']
        if contact_page_form.is_valid() and seo_form.is_valid():
            contact_page_form.save()
            seo_form.save()
            return redirect(self.success_url)
        else:
            return super().render_to_response(context)


class ServicePageUpdate(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'website'
    template_name = 'admin_website/services_page.html'
    success_url = reverse_lazy('website_services_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = ServicePage.objects.first()
        if self.request.POST:
            context['services_page_form'] = ServicePageForm(self.request.POST, self.request.FILES, instance=self.object,
                                                            prefix='services_page')
            context['seo_form'] = SeoForm(self.request.POST, instance=self.object.seo, prefix='seo')
            context['service_block_formset'] = ServiceBlockFormSet(self.request.POST, self.request.FILES,
                                                                   queryset=self.object.serviceblock_set.all(),
                                                                   prefix='service_block')
        else:
            context['services_page_form'] = ServicePageForm(instance=self.object, prefix='services_page')
            context['seo_form'] = SeoForm(instance=self.object.seo, prefix='seo')
            context['service_block_formset'] = ServiceBlockFormSet(queryset=self.object.serviceblock_set.all(),
                                                                   prefix='service_block')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        services_page_form = context['services_page_form']
        seo_form = context['seo_form']
        service_block_formset = context['service_block_formset']
        if services_page_form.is_valid() and seo_form.is_valid() and service_block_formset.is_valid():
            seo_form.save()
            service_page = services_page_form.save()
            formset = service_block_formset.save(commit=False)
            for service_block in formset:
                service_block.service_page = service_page
            service_block_formset.save()
            return redirect(self.success_url)
        else:
            return super().render_to_response(context)


class TariffPageUpdate(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'website'
    template_name = 'admin_website/tariffs_page.html'
    success_url = reverse_lazy('website_tariffs_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = TariffPage.objects.first()
        if self.request.POST:
            context['tariffs_page_form'] = TariffPageForm(self.request.POST, self.request.FILES, instance=self.object,
                                                          prefix='tariffs_page')
            context['seo_form'] = SeoForm(self.request.POST, instance=self.object.seo, prefix='seo')
            context['tariff_block_formset'] = TariffBlockFormSet(self.request.POST, self.request.FILES,
                                                                 queryset=self.object.tariffblock_set.all(),
                                                                 prefix='tariff_block')
        else:
            context['tariffs_page_form'] = TariffPageForm(instance=self.object, prefix='tariffs_page')
            context['seo_form'] = SeoForm(instance=self.object.seo, prefix='seo')
            context['tariff_block_formset'] = TariffBlockFormSet(queryset=self.object.tariffblock_set.all(),
                                                                 prefix='tariff_block')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        tariffs_page_form = context['tariffs_page_form']
        seo_form = context['seo_form']
        tariff_block_formset = context['tariff_block_formset']
        if tariffs_page_form.is_valid() and seo_form.is_valid() and tariff_block_formset.is_valid():
            seo_form.save()
            tariff_page = tariffs_page_form.save()
            formset = tariff_block_formset.save(commit=False)
            for tariff_block in formset:
                tariff_block.tariff_page = tariff_page
            tariff_block_formset.save()
            return redirect(self.success_url)
        else:
            return super().render_to_response(context)
