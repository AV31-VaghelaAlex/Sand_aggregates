from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
    verbose_name = 'Sand & Aggregates Management'

    def ready(self):
        # Python 3.14 compatibility patch for Django 4.2 template context copying in admin
        try:
            from django.template import context
            def _patched_base_context_copy(self):
                duplicate = object.__new__(self.__class__)
                duplicate.__dict__.update(self.__dict__)
                duplicate.dicts = self.dicts[:]
                return duplicate

            context.BaseContext.__copy__ = _patched_base_context_copy
        except Exception:
            pass
