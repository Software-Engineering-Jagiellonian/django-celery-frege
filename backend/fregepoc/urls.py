"""fregepoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.generic import RedirectView
from rest_framework import routers

from fregepoc.repositories.consumers import LiveStatusConsumer
from fregepoc.repositories.views import (
    RepositoryFileViewSet,
    RepositoryViewSet,
)

router = routers.DefaultRouter()
router.register("repositories", RepositoryViewSet, basename="repositories")
router.register(
    "repositoryfiles", RepositoryFileViewSet, basename="repositoryfiles"
)

urlpatterns = [
    path("", RedirectView.as_view(url='/admin')),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("ht/", include('health_check.urls')),
]

websocket_urlpatterns = [path("ws/", LiveStatusConsumer.as_asgi())]
