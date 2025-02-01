"""
URL configuration for orm_comparison project.

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
from django.urls import path, include
import django_orm.views as views
from django.contrib.auth.views import LoginView, LogoutView
import sqlalchemy_orm.views as views_sa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('sa/logout/', LogoutView.as_view(template_name='sqlalchemy_orm/logout.html'), name='sa_logout'),
    path('sa/register/', views_sa.register, name='sa_register'),
    path('sa/login/',views_sa.login, name='sa_login'),
    path('sa/tasks/', views_sa.task_list, name='sa_task_list'),
    path('sa/tasks/add/', views_sa.add_task, name='sa_add_task'),
    path('sa/tasks/<int:task_id>/toggle/', views_sa.toggle_task, name='sa_toggle_task'),
    path('sa/tasks/<int:task_id>/delete/', views_sa.delete_task, name='sa_delete_task'),
]