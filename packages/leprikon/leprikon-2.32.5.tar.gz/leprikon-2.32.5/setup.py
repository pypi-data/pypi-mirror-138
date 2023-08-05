# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leprikon',
 'leprikon.admin',
 'leprikon.api',
 'leprikon.cms_plugins',
 'leprikon.conf',
 'leprikon.forms',
 'leprikon.forms.reports',
 'leprikon.management',
 'leprikon.management.commands',
 'leprikon.migrations',
 'leprikon.models',
 'leprikon.search_indexes',
 'leprikon.site',
 'leprikon.templatetags',
 'leprikon.views',
 'leprikon.views.reports']

package_data = \
{'': ['*'],
 'leprikon': ['locale/cs/LC_MESSAGES/*',
              'locale/en/LC_MESSAGES/*',
              'static/*',
              'static/admin/css/*',
              'static/admin/js/admin/*',
              'static/leprikon/css/*',
              'static/leprikon/fonts/*',
              'static/leprikon/img/*',
              'static/leprikon/js/*',
              'templates/admin/*',
              'templates/admin/inc/*',
              'templates/admin/leprikon/*',
              'templates/admin/leprikon/coursediscount/*',
              'templates/admin/leprikon/donation/*',
              'templates/admin/leprikon/eventdiscount/*',
              'templates/admin/leprikon/message/*',
              'templates/admin/leprikon/messagerecipient/*',
              'templates/admin/leprikon/orderablediscount/*',
              'templates/admin/leprikon/subjectreceivedpayment/*',
              'templates/admin/leprikon/subjectreturnedpayment/*',
              'templates/auth/widgets/*',
              'templates/cms/toolbar/items/*',
              'templates/leprikon/*',
              'templates/leprikon/admin/*',
              'templates/leprikon/cms/*',
              'templates/leprikon/cms/course/*',
              'templates/leprikon/cms/course_list/*',
              'templates/leprikon/cms/event/*',
              'templates/leprikon/cms/event_list/*',
              'templates/leprikon/cms/leader/*',
              'templates/leprikon/cms/leader_list/*',
              'templates/leprikon/cms/orderable/*',
              'templates/leprikon/cms/orderable_list/*',
              'templates/leprikon/donation_pdf/*',
              'templates/leprikon/journal_journal_pdf/*',
              'templates/leprikon/received_payment_pdf/*',
              'templates/leprikon/received_payment_received/*',
              'templates/leprikon/registration_approved/*',
              'templates/leprikon/registration_canceled/*',
              'templates/leprikon/registration_payment_request/*',
              'templates/leprikon/registration_pdf/*',
              'templates/leprikon/registration_received/*',
              'templates/leprikon/registration_refund_offer/*',
              'templates/leprikon/registration_refused/*',
              'templates/leprikon/reports/*',
              'templates/leprikon/returned_payment_pdf/*',
              'templates/leprikon/returned_payment_received/*',
              'templates/leprikon/static/*',
              'templates/leprikon/widgets/*',
              'templates/rocketchat/*']}

install_requires = \
['Django<2',
 'PyICU>=2.6,<3.0',
 'PyPDF2>=1.26.0,<2.0.0',
 'Whoosh>=2.7.4,<3.0.0',
 'certbot-nginx>=1.12.0,<2.0.0',
 'certbot>=1.12.0,<2.0.0',
 'cmsplugin-filer>=1.1.3,<2.0.0',
 'django-bankreader<0.7',
 'django-cms<3.7',
 'django-countries>=7.0,<8.0',
 'django-cron>=0.5.1,<0.6.0',
 'django-excel>=0.0.10,<0.0.11',
 'django-filer<1.6',
 'django-ganalytics>=0.7.0,<0.8.0',
 'django-haystack<2.8',
 'django-localflavor<2',
 'django-mathfilters>=1.0.0,<2.0.0',
 'django-multiselectfield>=0.1.12,<0.2.0',
 'django-pays>=0.1.0,<0.2.0',
 'django-qr-code<1.3',
 'django-redis==4.11.0',
 'django-staticfiles-downloader<0.3',
 'django-template-admin>=1.1.1,<2.0.0',
 'django-user-unique-email>=0.1.1,<0.2.0',
 'django-verified-email-field>=1.7.0,<2.0.0',
 'djangocms-googlemap<1.5',
 'djangocms-link<2.7',
 'djangocms-snippet<2.4',
 'djangocms-style<2.4',
 'djangocms-text-ckeditor<4',
 'djangocms-video<2.4',
 'gunicorn>=20.1.0,<21.0.0',
 'html2rml>=0.3.0,<0.4.0',
 'ipython>=7.20.0,<8.0.0',
 'lxml>=4.6.2,<5.0.0',
 'mysqlclient<2.1',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pyexcel-xlsxw>=0.6.1,<0.7.0',
 'pymongo>=3.11.3,<4.0.0',
 'python-memcached>=1.59,<2.0',
 'requests>=2.25.1,<3.0.0',
 'rocketchat-API>=1.14.0,<2.0.0',
 'schwifty>=2021.5.2,<2022.0.0',
 'sentry-sdk>=0.19.5,<0.20.0',
 'social-auth-app-django>=4.0.0,<5.0.0',
 'sqlparse>=0.4.1,<0.5.0',
 'trml2pdf>=0.6,<0.7']

entry_points = \
{'console_scripts': ['leprikon = leprikon.__main__:main']}

setup_kwargs = {
    'name': 'leprikon',
    'version': '2.32.5',
    'description': 'Django CMS based IS for education',
    'long_description': 'Leprikón\n========\n\nLeprikón is web information system for leisure centres and other educational organizations.\n\n`www.leprikon.cz <https://www.leprikon.cz/>`__\n\n`Docker image <https://hub.docker.com/r/leprikon/leprikon/>`__\n\n\nInstallation with pip\n---------------------\n\n.. code:: shell\n\n    # create and enter an empty directory of your choice\n    mkdir leprikon && cd leprikon\n\n    # create and activate virtual environment\n    virtualenv env\n    . env/bin/activate\n\n    # install leprikon with all the requirements\n    pip install leprikon\n\n    # create database\n    leprikon migrate\n\n    # create admin user\n    leprikon createsuperuser\n\n    # run development server\n    ./manage.py runserver\n',
    'author': 'Jakub Dorňák',
    'author_email': 'jakub.dornak@misli.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://leprikon.cz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
