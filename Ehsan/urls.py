"""Ehsan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings  
from django.conf.urls.static import static 
from router import router 
from rest_framework.authtoken import views as tokenview
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('accounts/',include('accounts.urls')),
    path('patients/',include('patients.urls')),
    #API urls
    # path("api/patients",include("patients.api.urls"))
    path('api-token-auth/', tokenview.obtain_auth_token, name='api-token-auth'),
    path("api/",include(router.urls)),
    path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("api/schema/docs/",SpectacularSwaggerView.as_view(url_name = "schema")),
    path("firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-messaging-sw.js"
    ),
    
    
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
