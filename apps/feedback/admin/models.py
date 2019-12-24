from apps.feedback import models
from django.contrib import admin

from apps.feedback.admin import forms


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['title', 'phone', 'email', 'handled_by']
    list_display = ['title', 'phone', 'email']

    def get_readonly_fields(self, request, obj=None):
        return [] if request.user.is_superuser else ['title', 'phone', 'email', 'handled_by', 'text', 'created_at']

    def change_view(self, request, object_id, *args, **kwargs):
        models.Feedback.objects.filter(pk=object_id, handled_by=None).update(handled_by=request.user)
        return super(FeedbackAdmin, self).change_view(request, object_id, *args, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser


@admin.register(models.SpecificationsFeedback2Landing)
class FormSpecificationsFeedback2LandingAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'landing', 'phone', 'email']
    readonly_fields = [
        'landing', 'phone', 'email', 'name', 'select_forms', 'created_at'
    ]
    list_filter = ('landing',)


@admin.register(models.SimpleFeedback2Landing)
class FormSimpleFeedback2LandingAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'landing', 'type_form', 'phone', 'email', 'name_product', 'checkbox_text']
    readonly_fields = [
        'landing', 'type_form', 'phone', 'email', 'characteristic',
        'name', 'name_product', 'checkbox_text', 'created_at'
    ]
    list_filter = ('landing', 'type_form')
    change_form_template = 'admin/feedback/simplefeedback2landing/change_form.html'

    def _changeform_view(self, request, object_id, form_url, extra_context):
        extra_context = extra_context or {}
        extra_context['type_form_catalog'] = models.TYPE_SIMPLE_FORM[1][1]
        extra_context['type_form_add_form'] = models.TYPE_SIMPLE_FORM[2][1]
        extra_context['type_form_product'] = models.TYPE_SIMPLE_FORM[4][1]
        extra_context['type_form_part'] = models.TYPE_SIMPLE_FORM[5][1]
        return super()._changeform_view(request, object_id, form_url, extra_context)


@admin.register(models.EmailFeedback2Landing)
class FormEmailFeedback2LandingAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'landing', 'email']
    readonly_fields = ['landing', 'email', 'created_at']
    list_filter = ('landing',)


class ManagerEmailInline(admin.TabularInline):
    form = forms.ManagerEmailForm
    model = models.ManagerEmailFeedback
    autocomplete_fields = ['landing', ]
    extra = 1


@admin.register(models.SettingsEmailFeedback)
class SettingsEmailAdmin(admin.ModelAdmin):
    inlines = [ManagerEmailInline]

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(models.Feedback)
