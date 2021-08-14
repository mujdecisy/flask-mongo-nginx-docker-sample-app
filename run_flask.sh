sed -i 's/STANDALONE: false/STANDALONE: true/' instance/config.yml
sed -i 's/LEVEL_LOG: INFO/LEVEL_LOG: DEBUG/' instance/config.yml
export FLASK_APP=flaskmgnd
export FLASK_ENV=development
flask run