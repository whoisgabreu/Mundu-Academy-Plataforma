from django.conf import settings
from django_tenants.middleware.main import TenantMainMiddleware

from tenants.models import Tenant


class TenantFallbackMiddleware(TenantMainMiddleware):
    """Fallback para um tenant padrão quando o host não possui domínio cadastrado."""

    def get_tenant(self, domain_model, hostname):
        try:
            return super().get_tenant(domain_model, hostname)
        except domain_model.DoesNotExist:
            fallback_slug = getattr(settings, 'DEFAULT_TENANT_SLUG', None)
            queryset = Tenant.objects.filter(is_active=True)
            if fallback_slug:
                queryset = queryset.filter(slug=fallback_slug)

            tenant = queryset.order_by('id').first()
            if tenant is not None:
                return tenant

            raise
