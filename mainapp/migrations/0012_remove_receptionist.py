from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_patient'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Receptionist',
        ),
    ]
