
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', views.main_page, name='main_page'),  # 루트 URL에 대한 패턴 추가
]
