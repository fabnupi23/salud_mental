"""
URL configuration for saludmental project.

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
from mentals import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('agendar/', views.agendar, name='agendar'),
    path('citas/', views.citas, name='citas'),
    path('citas_completadas/', views.citas_completadas, name='citas_completadas'),
    path('cita/<int:cita_id>/', views.cita_detail, name='cita_detail'),
    path('cita/<int:cita_id>/complete', views.complete_task, name='complete_task'),
    path('cita/<int:cita_id>/delete', views.delete_task, name='delete_task'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('recursos/', views.recursos, name='recursos'),
    path('telepsicologia/', views.telepsicologia, name='telepsicologia'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
]
