python manage.py makemigrations
python manage.py sqlmigrate ui 0001_initial
python manage.py migrate

python manage.py loaddata user

python manage.py loaddata init
python manage.py loaddata test/testWorld
python manage.py loaddata test/testUnits

