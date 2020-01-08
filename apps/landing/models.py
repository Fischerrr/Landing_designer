import os
import re

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django_ymap.fields import YmapCoord
from ckeditor.fields import RichTextField
from versatileimagefield.fields import VersatileImageField

from apps.landing import constant


def svg_validator(file):
    _, exn = os.path.splitext(file.name)
    if exn != '.svg':
        raise ValidationError('Файл не является SVG')


def pdf_validator(file):
    _, exn = os.path.splitext(file.name)
    if exn != '.pdf':
        raise ValidationError('Файл не является PDF')


class Enabled(models.Model):
    enabled = models.BooleanField(default=False, db_index=True, verbose_name='Включен')

    class Meta:
        abstract = True


class Text2BlockAbstract(models.Model):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    description = RichTextField(max_length=1500, blank=True, null=True,
                                help_text='Максимальное количество символов 1500', verbose_name='Описание')
    image = VersatileImageField(upload_to='landing/block/', blank=True, null=True, verbose_name='Изображение')
    svg = models.FileField(upload_to='landing/block/svg/', validators=[svg_validator], blank=True, null=True,
                           verbose_name='SVG изображение')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')
    column_number = models.PositiveSmallIntegerField(choices=constant.COLUMN_NUMBER, default=1, db_index=True,
                                                     verbose_name='Номер колонки')

    class Meta:
        abstract = True


class Block(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название блока')
    template = models.PositiveSmallIntegerField(choices=constant.BLOCK_TEMPLATE_CHOICE, db_index=True,
                                                verbose_name='Шаблон для блока')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='Подзаголовок')
    description = RichTextField(max_length=1500, blank=True, null=True, help_text='Максимальное количество символов 1500',
                                verbose_name='Описание')
    svg_background = models.FileField(upload_to='landing/block/svg/', validators=[svg_validator], blank=True, null=True,
                                      verbose_name='SVG изображение заднего фона')
    catalog = models.ManyToManyField('landing.Catalog', blank=True, null=True, verbose_name='Каталог')
    text_button = models.CharField(max_length=255, blank=True, null=True, verbose_name='Текст для кнопки')
    catalog_file = models.FileField(upload_to='landing/block/file/', blank=True, null=True,
                                    help_text='Рекомендуется загружать PDF файлы', verbose_name='Файл каталога')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Блок'
        verbose_name = 'Блок'


class Text2Block(Text2BlockAbstract):
    title_hide_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок скрытого текста')
    hide_text = RichTextField(max_length=1000, blank=True, null=True, verbose_name='Скрытый текст')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Текст для блока'
        verbose_name = 'Текст для блока'


class Comments2Block(Text2BlockAbstract):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    post = models.CharField(max_length=255, blank=True, null=True, verbose_name='Должность')
    company = models.CharField(max_length=255, blank=True, null=True, verbose_name='Компания')

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Комментарии для блока'
        verbose_name = 'Комментарий для блока'


