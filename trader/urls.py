from django.urls import path
from .views import *


urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path('marketplace/',marketplace,name="marketplace"),
    path('copyTrading/',copyTrading,name="copyTrading"),
    path('profile/',profile,name="profile"),
    path('settings/',settings,name="settings"),
    path('traderAccount/',traderAccount,name="traderAccount"),
]