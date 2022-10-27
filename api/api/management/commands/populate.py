from django.core.management.base import BaseCommand

from profiles.populate import populate as populate_profiles
from sso.populate import populate as populate_sso


class Command(BaseCommand):
    help = "Populate database with default objects"

    def add_arguments(self, parser):
        parser.add_argument(
            '-q', '--quiet', action='store_true', help='No verbosity')

    def handle(self, *args, **options):
        # quiet = options.get("quiet", False)
        populate_sso()
        populate_profiles()
