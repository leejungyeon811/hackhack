from django.urls import path
from .views import process_image, service_page, main_page

urlpatterns = [
    path('service_page/',service_page, name='service_page'),
    path('process_image/', process_image, name='process_image'),
    path('main_page/', main_page, name='main_page'),
]