from django.apps import AppConfig


class PharmashopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmashop'
    
    def ready(self) -> None:
        from .Scheduler import scheduler
        scheduler.start()
