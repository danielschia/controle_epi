#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'controle_epi.settings')
    try:
        from django.core.management import execute_from_command_line
        # If running the development server, run the bootstrap command first so
        # default superuser and test gerentes are created at server start.
        # We do this only when the 'runserver' command is used to avoid surprising
        # behavior on other management commands.
        if 'runserver' in sys.argv:
            try:
                import django
                django.setup()
                from django.core.management import call_command
                call_command('bootstrap_initial')
            except Exception:
                # If bootstrap fails (DB not ready etc.), continue and let Django handle errors.
                pass
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
