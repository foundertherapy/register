from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.core import cache


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_cache_name = 'default'
        old_cache_name = 'insecure'
        old_key_prefix = 'register'
        new_prefix = 'register:secure'
        delete_old_keys = False

        old_cache = cache.caches[old_cache_name]
        new_cache = cache.caches[new_cache_name]

        # Use low level api to access full key name
        existing_keys = old_cache.client.get_client().keys('{}*'.format(old_key_prefix))
        for key in existing_keys:
            if new_prefix not in key:
                actual_key = old_cache.client.reverse_key(key)
                unencrypted_val = old_cache.get(actual_key)
                if new_cache.set(actual_key, unencrypted_val):
                    if delete_old_keys:
                        old_cache.delete(actual_key)
