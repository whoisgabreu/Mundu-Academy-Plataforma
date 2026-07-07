from django.contrib import admin
from django.urls import path, include
from usuarios import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', auth_views.login_view, name='login'),
    path('logout', auth_views.logout_view, name='logout'),
    path('registro', auth_views.registro_view, name='registro'),
    path('', include('core.urls')),
    path('api/', include('cursos.urls')),
    path('api/', include('core.api_urls')),
    path('watch/', include('streaming.urls')),
    path('', include('guild.urls')),
    path('', include('library.urls')),
    path('', include('brain.urls')),
]
