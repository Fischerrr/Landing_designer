from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from dal import autocomplete
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic

from apps.app_auth import models


class AppUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return models.AppUser.objects.none()

        qs = models.AppUser.objects.all()

        if self.q:
            qs = qs.filter(Q(username__icontains=self.q) | Q(phone__icontains=self.q) | Q(last_name__icontains=self.q))

        return qs


@method_decorator(login_required, 'dispatch')
class Logout(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
