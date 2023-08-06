from django.core.management.base import BaseCommand
from httpx import Client

from spoof import utils as spoof_utils
from ... import models


class Command(BaseCommand):
    help = 'Test Proxies'

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Target URL for proxies",
        )
        parser.add_argument(
            "--no-proxies",
            action='store_true',
            help="Omit proxies",
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        try:
            if kwargs['no_proxies']:
                with Client() as client:
                    client.get(url)
            else:
                with spoof_utils.SpoofSession(proxy_str=models.Proxy.objects.get_rotating_proxy().url) as client:
                    client.get(url)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
