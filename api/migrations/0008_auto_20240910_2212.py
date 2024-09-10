from django.db import migrations

def reset_user_id_sequence(apps, schema_editor):
    # For PostgreSQL
    schema_editor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1")

    # Uncomment for MySQL if needed
    # schema_editor.execute("ALTER TABLE auth_user AUTO_INCREMENT = 1")

class Migration(migrations.Migration):

    dependencies = [
        # Add your last migration file here
        ('api', '0007_alter_article_tags'),
    ]

    operations = [
        migrations.RunPython(reset_user_id_sequence),
    ]
