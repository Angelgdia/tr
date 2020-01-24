from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path(r'products/', views.main),
    path(r'products/manage/', views.manage),
    path(r'products/manage/create_edit/', views.create_edit),
    path(r'products/delete/', views.delete),
    path('accounts/', include('allauth.urls')),
]