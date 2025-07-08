web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

     --chdir . \
     --bind 0.0.0.0:$PORT \
     --workers 3 \
     --log-level info \
     --access-logfile - \
     --error-logfile -
