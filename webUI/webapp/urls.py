from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check-image-exists/', views.check_image_exists, name='check_image_exists'),
    path('get-counters/', views.get_counters, name='get_counters'),
]
