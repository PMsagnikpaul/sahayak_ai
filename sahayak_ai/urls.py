"""
URL configuration for sahayak_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('create-request/', views.create_request, name='create_request'),
    path('register-volunteer/', views.register_volunteer, name='register_volunteer'),
    path('run-matching/', views.run_matching, name='run_matching'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
]
