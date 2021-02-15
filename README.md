# RZBlog
Personal blog built with Django

To get started using it:
1. Clone this repository

2. Create a virtual environment
```
python -m venv <env-name>
```
  
3. Install requirements
```
python -m pip install -r requirements.txt
```

4. Make migrations
```
python manage.py makemigrations
```

5. Migrate them to the database
```
python manage.py migrate
```

6. Create an admin (Optional)
```
python manage.py createsuperuser
```
