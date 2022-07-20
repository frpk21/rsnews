from django.urls import include, path

from generales.views import HomeView, HomeSinPrivilegios, PoliticaView

from django.contrib.auth import views as auth_views
 
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from noticias import views

urlpatterns = [
    path('news/cat/<int:pk>', views.CategoriaView, name="categoria"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 