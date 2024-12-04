from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('<slug:slug>/', views.course_page, name='course_page'),
    path('purchase/<slug:slug>/', views.purchase_course, name='purchase_course'),
    path('full/<slug:slug>/', views.full_course_view, name='full_course'),
]
