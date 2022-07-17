from django.urls import include, path
from catalogos import views
from catalogos.views import CategoriaView, CategoriaNew, CategoriaEdit, CategoriaDel,\
    SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, SubCategoriaDel


urlpatterns = [
    path('mainprod', views.MenuView, name='menu'),
    path('maininv', views.MenuInvView, name='menu_inv'),
    path('categorias', CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new', CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>', CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/delete/<int:pk>', CategoriaDel.as_view(), name='categoria_delete'),
    path('subcategorias', SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new', SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>', SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategorias/delete/<int:pk>', SubCategoriaDel.as_view(), name='subcategoria_delete'),
    path('subcategoria/', views.get_ajaxSubcategoria, name='subcategoria_select2'),
]