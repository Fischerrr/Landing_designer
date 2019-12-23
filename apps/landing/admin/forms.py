from dal import autocomplete
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.urls import reverse

from apps.landing import models
from django import forms


# добавляем возможность редактирования М2М экземпляров
# важно, что бы у поля М2М был виджет с параметром ModelSelect2Multiple(attrs={'data-html': True})
class DalLinkM2MFieldMixin(object):
    dal_m2m_field = ''

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.dal_m2m_field:
            self.fields[self.dal_m2m_field].label_from_instance = label_from_instance


def label_from_instance(obj):
    url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])
    return f'{obj} <a class="related-widget-wrapper-link" href="{url}?_to_field=id&_popup=1" target="_blank"><img src="/static/admin/img/icon-changelink.svg" alt="Изменить"></a>'


class LandingForm(forms.ModelForm):
    def clean_slug(self):
        slug = super().clean().get('slug')
        return slug.lower()

    class Meta:
        model = models.Landing
        exclude = []
        widgets = {
            'main_color': TextInput(attrs={'type': 'color'}),
            'second_color': TextInput(attrs={'type': 'color'}),
            'accent_color': TextInput(attrs={'type': 'color'}),
        }


class BlockForm(DalLinkM2MFieldMixin, forms.ModelForm):
    dal_m2m_field = 'catalog'

    class Meta:
        model = models.Block
        exclude = []
        widgets = {
            'template': autocomplete.Select2,
            'catalog': autocomplete.ModelSelect2Multiple(attrs={'data-html': True}),
        }


class CatalogForm(DalLinkM2MFieldMixin, forms.ModelForm):
    dal_m2m_field = 'product'

    def clean_product(self):
        products = super().clean().get('product')
        name = super().clean().get('name')
        for product in products:
            catalog = models.Catalog.objects.filter(product=product).values_list('name', flat=True)
            if catalog.exists() and catalog[0] != name:
                err = ValidationError(f'Продукт "{product}"  уже используется у Каталога "{catalog[0]}"', code="invalid_utype")
                self.add_error("product", err)

        return products

    class Meta:
        model = models.Catalog
        exclude = []
        widgets = {
            'product': autocomplete.ModelSelect2Multiple(attrs={'data-html': True}),
            'catalog': autocomplete.ModelSelect2Multiple(attrs={'data-html': True}),
        }


class ProductsCatalogForm(DalLinkM2MFieldMixin, forms.ModelForm):
    dal_m2m_field = 'tabs'

    class Meta:
        model = models.ProductsCatalog
        exclude = []
        widgets = {
            'tabs': autocomplete.ModelSelect2Multiple(attrs={'data-html': True}),
        }