class Gallery2Block(models.Model):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, blank=True, null=True)
    gruop_catalog = models.ForeignKey('landing.Catalog', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Группа каталога')
    image = VersatileImageField(upload_to='landing/block/gallery/', verbose_name='Изображение')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Галерея для блока'
        verbose_name = 'Галерея для блока'


class CheckBoxForm2Block(models.Model):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name_plural = 'Чекбоксы формы'
        verbose_name = 'Чекбокс формы'


class MultiSelectsForm2Block(Enabled):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    select = models.TextField(blank=True, null=True, help_text='Перечислите построчно необходимые параметры',
                              verbose_name='Параметры для выбора')


class MonoSelectsForm2Block(Enabled):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    select = models.TextField(blank=True, null=True, help_text='Перечислите построчно необходимые параметры',
                              verbose_name='Параметры для выбора')


class SpecificationsForm2Block(Enabled):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    title_select_first = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок первого селекта')
    select_first = models.TextField(blank=True, null=True, help_text='Перечислите построчно необходимые параметры',
                                    verbose_name='Первый селект')
    title_select_second = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок второго селекта')
    select_second = models.TextField(blank=True, null=True, help_text='Перечислите построчно необходимые параметры',
                                     verbose_name='Второй селект')


class Landing(Enabled):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    alt_url_site = models.URLField(unique=True, blank=True, null=True, verbose_name='Альтернативный url сайта')
    block = models.ManyToManyField('landing.Block', blank=True, null=True, through='BlockToLanding')
    brand = models.ForeignKey('landing.Brand', on_delete=models.CASCADE, verbose_name='Бренд')
    type_product = models.CharField(max_length=255, verbose_name='Тип продукта')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')
    main_color = models.CharField(max_length=7, default='#f4f4f4', verbose_name='Основной цвет')
    second_color = models.CharField(max_length=7, default='#58504C', verbose_name='Второстепенный цвет')
    accent_color = models.CharField(max_length=7, default='#F95D06', verbose_name='Акцентный цвет')
    logo = models.FileField(upload_to='landing/svg/', validators=[svg_validator], blank=True, null=True,
                                    verbose_name='SVG логотип компнаии')
    logo_mobile = models.FileField(upload_to='landing/svg/', validators=[svg_validator], blank=True, null=True,
                                           verbose_name='SVG логотип компании для мобильных экранов')
    image = VersatileImageField(upload_to='landing/image/', blank=True, null=True,
                                verbose_name='Изображение приветствия')
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон')
    phone_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Подпись к телефону')
    link_privacy = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name='Ссылка для политики конфиденциальности')
    contract_offer = models.CharField(max_length=255, blank=True, null=True, verbose_name='Договор оферты')
    copyright = models.CharField(max_length=100, blank=True, null=True, verbose_name='Копирайт')
    ymap = YmapCoord(max_length=200, start_query=u'Россия', size_width=500, size_height=500, verbose_name='Карта')
    id_ym = models.CharField(max_length=20, unique=True, blank=True, null=True,
                             verbose_name='Номер счетчика яндекс метрики')
    title_seo = models.CharField(max_length=255, blank=True, null=True, verbose_name='title seo')
    description_seo = models.CharField(max_length=255, blank=True, null=True, verbose_name='description seo')

    def __str__(self):
        return self.name

    def get_landing_subdomain_url(self, request):
        return f"{self.slug}.{request.META.get('SERVER_NAME')}"

    class Meta:
        unique_together = ('brand', 'type_product',)
        verbose_name_plural = 'Лендинг'
        verbose_name = 'Лендинг'


