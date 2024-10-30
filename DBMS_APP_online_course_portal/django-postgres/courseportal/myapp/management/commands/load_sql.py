from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Loads SQL script into the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            with open('myapp/migrations/migrations.sql', 'r') as sql_file:
                sql_statements = sql_file.read()
                cursor.execute(sql_statements)
                self.stdout.write(self.style.SUCCESS('SQL script executed successfully'))
