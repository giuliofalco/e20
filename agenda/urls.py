from django.urls import path
from . import views

app_name = 'agenda' 

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('edit/<int:year>/<int:month>/<int:day>/', views.day_editor, name='day_editor'),
    path('pdfs/<str:filename>', views.serve_pdf, name='serve_pdf'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('weekly_report/', views.weekly_report, name='weekly_report'),
]
