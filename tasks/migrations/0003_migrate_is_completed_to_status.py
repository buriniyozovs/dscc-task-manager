from django.db import migrations


def set_status_from_is_completed(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.filter(is_completed=True).update(status='completed')
    Task.objects.filter(is_completed=False).update(status='created')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_add_task_status'),
    ]

    operations = [
        migrations.RunPython(set_status_from_is_completed, noop),
    ]
