from django.urls import path
from . import views

app_name="OffPcto"

urlpatterns = [
      path('',views.index,name="index"),
]