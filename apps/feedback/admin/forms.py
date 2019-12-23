from dal import autocomplete

from apps.feedback import models
from django import forms


class ManagerEmailForm(forms.ModelForm):
    class Meta:
        model = models.ManagerEmailFeedback
        exclude = []
        widgets = {
            'type_form': autocomplete.Select2,
        }
