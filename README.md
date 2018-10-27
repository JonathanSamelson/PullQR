# PullQR


Computer Science students at UCLouvain have a sweater with a QRCode.

PullQR is a website linking the QRCode and the students

demo: www.sinfstudent.be

# Get started (how to run it locally ?)
Require python3 and pip ! 


- Clone it

```
git clone https://github.com/fdardenne
```

- Modify email settings in PullQR/settings.py

```
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'passwordExample'
EMAIL_PORT = 587
```

- Install the requirements
```
pip install -r requirements.txt
```

- Create the database

```
python manage.py makemigrations
python manage.py migrate
```
- Collect the static files

```
python manage.py collectstatic
```

- Create a superuser

```
python manage.py createsuperuser
```

- Run it

```
python manage.py runserver
```

# Contribute

Do not hesitate to contribute !
Fork this repository and pull request your change ! 


