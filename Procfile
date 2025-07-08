web: gunicorn --chdir core core.wsgi:application --bind 0.0.0.0:$PORT

    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --error-logfile - \
    --log-level debug
