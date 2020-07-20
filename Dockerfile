CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mysite.wsgi:application"]
