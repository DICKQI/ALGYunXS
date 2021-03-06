"""ALGXS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('super/', include('apps.SuperAdmin.urls', namespace='SuperAdmin')),

    path('users/', include('apps.account.urls', namespace='users')),
    path('market/', include('apps.market.urls', namespace='market')),
    path('helps/', include('apps.helps.urls', namespace='helps')),
    path('tail/', include('apps.tailwind.urls', namespace='tailwind')),
    path('ptj/', include('apps.PTJ.urls', namespace='ptj')),
    path('fq/', include('apps.FandQ.urls', namespace='FandQ')),
    path('autoAPI/', include('apps.AutoExecution.urls', namespace='AutoExecution')), # 被自动执行的API，前端人员不需要知道

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)