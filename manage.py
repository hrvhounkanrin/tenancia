import os
import sys
from setup import main as project_setup_main

if __name__ == "__main__":
    project_setup_main()
    os.environ["DJANGO_SETTINGS_MODULE"] = "meslimmo.settings"
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django

            print(f"runing django {django.VERSION}")
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
