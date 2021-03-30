from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class EtrackConfig(AppConfig):
    name = 'etrack'

class MyAdminConfig(AdminConfig):
    default_site = 'etrack.admin.MyAdminSite'

