from django.urls import path
from .views import SugangView, GetInfoView, StartDateView

urlpatterns = [
    path('sugang', SugangView.as_view(), name='sugang'),
    path('info', GetInfoView.as_view(), name='info'),
    path('start_date', StartDateView.as_view(), name='start_date'),
]
