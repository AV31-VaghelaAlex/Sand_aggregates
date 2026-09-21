"""
sand_aggregates package.
Includes Python 3.14 compatibility patch for Django 4.2 template context copying.
"""

def _apply_python314_patches():
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

_apply_python314_patches()
