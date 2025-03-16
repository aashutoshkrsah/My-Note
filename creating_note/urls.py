"""
URL configuration for creating_note project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from base.views import home,views_note, create_note, create_notetype, view_notetype, user_login, register, user_logout
from base.views import edit_note, edit_notetype, delete_note, delete_notetype

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('views_note/', views_note, name='views_note'),
    path('create_note/', create_note, name='create_notes'),
    path('create_notetype/', create_notetype, name='create_notetype'),
    path('view_notetype/', view_notetype, name='view_notetype'),
    path('login/', user_login, name='login'),
    path('register/', register, name= 'register'),
    path('logout/', user_logout,  name= 'logout'),
    path('edit_note/<int:pk>/', edit_note,  name= 'edit_note'),
    path('delete_note/<int:pk>/', delete_note,  name= 'delete_note'),
    path('edit_notetype/<int:pk>/', edit_notetype,  name= 'edit_notetype'),
    path('delete_notetype/<int:pk>/', delete_notetype,  name= 'delete_notetype'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

