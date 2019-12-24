from django.urls import path

from apps.landing import views

app_name = 'landing'

urlpatterns = [
    path('', views.LandingTemplate.as_view(), name='landing_page'),
    path('spec/', views.SpecificationsFeedbackCreate.as_view(), name='send_form_spec'),
    path('color-style.css', views.ColorStyle.as_view(), name='color-style'),
]
