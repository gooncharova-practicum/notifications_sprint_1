from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL('CREATE SCHEMA IF NOT EXISTS notify;'),
    ]
