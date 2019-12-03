del -r ./*/migrations/*0*
del -r ./*/migrations/__pycache__/
del -r ./*/__pycache__/

python.exe ./manage.py makemigrations
python.exe ./manage.py migrate

python.exe ./manage.py createsuperuser