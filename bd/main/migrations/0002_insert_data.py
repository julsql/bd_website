# Generated by Django 4.2.16 on 2024-12-15 14:41

from django.db import migrations

from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from main.core.update_database.update_database_service import UpdateDatabaseService


def insert_initial_data(apps, schema_editor) -> None:
    sheet_repository = SheetConnexion()
    database_repository = DatabaseConnexion()
    service = UpdateDatabaseService(sheet_repository, database_repository)
    service.main()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_initial_data)
    ]
