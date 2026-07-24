from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from professor import views as professor_views
from usuarios import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', auth_views.login_view, name='login'),
    path('logout', auth_views.logout_view, name='logout'),
    path('registro', auth_views.registro_view, name='registro'),
    path('alterar-senha', auth_views.alterar_senha_view, name='alterar_senha'),
    path('certificados/<str:codigo>', professor_views.certificate_view, name='certificate_public'),
    path('certificados/<str:codigo>/pdf', professor_views.certificate_pdf, name='certificate_public_pdf'),
    path('', include('core.urls')),
    path('api/', include('cursos.urls')),
    path('api/', include('core.api_urls')),
    path('watch/', include('streaming.urls')),
    path('', include('guild.urls')),
    path('', include('library.urls')),
    path('', include('brain.urls')),
    path('professor/', include('professor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
