# config/urls.py (atualizado)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),  # URLs de autenticação
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('categories/', include('apps.categories.urls')),
    path('reports/', include('apps.reports.urls')),  # URLs de relatórios
    path('responsibles/', include('apps.responsibles.urls')),  # URLs de responsáveis
    # Redirecionar a raiz para o dashboard
    path('', RedirectView.as_view(url='/dashboard/'), name='home'),
]

# Configuração para arquivos estáticos (apenas em desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    