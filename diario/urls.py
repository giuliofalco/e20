from django.urls import path
from . import views

app_name="diario"

urlpatterns = [
      path('',views.index,name="index"),
      path('<int:w>',views.settimana,name="settimana"),
      path('modifica/<int:id>/<str:pasto>',views.modifica,name="modifica"),
]
