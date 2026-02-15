web: python manage.py migrate && python manage.py shell -c "import AuditionForm.create_superuser" && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
