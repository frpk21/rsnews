from django.urls import include, path

from generales.views import HomeView, HomeSinPrivilegios, PoliticaView

from django.contrib.auth import views as auth_views
 
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from noticias import views

urlpatterns = [
   # path('news/cat/<int:pk>', views.CategoriaView, name="categoria"),
    path('news/list', views.NoticiasListView.as_view(), name="noticia_list"),
    path('news/photo', views.FotosListView, name="fotos_list"),
    path('news/new', views.NoticiaNew.as_view(), name='noticia'),
    path('news/edit/<int:pk>', views.NoticiaEdit.as_view(), name='noticia_edit'),
    path('news/view/<int:pk>', views.NoticiaView.as_view(), name='noticia_view'),
    path('news/postcat/<int:pk>', views.NoticiasCategoriaView.as_view(), name='postcat_view'),
    path('news/ap/upd', views.AprobarPostAjax, name='aprobar_post'),
    path('news/ap/exp', views.InsertPostSonajero, name='insert_post'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 