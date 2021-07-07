"""majibu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

urlpatterns = [
    path('master/', admin.site.urls),
    path('', include('core.urls')),
]

handler404 = 'core.views.page_not_found'  # noqa
handler500 = 'core.views.server_side_error'  # noqa
handler403 = 'core.views.permission_denied'  # noqa
handler400 = 'core.views.bad_request'  # noqa
