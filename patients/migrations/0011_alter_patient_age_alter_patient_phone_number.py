# Generated by Django 5.0.1 on 2024-02-14 22:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0010_alter_patient_age_alter_patient_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="age",
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name="patient",
            name="phone_number",
            field=models.PositiveIntegerField(),
        ),
    ]