sed -i 's/STANDALONE: true/STANDALONE: false/' instance/config.yml
sed -i 's/LEVEL_LOG: DEBUG/LEVEL_LOG: INFO/' instance/config.yml
gunicorn wsgi:app --timeout 999999 --workers 2 --pid gunicornpid --bind 0.0.0.0:5000