from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Create default admin and student users'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                role='admin',
                email='admin@letran.edu.ph'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            self.stdout.write('Admin user already exists')

        if not User.objects.filter(username='student').exists():
            User.objects.create_user(
                username='student',
                password='student123',
                role='student',
                email='student@letran.edu.ph'
            )
            self.stdout.write(self.style.SUCCESS('Student user created'))
        else:
            self.stdout.write('Student user already exists')