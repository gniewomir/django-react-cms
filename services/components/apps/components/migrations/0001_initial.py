# Generated by Django 2.0.6 on 2018-09-09 13:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('children', models.ManyToManyField(blank=True, help_text='Component types that are allowed to be children of this component.', to='components.ComponentInstance')),
            ],
            options={
                'verbose_name': 'Component instance',
                'verbose_name_plural': 'Component instances',
            },
        ),
        migrations.CreateModel(
            name='ComponentType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('react_name', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=120)),
                ('allowed_children_types', models.ManyToManyField(blank=True, help_text='Component types that are allowed to be children of this component', to='components.ComponentType')),
            ],
            options={
                'verbose_name': 'Component type',
                'verbose_name_plural': 'Component type',
            },
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('root_component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='components.ComponentInstance')),
            ],
            options={
                'verbose_name': 'Scene',
                'verbose_name_plural': 'Scenes',
            },
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.ComponentType'),
        ),
    ]