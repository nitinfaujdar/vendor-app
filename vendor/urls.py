from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorListView.as_view()),
]