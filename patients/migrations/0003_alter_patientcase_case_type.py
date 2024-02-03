# Generated by Django 5.0.1 on 2024-02-03 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0002_alter_patientcase_patient_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientcase",
            name="case_type",
            field=models.CharField(
                choices=[
                    ("Urgent", "Urgent"),
                    ("Surgery", "Surgery"),
                    ("Treatment", "Treatment"),
                ],
                max_length=10,
            ),
        ),
    ]
