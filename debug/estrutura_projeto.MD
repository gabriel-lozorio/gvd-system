# Estrutura do Projeto

├── apps/
│   ├── accounts/
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_add_responsible_name_field.py
│   │   │   ├── 0003_account_related_responsible_and_more.py
│   │   │   └── __init__.py
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
│   │   ├── urls.py
│   │   └── views.py
│   ├── categories/
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── core/
│   │   ├── templatetags/
│   │   │   ├── __init__.py
│   │   │   └── currency_filters.py
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
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   └── urls.py
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── responsibles/
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── users/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── __init__.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   ├── estrutura.md
│   ├── funcionalidades GVD 2.md
│   └── planejamento de projeto.md
├── static/
│   └── fonts/
│       ├── Axiforma Bold.otf
│       ├── Axiforma Regular.otf
│       ├── FiraSans-Black.ttf
│       ├── FiraSans-BlackItalic.ttf
│       ├── FiraSans-Bold.ttf
│       ├── FiraSans-BoldItalic.ttf
│       ├── FiraSans-ExtraBold.ttf
│       ├── FiraSans-ExtraBoldItalic.ttf
│       ├── FiraSans-ExtraLight.ttf
│       ├── FiraSans-ExtraLightItalic.ttf
│       ├── FiraSans-Italic.ttf
│       ├── FiraSans-Light.ttf
│       ├── FiraSans-LightItalic.ttf
│       ├── FiraSans-Medium.ttf
│       ├── FiraSans-MediumItalic.ttf
│       ├── FiraSans-Regular.ttf
│       ├── FiraSans-SemiBold.ttf
│       ├── FiraSans-SemiBoldItalic.ttf
│       ├── FiraSans-Thin.ttf
│       └── FiraSans-ThinItalic.ttf
├── templates/
│   ├── accounts/
│   │   ├── detail.html
│   │   ├── form.html
│   │   ├── list.html
│   │   └── payment_form_modal.html
│   ├── categories/
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── list.html
│   ├── dashboard/
│   │   ├── partials/
│   │   │   └── summary.html
│   │   └── index.html
│   ├── reports/
│   │   └── list.html
│   ├── responsibles/
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── list.html
│   ├── users/
│   │   ├── login.html
│   │   ├── password_change.html
│   │   ├── password_change_done.html
│   │   ├── password_reset.html
│   │   ├── password_reset_complete.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_done.html
│   │   ├── profile.html
│   │   └── register.html
│   └── base.html
├── comandos.md
├── create_responsibles_table.py
├── db.sqlite3
├── fix_migrations.py
├── manage.py
├── migrate_responsible_data.py
├── migrate_to_responsible_model.py
└── planejamento.md
