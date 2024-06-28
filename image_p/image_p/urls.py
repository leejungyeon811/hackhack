
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from core import views #수정함

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
     path('', views.main_page, name='main_page'),  # 기본 페이지를 main_page로 설정
]
