# Generated by Django 4.0.3 on 2022-05-09 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0005_atendimento_anotacoes_ccurador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atendimento',
            old_name='anotacoes_ccurador',
            new_name='anotacoes_curador',
        ),
    ]
