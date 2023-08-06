=================
django-unique-audit
=================

An app that creates a unique django audit log across multiple instances.
It aims to provide consistent audit logs even on different DBs.

Quick start
-----------

1. Add "unique_audit" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'unique_audit',
    ]

2. Add django-easy-audit's middleware to your MIDDLEWARE (or MIDDLEWARE_CLASSES) setting like this::

    MIDDLEWARE = (
        ...
        'unique_audit.middleware.unique_audit.UniqueAuditMiddleware',
    )

3. Run 'python manage.py migrate unique_audit' to create the audit models.

4. That's it! Now every CRUD event on your whole project will be registered in the audit models, which you will be able to query from the Django admin app. Additionally, this app will also log all authentication events and all URLs requested.
