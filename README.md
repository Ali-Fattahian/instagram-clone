# Instagram Clone Project

### Description

Instagram website clone built with Django.
This project was made to be as close as possible to Instagram website, however a few features are missing that are planned to be added later.

### Features

- Viewers can explore the website but are not allowed to add anything to the website.
- To sign up, users must provide email, password, username and their fullname.
- Users have to validate their email to activate their account. This will automatically creates a profile for them with the information given.
- Users can Edit their profile, add bio, add profile picture, and if they want delete their profile.
- Deleting a profile causes the is_active field to change to False, not allowing them to log in anymore, they can contact the support via email to bring back their account (backup).
- Users can reset their password using the email they have provided.
- Users can create posts, edit and delete them. They can save posts (Bookmark), like them and write comments for them.
- Users can follow each other and receive posts from their following users (home page).
- Users can also search for other users.

### Technologies and libraries used

- Django
- Django-Verify-Email
- Postgres
- psycopg2
- dj-database-url
- Cloudinary
- Django cloudinary storage
- Django white noise
- Pillow
- gunicorn
- python-dotenv

### Possible incoming features
- Chat application
- Stories

### How to run the project

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Ali-Fattahian/instagram-clone
```

Navigate to the root directory
```sh
cd instagram_clone
```

Create a virtual environment to install dependencies in and activate it:

```sh
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Since this project is in production, you have to change settings to dev to work with it, so open settings.py,

Use an online tool like *https://djecrety.ir/*
to get a new secret key for the project.

Set DEBUG=True,

Create a database and set DATABASES settings to the one you created,

either remove cloudinary settings and apps from installed_apps or set the configuration to your own account, at last set the email config to your email.

once you did all of that,

```sh
python manage.py makemigrations
python manage.py migrate
```

To create the tables in your database.


```ssh
python manage.py runserver
```

to run the server.

You can navigate to
`http://localhost:8000/homepage`
to explore the website.

You can navigate to
`http://localhost:8000/`
to create an account

To run the tests,
`python manage.py tests`
