# Generated by Django 5.1.1 on 2024-09-07 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_inscrito_numero_inscricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='controle',
            name='vagas_disponiveis',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 7, 3, 0, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
