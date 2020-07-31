import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200731_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True,default=datetime.datetime(2020, 11, 1, 7, 15, 12, 655838)),
            preserve_default=False,
        ),
    ]
