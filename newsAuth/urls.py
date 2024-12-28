"""
URL configuration for newsAuth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views

from newsAuth.views import  error
from register.views import registerAction
from login.views import loginAction,clear_history,index,logout,report,admin_panel,delete_report, append_report_to_csv
from Chat.views import  read_more, welcome

urlpatterns = [
    path("", index, name="index"),
    path("index/", index, name="index"),
    path('admin/', admin.site.urls),
    path('clear-history/', clear_history, name='clear_history'),
    path('login/', loginAction, name='login'),  # Use Django's built-in login view
    path('logout/', logout, name='logout'),
    path('register/', registerAction, name='register'),
    path('error/', error, name='error'),
    path('welcome/', welcome, name='welcome'),
    path('report/', report, name='report'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
    path('read_more/<int:news_id>/', read_more, name='read_more'),
    path('delete_report/<int:report_id>/', delete_report, name='delete_report'),
    path('append_report_to_csv/<int:report_id>/', append_report_to_csv, name='append_report_to_csv'),

]
