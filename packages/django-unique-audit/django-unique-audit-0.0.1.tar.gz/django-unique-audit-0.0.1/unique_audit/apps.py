from django.apps import AppConfig


class UniqueAuditConfig(AppConfig):
    name = 'unique_audit'
    verbose_name = 'Unique Audit Application'

    def ready(self):
        from unique_audit.signals import auth_signals, model_signals, request_signals
