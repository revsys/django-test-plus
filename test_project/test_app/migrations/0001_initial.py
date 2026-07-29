from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Data",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=50)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
