from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.appointment_book, name='appointment_book'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
]
