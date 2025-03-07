from django.urls import path
from .views import registerVendor
urlpatterns = [
  path('registerVendor',view=registerVendor,name='registerVendor'),
]
