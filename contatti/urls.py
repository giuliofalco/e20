from django.urls import path
from . import views

app_name="contatti"

urlpatterns = [
      path('',views.index,name="index"),
]
