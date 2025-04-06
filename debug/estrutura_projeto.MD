# Estrutura do Projeto

├── apps/
│   ├── accounts/
│   │   ├── tests/
│   │   │   └── test_models.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   └── views.py
│   ├── categories/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   └── views.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── payments/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── services.py
│   └── __init__.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── templates/
│   ├── accounts/
│   │   ├── list.html
│   │   └── payment_form_modal.html
│   ├── dashboard/
│   │   └── index.html
│   └── base.html
├── copiar_arquivos_claude.py
├── db.sqlite3
└── manage.py
