from django.apps import AppConfig


class CostcenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'costcenter'

class costcenterConfig(AppConfig):
    name = 'costcenter'

    def ready(self):
        import costcenter.signals  # Asegúrate de que este es el nombre correcto de tu módulo