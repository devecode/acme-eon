# Generated by Django 3.2.7 on 2021-09-10 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('sales', '0003_ventaproducto_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventaproducto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]