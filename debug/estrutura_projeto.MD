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
├── nginx/
│   └── app.conf
├── static/
│   ├── css/
│   │   └── gvd-fonts.css
│   ├── fonts/
│   │   ├── Axiforma Bold.otf
│   │   ├── Axiforma Regular.otf
│   │   ├── FiraSans-Black.ttf
│   │   ├── FiraSans-BlackItalic.ttf
│   │   ├── FiraSans-Bold.ttf
│   │   ├── FiraSans-BoldItalic.ttf
│   │   ├── FiraSans-ExtraBold.ttf
│   │   ├── FiraSans-ExtraBoldItalic.ttf
│   │   ├── FiraSans-ExtraLight.ttf
│   │   ├── FiraSans-ExtraLightItalic.ttf
│   │   ├── FiraSans-Italic.ttf
│   │   ├── FiraSans-Light.ttf
│   │   ├── FiraSans-LightItalic.ttf
│   │   ├── FiraSans-Medium.ttf
│   │   ├── FiraSans-MediumItalic.ttf
│   │   ├── FiraSans-Regular.ttf
│   │   ├── FiraSans-SemiBold.ttf
│   │   ├── FiraSans-SemiBoldItalic.ttf
│   │   ├── FiraSans-Thin.ttf
│   │   └── FiraSans-ThinItalic.ttf
│   └── images/
│       ├── logo-gvd.png
│       └── logo-gvd2.png
├── staticfiles/
│   ├── admin/
│   │   ├── css/
│   │   │   ├── vendor/
│   │   │   │   └── select2/
│   │   │   │       ├── LICENSE-SELECT2.md
│   │   │   │       ├── select2.css
│   │   │   │       └── select2.min.css
│   │   │   ├── autocomplete.css
│   │   │   ├── base.css
│   │   │   ├── changelists.css
│   │   │   ├── dark_mode.css
│   │   │   ├── dashboard.css
│   │   │   ├── forms.css
│   │   │   ├── login.css
│   │   │   ├── nav_sidebar.css
│   │   │   ├── responsive.css
│   │   │   ├── responsive_rtl.css
│   │   │   ├── rtl.css
│   │   │   ├── unusable_password_field.css
│   │   │   └── widgets.css
│   │   ├── img/
│   │   │   ├── gis/
│   │   │   │   ├── move_vertex_off.svg
│   │   │   │   └── move_vertex_on.svg
│   │   │   ├── LICENSE
│   │   │   ├── README.txt
│   │   │   ├── calendar-icons.svg
│   │   │   ├── icon-addlink.svg
│   │   │   ├── icon-alert.svg
│   │   │   ├── icon-calendar.svg
│   │   │   ├── icon-changelink.svg
│   │   │   ├── icon-clock.svg
│   │   │   ├── icon-deletelink.svg
│   │   │   ├── icon-hidelink.svg
│   │   │   ├── icon-no.svg
│   │   │   ├── icon-unknown-alt.svg
│   │   │   ├── icon-unknown.svg
│   │   │   ├── icon-viewlink.svg
│   │   │   ├── icon-yes.svg
│   │   │   ├── inline-delete.svg
│   │   │   ├── search.svg
│   │   │   ├── selector-icons.svg
│   │   │   ├── sorting-icons.svg
│   │   │   ├── tooltag-add.svg
│   │   │   └── tooltag-arrowright.svg
│   │   └── js/
│   │       ├── admin/
│   │       │   ├── DateTimeShortcuts.js
│   │       │   └── RelatedObjectLookups.js
│   │       ├── vendor/
│   │       │   ├── jquery/
│   │       │   │   ├── LICENSE.txt
│   │       │   │   ├── jquery.js
│   │       │   │   └── jquery.min.js
│   │       │   ├── select2/
│   │       │   │   ├── i18n/
│   │       │   │   │   ├── af.js
│   │       │   │   │   ├── ar.js
│   │       │   │   │   ├── az.js
│   │       │   │   │   ├── bg.js
│   │       │   │   │   ├── bn.js
│   │       │   │   │   ├── bs.js
│   │       │   │   │   ├── ca.js
│   │       │   │   │   ├── cs.js
│   │       │   │   │   ├── da.js
│   │       │   │   │   ├── de.js
│   │       │   │   │   ├── dsb.js
│   │       │   │   │   ├── el.js
│   │       │   │   │   ├── en.js
│   │       │   │   │   ├── es.js
│   │       │   │   │   ├── et.js
│   │       │   │   │   ├── eu.js
│   │       │   │   │   ├── fa.js
│   │       │   │   │   ├── fi.js
│   │       │   │   │   ├── fr.js
│   │       │   │   │   ├── gl.js
│   │       │   │   │   ├── he.js
│   │       │   │   │   ├── hi.js
│   │       │   │   │   ├── hr.js
│   │       │   │   │   ├── hsb.js
│   │       │   │   │   ├── hu.js
│   │       │   │   │   ├── hy.js
│   │       │   │   │   ├── id.js
│   │       │   │   │   ├── is.js
│   │       │   │   │   ├── it.js
│   │       │   │   │   ├── ja.js
│   │       │   │   │   ├── ka.js
│   │       │   │   │   ├── km.js
│   │       │   │   │   ├── ko.js
│   │       │   │   │   ├── lt.js
│   │       │   │   │   ├── lv.js
│   │       │   │   │   ├── mk.js
│   │       │   │   │   ├── ms.js
│   │       │   │   │   ├── nb.js
│   │       │   │   │   ├── ne.js
│   │       │   │   │   ├── nl.js
│   │       │   │   │   ├── pl.js
│   │       │   │   │   ├── ps.js
│   │       │   │   │   ├── pt-BR.js
│   │       │   │   │   ├── pt.js
│   │       │   │   │   ├── ro.js
│   │       │   │   │   ├── ru.js
│   │       │   │   │   ├── sk.js
│   │       │   │   │   ├── sl.js
│   │       │   │   │   ├── sq.js
│   │       │   │   │   ├── sr-Cyrl.js
│   │       │   │   │   ├── sr.js
│   │       │   │   │   ├── sv.js
│   │       │   │   │   ├── th.js
│   │       │   │   │   ├── tk.js
│   │       │   │   │   ├── tr.js
│   │       │   │   │   ├── uk.js
│   │       │   │   │   ├── vi.js
│   │       │   │   │   ├── zh-CN.js
│   │       │   │   │   └── zh-TW.js
│   │       │   │   ├── LICENSE.md
│   │       │   │   ├── select2.full.js
│   │       │   │   └── select2.full.min.js
│   │       │   └── xregexp/
│   │       │       ├── LICENSE.txt
│   │       │       ├── xregexp.js
│   │       │       └── xregexp.min.js
│   │       ├── SelectBox.js
│   │       ├── SelectFilter2.js
│   │       ├── actions.js
│   │       ├── autocomplete.js
│   │       ├── calendar.js
│   │       ├── cancel.js
│   │       ├── change_form.js
│   │       ├── core.js
│   │       ├── filters.js
│   │       ├── inlines.js
│   │       ├── jquery.init.js
│   │       ├── nav_sidebar.js
│   │       ├── popup_response.js
│   │       ├── prepopulate.js
│   │       ├── prepopulate_init.js
│   │       ├── theme.js
│   │       ├── unusable_password_field.js
│   │       └── urlify.js
│   ├── css/
│   │   └── gvd-fonts.css
│   ├── fonts/
│   │   ├── Axiforma Bold.otf
│   │   ├── Axiforma Regular.otf
│   │   ├── FiraSans-Black.ttf
│   │   ├── FiraSans-BlackItalic.ttf
│   │   ├── FiraSans-Bold.ttf
│   │   ├── FiraSans-BoldItalic.ttf
│   │   ├── FiraSans-ExtraBold.ttf
│   │   ├── FiraSans-ExtraBoldItalic.ttf
│   │   ├── FiraSans-ExtraLight.ttf
│   │   ├── FiraSans-ExtraLightItalic.ttf
│   │   ├── FiraSans-Italic.ttf
│   │   ├── FiraSans-Light.ttf
│   │   ├── FiraSans-LightItalic.ttf
│   │   ├── FiraSans-Medium.ttf
│   │   ├── FiraSans-MediumItalic.ttf
│   │   ├── FiraSans-Regular.ttf
│   │   ├── FiraSans-SemiBold.ttf
│   │   ├── FiraSans-SemiBoldItalic.ttf
│   │   ├── FiraSans-Thin.ttf
│   │   └── FiraSans-ThinItalic.ttf
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
├── manage.py
├── migrate_responsible_data.py
├── migrate_to_responsible_model.py
├── planejamento.md
├── requirements.txt
└── setup_db.sql
