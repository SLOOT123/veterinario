web: gunicorn core.wsgi:application \
     --chdir . \
     --bind 0.0.0.0:$PORT \
     --workers 3 \
     --log-level info \
     --access-logfile - \
     --error-logfile -