class BlockToLanding(Enabled):
    block = models.ForeignKey('landing.Block', on_delete=models.CASCADE, verbose_name='Блок')
    landing = models.ForeignKey('landing.Landing', on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')
    name_navigation = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название пункта навигиции')
    slug_navigation = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    use_navigation = models.BooleanField(default=False, verbose_name='Включить навигацию')

    class Meta:
        ordering = ['position', 'id']
        verbose_name_plural = 'Добавление блоков'
        verbose_name = 'Добавить блок'


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['priority']
        verbose_name_plural = 'Бренды'
        verbose_name = 'Бренд'


class Catalog(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    incline_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Склоняемый заголовок для каталога')
    description = RichTextField(max_length=1500, blank=True, null=True,
                                help_text='Максимальное количество символов 1500', verbose_name='Описание')
    pdf_file = models.FileField(upload_to='landing/catalog/pdf/', validators=[pdf_validator], blank=True, null=True,
                                verbose_name='PDF файл')
    product = models.ManyToManyField('landing.ProductsCatalog', blank=True, null=True, verbose_name='Продукт')
    column_product = models.ManyToManyField('landing.SpecificationProduct', blank=True, null=True, through='ColumnToCatalog')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    def __str__(self):
        return self.name

    def get_landing_name_display(self):
        landing = Landing.objects.filter(block__catalog=self.pk).values_list('name', flat=True)
        return ', '.join(landing)

    get_landing_name_display.short_description = 'Лендинг'

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Каталог'
        verbose_name = 'Каталог'


class SpecificationProduct(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название столбца продукта')
    unit = RichTextField(max_length=255, blank=True, null=True, verbose_name='Параметр продукта')

    def __str__(self):
        return self.name

    @mark_safe
    def get_unit_display(self):
        return self.unit or ''

    get_unit_display.short_description = 'Параметр'
    get_unit_display.admin_order_field = 'unit'

    class Meta:
        verbose_name_plural = 'Основные характеристики'
        verbose_name = 'Основная характеристика'


class SpecificationProductTabs(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название столбца продукта')
    unit = RichTextField(max_length=255, blank=True, null=True, verbose_name='Параметр продукта')

    def __str__(self):
        return self.name

    @mark_safe
    def get_unit_display(self):
        return self.unit or ''

    get_unit_display.short_description = 'Параметр'
    get_unit_display.admin_order_field = 'unit'

    class Meta:
        verbose_name_plural = 'Дополнительные характеристики'
        verbose_name = 'Дополнительная характеристика'


class ColumnToCatalog(models.Model):
    catalog = models.ForeignKey('landing.Catalog', on_delete=models.CASCADE, verbose_name='Каталог')
    column = models.ForeignKey('landing.SpecificationProduct', on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')

    class Meta:
        ordering = ['position', 'id']
        verbose_name_plural = 'Добавление столбцов продуктов каталога'
        verbose_name = 'Добавить столбец продуктов каталога'


class ParamColumnProduct(models.Model):
    product = models.ForeignKey('landing.ProductsCatalog', on_delete=models.CASCADE, verbose_name='Продукт')
    column_product = models.ForeignKey('landing.SpecificationProduct', on_delete=models.CASCADE, verbose_name='Столбцы продукта')
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name='Значение параметра')

    class Meta:
        verbose_name_plural = 'Параметры колонки продукта'
        verbose_name = 'Параметр колонки продукта'


class ProductsCatalog(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    tabs = models.ManyToManyField('landing.TabsProductCatalog', verbose_name='Описание продукта')
    youtube = models.CharField(max_length=255, blank=True, null=True, verbose_name='YouTube ссылка')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')
    json_param = JSONField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def parse_id_youtube(self):
        id_youtube = ''
        if self.youtube:
            id_youtube = re.search(r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", self.youtube)
        return id_youtube.group()

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Продукты каталога'
        verbose_name = 'Продукт каталога'


class Gallery2ProductsCatalog(models.Model):
    product = models.ForeignKey('landing.ProductsCatalog', on_delete=models.CASCADE, verbose_name='Продукт')
    image = VersatileImageField(upload_to='landing/catalog/', verbose_name='Изображение')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Галерея продукта'
        verbose_name = 'Галерея продукта'


class TabsProductCatalog(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    template = models.PositiveSmallIntegerField(default=1, choices=constant.CATALOG_PRODUCT_TEMPLATE, db_index=True,
                                                verbose_name='Шаблон для параметров продукта')
    image = VersatileImageField(upload_to='landing/catalog/', blank=True, null=True, verbose_name='Изображение')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Описание продуктов каталога'
        verbose_name = 'Описание продукта каталога'


class SpecificationsTabs(models.Model):
    tabs = models.ForeignKey('landing.TabsProductCatalog', on_delete=models.CASCADE, verbose_name='Описание')
    parameter = models.ForeignKey('landing.SpecificationProductTabs', on_delete=models.CASCADE, verbose_name='Параметр')
    group_parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name='Параметр для группировки')
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name='Значение')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')

    class Meta:
        ordering = ['priority', 'id']
        verbose_name_plural = 'Параметры для описания'
        verbose_name = 'Параметр описания'
