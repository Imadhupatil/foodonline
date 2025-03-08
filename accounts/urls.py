from  django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',view=views.registerUser, name='registerUser'),
    path('myAccount/',view=views.myAccount,name='myAccount'),
    path('login/', view=views.login,name='login'),
    path('logout/',view=views.logout,name='logout'),
    path('custDashboard/',view=views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',view=views.vendorDashboard,name='vendorDashboard'),
]
