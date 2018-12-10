heroku create gow-ui --region eu
git push heroku master

heroku run python manage.py makemigrations
