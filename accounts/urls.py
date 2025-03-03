from  django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',view=views.registerUser, name='registerUser'),
]
