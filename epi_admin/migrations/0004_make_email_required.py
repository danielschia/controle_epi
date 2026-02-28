"""Make Gerente.email non-nullable / required at the DB level.

This should run after a data migration that populated missing values.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epi_admin', '0003_populate_gerente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gerente',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
