"""
URL configuration for educa project.

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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from courses import views

urlpatterns = [
    path(route='', view=views.CourseListView.as_view(), name='course_list'),
    path(route='accounts/login/', view=auth_views.LoginView.as_view(), name='login'),
    path(route='accounts/logout/', view=auth_views.LogoutView.as_view(), name='logout'),
    path(route='admin/', view=admin.site.urls),
    path(route='course/', view=include(arg='courses.urls')),
    path(route='students/', view=include(arg='students.urls')),
    path(route='chat/', view=include(arg='chat.urls', namespace='chat')),
    path(route='api/', view=include(arg='courses.api.urls', namespace='api')),
    # path(route='__debug__/', view=include(arg='debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)