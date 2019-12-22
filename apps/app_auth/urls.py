from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.app_auth import views

app_name = 'app_auth'

urlpatterns = [
    path(r'^autocomplete/', staff_member_required(views.AppUserAutocomplete.as_view()), name='autocomplete'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
