from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from core.middleware import TenantFallbackMiddleware


class TenantFallbackMiddlewareTests(SimpleTestCase):
    @override_settings(DEFAULT_TENANT_SLUG='mundu')
    def test_falls_back_to_default_tenant_for_unknown_hostname(self):
        middleware = TenantFallbackMiddleware(lambda request: None)
        tenant = SimpleNamespace(slug='mundu', is_active=True)

        class DummyDomainModel:
            class DoesNotExist(Exception):
                pass

            class DummyManager:
                def select_related(self, *args, **kwargs):
                    return self

                def get(self, **kwargs):
                    raise DummyDomainModel.DoesNotExist()

            objects = DummyManager()

        class QuerysetStub:
            def __init__(self, tenant):
                self.tenant = tenant

            def filter(self, **kwargs):
                return self

            def order_by(self, *args, **kwargs):
                return self

            def first(self):
                return self.tenant

        with patch('core.middleware.Tenant.objects.filter', return_value=QuerysetStub(tenant)):
            resolved_tenant = middleware.get_tenant(DummyDomainModel, 'mundu-academy-mundu-plataforma.9qlaka.easypanel.host')

        self.assertEqual(resolved_tenant, tenant)
