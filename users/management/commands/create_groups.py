from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Создание группы модераторов"""

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Moderators")

        if created:
            self.stdout.write("Группа Moderators создана")
        else:
            self.stdout.write("Группа Moderators уже существует")