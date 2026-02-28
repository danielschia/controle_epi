"""Populate missing Gerente.email values from linked User.email or generate unique placeholder.

This migration is a data migration that runs before we make the DB column non-nullable.
"""
from django.db import migrations


def populate_emails(apps, schema_editor):
    Gerente = apps.get_model('epi_admin', 'Gerente')
    User = apps.get_model('auth', 'User')

    for g in Gerente.objects.all():
        if g.email:
            continue

        # prefer linked user email if available
        assigned = None
        try:
            if g.user_id:
                user = User.objects.filter(pk=g.user_id).first()
                if user and user.email:
                    assigned = user.email.lower()
        except Exception:
            assigned = None

        if not assigned:
            base = (f"{getattr(g, 'nome', '')}.{getattr(g, 'sobrenome', '')}") or f"gerente{g.pk}"
            base = ''.join(c for c in base.lower() if c.isalnum() or c == '.')
            candidate = f"{base}@example.local"
            suffix = 1
            # ensure candidate uniqueness across Gerente.email and User.email
            while Gerente.objects.filter(email=candidate).exists() or User.objects.filter(email=candidate).exists():
                candidate = f"{base}{suffix}@example.local"
                suffix += 1
            assigned = candidate

        # assign and save
        g.email = assigned
        g.save()


class Migration(migrations.Migration):

    dependencies = [
        ('epi_admin', '0002_gerente_email'),
    ]

    operations = [
        migrations.RunPython(populate_emails, reverse_code=migrations.RunPython.noop),
    ]
