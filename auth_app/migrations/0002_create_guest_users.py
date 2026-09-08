from django.contrib.auth.hashers import make_password
from django.db import migrations

GUEST_USERS = [
    {
        "username": "andrey",
        "password": "asdasd",
        "email": "andrey@coderr.example",
        "type": "customer",
    },
    {
        "username": "kevin",
        "password": "asdasd24",
        "email": "kevin@coderr.example",
        "type": "business",
    },
]


def create_guest_users(apps, schema_editor):
    user_model = apps.get_model("auth_app", "CustomUser")
    for guest in GUEST_USERS:
        username = guest["username"]
        password = guest["password"]
        defaults = {
            "email": guest["email"],
            "type": guest["type"],
        }
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults=defaults,
        )
        if created:
            user.password = make_password(password)
            user.save(update_fields=["password"])


def remove_guest_users(apps, schema_editor):
    user_model = apps.get_model("auth_app", "CustomUser")
    user_model.objects.filter(username__in=["andrey", "kevin"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_guest_users, remove_guest_users),
    ]
