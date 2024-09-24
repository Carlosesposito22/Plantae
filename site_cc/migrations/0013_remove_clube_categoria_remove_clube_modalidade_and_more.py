# Generated by Django 5.1.1 on 2024-09-24 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_cc', '0012_rename_comment_comentario_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clube',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='clube',
            name='modalidade',
        ),
        migrations.RemoveField(
            model_name='clube',
            name='moderador',
        ),
        migrations.RemoveField(
            model_name='membro',
            name='clube',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='clube',
        ),
        migrations.RemoveField(
            model_name='membro',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Avaliacao',
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.DeleteModel(
            name='Modalidade',
        ),
        migrations.DeleteModel(
            name='Clube',
        ),
        migrations.DeleteModel(
            name='Comentario',
        ),
        migrations.DeleteModel(
            name='Membro',
        ),
    ]
