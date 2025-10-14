from django.urls import path
from . import views

app_name = 'agenda' 

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('edit/<int:year>/<int:month>/<int:day>/', views.day_editor, name='day_editor'),
    path('pdfs/<str:filename>', views.serve_pdf, name='serve_pdf'),
    path('monthly_report/<str:utente>', views.monthly_report, name='monthly_report'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('weekly_report/<str:utente>', views.weekly_report, name='weekly_report'),
    path('redirect/<str:date_str>/', views.redirect_to_day_editor, name='redirect_to_day_editor'),
    path('genera_password/', views.genera_password, name='genera_password'),
    path('bcard/',views.bcard,name='bcard'),
    
]
