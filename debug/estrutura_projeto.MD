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
│   │   ├── urls.py
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
├── backups/
│   ├── backup_2025-05-04_17-12-35.sql.gz
│   └── backup_2025-05-04_17-54-22.sql.gz
├── certbot/
│   ├── conf/
│   └── www/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   └── production.py
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   ├── estrutura.md
│   ├── funcionalidades GVD 2.md
│   └── planejamento de projeto.md
├── media/
├── nginx/
│   ├── app.conf
│   └── default.conf
├── static/
│   ├── css/
│   │   └── gvd-fonts.css
│   ├── fonts/
│   │   ├── Axiforma Bold.otf
│   └── images/
│       ├── logo-gvd.png
│       └── logo-gvd2.png
├── staticfiles/
│   ├── admin/
│   │   ├── css/
│   │   │   ├── vendor/
│   ├── css/
│   │   └── gvd-fonts.css
│   ├── fonts/
│   │   ├── Axiforma Bold.otf
│   └── images/
│       ├── logo-gvd.png
│       └── logo-gvd2.png
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
├── .env
├── Dockerfile
├── comandos.md
├── create_responsibles_table.py
├── db.sqlite3
├── docker-compose.yml
├── entrypoint.sh
├── fix_migrations.py
├── get-docker.sh
├── manage.py
├── migrate_responsible_data.py
├── migrate_to_responsible_model.py
├── planejamento.md
├── requirements.txt
├── setup_db.sh
└── setup_db.sql
