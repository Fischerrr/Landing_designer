from django.contrib.auth import get_user_model
from django.db import models

from apps.landing import constant

TYPE_SIMPLE_FORM = (
    (constant.GREETING, 'Приветствие'),
    (constant.CATALOG, 'Каталог'),
    (constant.ADD_FORM, 'Форма дополнительных предложений'),
    (constant.PRODUCT_RANGE, 'Программа финансирования'),
    (100, 'Продукт'),
)

SETTINGS_TYPE_FORM = TYPE_SIMPLE_FORM + ((constant.FORM_SELECTION, 'Форма с характеристиками'),)


class Feedback(models.Model):
    title = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    text = models.TextField()
    email = models.EmailField()
    handled_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return self.title


class FormLandingAbstract(models.Model):
    landing = models.ForeignKey('landing.Landing', on_delete=models.CASCADE, verbose_name='Лендинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')

    class Meta:
        abstract = True


class SpecificationsFeedback2Landing(FormLandingAbstract):
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Телефон')
    select_forms = models.TextField(blank=True, null=True, verbose_name='Данные с форм выбора')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')

    def __str__(self):
        return self.landing.name

    class Meta:
        verbose_name_plural = 'Форма с характеристиками'
        verbose_name = 'Форму с характеристиками'


class SimpleFeedback2Landing(FormLandingAbstract):
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Телефон')
    checkbox_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выбранные чекбоксы')
    type_form = models.PositiveSmallIntegerField(choices=TYPE_SIMPLE_FORM, blank=True, null=True,
                                                 verbose_name='Тип формы')
    characteristic = models.TextField(blank=True, null=True, verbose_name='Характеристики')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')
    name_product = models.CharField(max_length=255, blank=True, null=True, verbose_name='Продукт')

    def __str__(self):
        return self.landing.name

    class Meta:
        verbose_name_plural = 'Формы'
        verbose_name = 'Форма'


class EmailFeedback2Landing(FormLandingAbstract):
    def __str__(self):
        return self.landing.name

    class Meta:
        verbose_name_plural = 'Форма с e-mail'
        verbose_name = 'Форма с e-mail'


class SettingsEmailFeedback(models.Model):
    email_recipient = models.EmailField(verbose_name='E-mail уведомлений')
    email_from = models.EmailField(verbose_name='E-mail исходящий')

    def __str__(self):
        return self.email_recipient

    class Meta:
        verbose_name_plural = 'Настройка отправки E-mail'
        verbose_name = 'Настройка отправки E-mail'


class ManagerEmailFeedback(models.Model):
    settings_email = models.ForeignKey('feedback.SettingsEmailFeedback', on_delete=models.CASCADE)
    landing = models.ForeignKey('landing.Landing', on_delete=models.CASCADE, verbose_name='Лендинг')
    type_form = models.PositiveSmallIntegerField(choices=SETTINGS_TYPE_FORM, verbose_name='Тип формы')
    email = models.EmailField(verbose_name='E-mail')

    class Meta:
        unique_together = ('landing', 'type_form')
        verbose_name_plural = 'Е-mail менеджеров'
        verbose_name = 'Е-mail менеджера'
