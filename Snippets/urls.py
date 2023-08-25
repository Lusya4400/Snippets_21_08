from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('admin/', admin.site.urls),
    path('snippets/add', views.add_snippet_page, name='snippet-add'),
    path('snippets/list', views.snippets_page, name='snippets-list'),
    path('snippet/<int:snippet_id>', views.snippet_detail, name='snippet_detail'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete, name='snippet_delete'),
    path('snippet/<int:snippet_id>/edit', views.snippet_edit, name='snippet-edit'),
    path('snippet/my', views.my_snippets, name='my-snippets'),
    path('auth/register', views.create_user, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('comment/add/<int:snippet_id>', views.comment_add, name='comment_add'),
    path('comment/<int:comment_id>/edit', views.comment_edit, name='comment_edit'),
#    path('sort_up_lang', views.sort_up_lang, name='sort_up_lang'),
#    path('snippet/create', views.create_snippet, name='create-snippet'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
