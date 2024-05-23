# Django Installation

<aside>
💡 **Django Tip: Django** is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

**_[More Details](https://www.djangoproject.com/)_**

</aside>

# Installation Django

---

- To install node on your machine go to [\*\*Django](https://docs.djangoproject.com/en/5.0/intro/install/)\*\* official page and install.
- At first, make sure python is available in system. To check, open cmd and type **`python -V`**

# How to Install this Django project

### **For Windows**

- Setup PowerShell to allow execution scripts

```powershell
Set-ExecutionPolicy Unrestricted
```

- Verify Installation

```powershell
python -V
```

- Install Virtual Environment

```powershell
pip install virtualenv
```

- Now create a project folder such as `**Djangoproject**`

```powershell
mk dir Djangoproject
```

### Project

- Now, inside the project folder create virtual env

```powershell
python -m venv venv
```

- Move to the virtual env

```powershell
cd .\venv\
```

- Activate the scripts

```powershell
.\Scripts\activate
```

- Install Django for the project folder

```powershell
pip insatll Django
```

- Make the Django Project called `**ourproject**`

```powershell
django-admin.exe startproject ourproject
```

- Now if we move inside **`ourproject` we can there will be another folder `ourproject`** Now, we will rename our root **`ourproject`** folder called **`src`** and move into the **`src`** folder.

```powershell
cd .\src\
```

- Clone the project

```powershell
git clone https://github.com/Limon00001/django-inventory-project.git
```

- Rename the cloned project folder `src` and replace it with the previous `src` folder

<!-- ```powershell
git clone https://github.com/Limon00001/django-inventory-project.git
``` -->

- Set up the default database

```powershell
python.exe .\manage.py migrate
```

- Create user for admin panel

```powershell
python.exe .\manage.py createsuperuser
```

- Set up completed! Now run the server

```powershell
python.exe .\manage.py runserver
```

- Now we need to create an Django app called **`ourapp`**

```powershell
python .\manage.py startapp ourapp
```

- And inside the **`settings.py`** put our app name under the **INSTALLED_APPS** array

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App Name
    'ourapp'
]
```

---
