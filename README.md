# Quizzing API

Quizzing is a web application where users can test their knowledge with various quizes submites by the comunity.


## 🛠️ Tecnologies utilizied
- [Python](https://www.python.org)
- [Django rest framework](https://www.django-rest-framework.org)
- [SQLite database](https://www.sqlite.org)
- [JSON Web Token](https://jwt.io)


## ⭐ Features
- Users can create their own quizes.
- Quizes have their total amount of times they have been completed.
- Users can see their quizes completions and best scores.
- Users can delete the quizes they created.
- Login/register functionality.
- JWT based authentication.
- Password recovery with email functionality.
- Users can change their password in-app

## 📚 What did I learned
This project helped me to learn Django rest framework and development of restfull API's. Also, I learned about JWT as a better way to manage users authentication.

---

## Enviroment variables
Before deploying the project, reate an ```.env``` file in the root of the proyect with the following variables:

```
SECRET_KEY (the secret key used by django)
DEBUG (set it to True)
```

By default, I'm showing the email recovery message for the password in the console. If you using something like mailtrap to send the emails, add this variables:
```
EMAIL_USER         both provided by the smtp service
EMAIL_PASSWORD
```
And change the ```USING_MAILTRAP``` variable located in ```settings.py``` to ```True```

---

## 🔩 Deploymnet


```
pip install requirements.txt
```

On the root directory
```
python manage.py makemigrations
python manage.py migrate
```

After that you need to create a superuser (admin user)
```
python manage.py createsuperuser
```
Finally:
```python manage.py runserver```

Visit ```http://127.0.0.1:8000/api/schema/docs/``` for the API documentation