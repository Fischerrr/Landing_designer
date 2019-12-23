import json
import re
from itertools import groupby
from django_ymap.admin import YmapAdmin
from django.contrib import admin

from apps.landing import models, utils, constant
from apps.landing.admin import forms


class BlockToLandingInline(admin.TabularInline):
    model = models.BlockToLanding
    prepopulated_fields = {'slug_navigation': ("name_navigation",)}
    autocomplete_fields = ['block']
    extra = 1


@admin.register(models.Landing)
class LandingAdmin(YmapAdmin, admin.ModelAdmin):
    form = forms.LandingForm
    search_fields = ['name']
    list_display = ['name', 'type_product', 'brand']
    list_filter = ('brand', 'type_product')
    autocomplete_fields = ['brand']
    change_form_template = 'admin/landing/landing/change_form.html'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['disabled_block'] = True
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [BlockToLandingInline]
        return super().change_view(request, object_id, form_url, extra_context)


class Text2BlockInline(admin.StackedInline):
    model = models.Text2Block
    extra = 1


class Comments2BlockInline(admin.StackedInline):
    model = models.Comments2Block
    extra = 1


class Gallery2BlockInline(admin.StackedInline):
    model = models.Gallery2Block
    extra = 1


class CheckBoxForm2BlockInline(admin.StackedInline):
    model = models.CheckBoxForm2Block
    max_num = 2
    extra = 2


class MultiSelectsForm2BlockInline(admin.StackedInline):
    model = models.MultiSelectsForm2Block
    max_num = 1


class SpecificationsForm2BlockInline(admin.StackedInline):
    model = models.SpecificationsForm2Block
    max_num = 1


class MonoSelectsForm2BlockInline(admin.StackedInline):
    model = models.MonoSelectsForm2Block
    max_num = 1


@admin.register(models.Block)
class BlockAdmin(admin.ModelAdmin):
    form = forms.BlockForm
    list_display = ['name']
    inlines = [
        Text2BlockInline, Comments2BlockInline, Gallery2BlockInline,
        CheckBoxForm2BlockInline, MultiSelectsForm2BlockInline, MonoSelectsForm2BlockInline,
        SpecificationsForm2BlockInline,
    ]
    search_fields = ['name']
    change_form_template = 'admin/landing/block/change_form.html'

    def _changeform_view(self, request, object_id, form_url, extra_context):
        extra_context = extra_context or {}
        extra_context['fields_dict'] = json.dumps(constant.BLOCK_FIELDS_DICT)
        return super()._changeform_view(request, object_id, form_url, extra_context)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.SpecificationProduct)
class SpecificationProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_unit_display']
    search_fields = ['name']


@admin.register(models.SpecificationProductTabs)
class SpecificationProductTabsAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_unit_display']
    search_fields = ['name']


class Gallery2GroupCatalogInlane(admin.TabularInline):
    model = models.Gallery2Block
    exclude = ['block']
    extra = 1


class ColumnToCatalogInline(admin.TabularInline):
    model = models.ColumnToCatalog
    autocomplete_fields = ['column']
    max_num = 6
    extra = 1


class CatalogToLandingFilter(admin.SimpleListFilter):
    title = 'Фильтр по лендингу'
    parameter_name = 'land'

    def lookups(self, request, model_admin):
        landing = models.Landing.objects.filter(
            block__catalog__in=models.Catalog.objects.values_list('pk', flat=True)).order_by('name').values_list('name',
                                                                                                                 'block__catalog__pk')
        group_land = groupby(landing, lambda x: x[0])
        lookups = tuple(
            ((list(val[1] for val in list_catalog_pk), land_name) for land_name, list_catalog_pk in group_land))
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pk__in=re.findall(r'\d+', self.value()))
        return queryset


@admin.register(models.Catalog)
class CatalogAdmin(admin.ModelAdmin):
    form = forms.CatalogForm
    list_display = ['name', 'get_landing_name_display']
    list_filter = [CatalogToLandingFilter]
    inlines = [Gallery2GroupCatalogInlane, ColumnToCatalogInline]

    def save_related(self, request, form, formsets, change):
        cd = super().save_related(request, form, formsets, change)
        for product in form.instance.product.all():
            utils.save_param_column_catalog(product=product)

        return cd


class Gallery2ProductsCatalogInline(admin.StackedInline):
    model = models.Gallery2ProductsCatalog
    extra = 1


class ParamColumnProductInline(admin.StackedInline):
    model = models.ParamColumnProduct
    autocomplete_fields = ['column_product']
    max_num = 6
    extra = 1


@admin.register(models.ProductsCatalog)
class ProductsCatalogAdmin(admin.ModelAdmin):
    form = forms.ProductsCatalogForm
    list_display = ['name', 'priority']
    search_fields = ['name']
    inlines = [ParamColumnProductInline, Gallery2ProductsCatalogInline]

    def save_related(self, request, form, formsets, change):
        cd = super().save_related(request, form, formsets, change)
        utils.save_param_column_catalog(product=form.instance)

        return cd


class SpecificationsTabsInline(admin.StackedInline):
    model = models.SpecificationsTabs
    autocomplete_fields = ['parameter']
    extra = 1


@admin.register(models.TabsProductCatalog)
class TabsProductCatalogAdmin(admin.ModelAdmin):
    inlines = [SpecificationsTabsInline]

