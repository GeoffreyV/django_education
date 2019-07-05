rm -rf db.sqlite3
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser
sqlite3 db.sqlite3 '.read data/init.sql'
