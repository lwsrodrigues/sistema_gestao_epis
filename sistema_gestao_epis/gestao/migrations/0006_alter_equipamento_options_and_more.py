# Generated by Django 5.1.6 on 2025-03-31 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0005_equipamento_alter_colaborador_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipamento',
            options={},
        ),
        migrations.RenameField(
            model_name='equipamento',
            old_name='criado_em',
            new_name='data_cadastro',
        ),
        migrations.RenameField(
            model_name='equipamento',
            old_name='atualizado_em',
            new_name='ultima_atualizacao',
        ),
        migrations.RemoveField(
            model_name='equipamento',
            name='data_aquisicao',
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_fabricacao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='numero_serie',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='quantidade',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='status',
            field=models.CharField(choices=[('Disponível', 'Disponível'), ('Emprestado', 'Emprestado'), ('Manutenção', 'Manutenção')], default='Disponível', max_length=20),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='tipo',
            field=models.CharField(choices=[('Capacete', 'Capacete de Segurança'), ('Luva', 'Luvas de Proteção'), ('Bota', 'Botas de Segurança'), ('Óculos', 'Óculos de Proteção')], max_length=50),
        ),
        migrations.AlterModelTable(
            name='equipamento',
            table='gestao_equipamento',
        ),
    ]
