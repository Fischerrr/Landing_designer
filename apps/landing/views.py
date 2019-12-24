from itertools import groupby
from post_office import mail
from scss.extension.core import darken, mix, rgba_
from scss.types import Color, Number

from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from apps.feedback.models import SETTINGS_TYPE_FORM
from apps.landing import models
from apps.feedback import models as models_feedback
from apps.landing import constant
from apps.landing.utils import hsl_change


# Миксин для форм feedback, с двумя функциями
# 1. Получение данных с отправленной формы
# 2. Получение email на который должна прийти информация с формы. (стандартный или менеджера)
class FeedbackInstanceMixin(object):
    def get_instance_data(self):
        data = self.request.POST
        slug = self.request.subdomain
        try:
            landing = models.Landing.objects.get(slug=slug)
        except models.Landing.DoesNotExist:
            raise Http404
        return landing, data

    def get_email_worker(self, landing, type_form):
        manager_email = models_feedback.ManagerEmailFeedback.objects.filter(landing=landing,
                                                                            type_form=type_form).values_list('email',
                                                                                                             flat=True)
        if manager_email:
            return manager_email[0]
        else:
            return models_feedback.SettingsEmailFeedback.objects.first().email_recipient


class LandingTemplate(generic.TemplateView):
    template_name = 'landing/landing.jinja'

    def get_queryset(self):
        qs = models.Landing.objects.get(slug=self.request.subdomain)
        if qs.enabled:
            return qs
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)
        landing = self.get_queryset()
        landing_offer = []

        # Так как лендинг уникален по двум полям, то можно формировать предложения других лендингов
        # и для вывода таких лендингов по бренду и продукту и делаем группировку
        group_offer = groupby(
            models.Landing.objects.select_related('brand').filter(enabled=True).order_by('brand', 'priority'),
            key=lambda x: getattr(x, 'brand'))
        for group, list_gr in group_offer:
            tuple_group = (group, list(list_gr))
            landing_offer.append(tuple_group)

        cd['object'] = landing
        cd['block_through'] = landing.blocktolanding_set.prefetch_related(
            'block__text2block_set', 'block__comments2block_set', 'block__catalog__product',
            'block__catalog__gallery2block_set',
            'block__catalog__product__tabs__specificationstabs_set__parameter',
            'block__catalog__product__gallery2productscatalog_set',
            'block__catalog__columntocatalog_set__column',
        ).select_related('block').filter(enabled=True)

        cd['landing_offer'] = landing_offer
        cd['block_template'] = constant.BLOCK_TEMPLATE
        cd['tab_image'] = constant.CATALOG_IMAGE
        cd['anchor_links'] = landing.blocktolanding_set.exclude(name_navigation__isnull=True).values_list(
            'slug_navigation', 'name_navigation')
        cd['map_coords'] = landing.ymap.split(',')

        return cd

# Формируем сolor_style.css для лендинга.
# На основе main_color, second_color и accent_color задаем цвета, для всех элементов лендинга
@method_decorator(cache_page(3600 * 24), name='dispatch')
class ColorStyle(generic.TemplateView):
    template_name = "landing/color_style.jinja"
    content_type = 'text/css'

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)
        landing = models.Landing.objects.get(slug=self.request.subdomain)
        main = Color.from_hsl(*hsl_change(Color.from_hex(landing.main_color).hsl, -0.09, 0.15))
        second = Color.from_hex(landing.second_color)
        accent = Color.from_hex(landing.accent_color)
        white = Color.from_rgb(255, 255, 255)
        color_style = {
            'main': main.render(),
            'second': second.render(),
            'accent': accent.render(),
            'form-bg': mix(white, main, Number(7, unit='%')).render(),
            'main-hover': darken(main, Number(5, unit='%')).render(),
            'map-active': rgba_(main, Number(0.7)).render(),
            'map-primary': rgba_(second, Number(0.08)).render(),
            'accent-bg': Color.from_hsl(*hsl_change(accent.hsl, 0.05, 0.48)).render(),
        }
        cd['color_style'] = color_style

        return cd


class SpecificationsFeedbackCreate(FeedbackInstanceMixin, generic.CreateView):
    model = models_feedback.SpecificationsFeedback2Landing
    fields = ['phone', 'select_forms']

    def form_valid(self, form):
        instance = form.save(commit=False)
        landing, data = self.get_instance_data()
        phone = data.get('phone')
        email = data.get('email')
        name = data.get('name')

        list_forms = []
        if data.get('multi-select'):
            list_forms.append(f"{data.get('multi-select-title') or ''}: {', '.join(data.getlist('multi-select'))}")
        if data.get('mono-select'):
            list_forms.append(f"{data.get('mono-select-title') or ''}: {data.get('mono-select') or ''}")

        select_forms = '\n\n'.join(list_forms)
        instance.select_forms = select_forms
        instance.phone = phone
        instance.email = email
        instance.name = name
        instance.landing = landing
        instance.save()

        email_worker = self.get_email_worker(landing, constant.FORM_SELECTION)
        email_from = models_feedback.SettingsEmailFeedback.objects.first().email_from
        mail.send(
            email_worker,
            email_from,
            template='manager_email',
            context={
                'landing': landing,
                'name_form': [t[1] for t in SETTINGS_TYPE_FORM if constant.FORM_SELECTION == t[0]][0],
                'email': email,
                'name': f'ФИО: {name}' if name else '',
                'form_select': select_forms if select_forms else ''

            }
        )

        return JsonResponse({'success': True}, content_type='application/json')


