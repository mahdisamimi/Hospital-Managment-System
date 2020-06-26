# Generated by Django 3.0.7 on 2020-06-21 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='clerk',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('natural_code', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('email', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('natural_code', models.IntegerField()),
                ('msn', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('email', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='hospital',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.IntegerField()),
                ('user_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='reserve',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('reserve_time', models.DateTimeField()),
                ('natural_code', models.IntegerField()),
                ('clerk_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.clerk')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.doctor')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='relation_doctor_hospital',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.doctor')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='relation_doctor_clerk',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('clerk_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.clerk')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.doctor')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='hospital_manager',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='free_time',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('free_time', models.DateTimeField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.doctor')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('natural_code', models.IntegerField()),
                ('request_kind', models.CharField(max_length=255)),
                ('request_txt', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital')),
            ],
        ),
        migrations.AddField(
            model_name='clerk',
            name='hospital_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.hospital'),
        ),
        migrations.AddField(
            model_name='clerk',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HospitalManagementApp.user'),
        ),
    ]