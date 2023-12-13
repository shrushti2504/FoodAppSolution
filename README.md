# FoodApp


  ### Technology used :
  ```sh
  Django REST Framework
```
## setup
  ```sh
      first,clone your repository :
      git clone git@github.com:shrushti2504/FoodAppSolution.git
```
## Installation
```sh
pip install djangorestframework
pip install dj_rest_auth
```
 open terminal to create project ,
  ```sh
  django-admin startproject <project-name>
  cd <project-name>
  python3 manage.py startapp <app-name>
  ```
 Create models as per your requirements and run following commands ,
 ```sh
    python3 manage.py makemigrations
    python3 manage.py migrate
 ```
## Run your project :
once you complete your code , run the project using ``` python3 manage.py runserver ```

## TestCases :
## test your web application :
once you run the project with `python3 manage.py runserver` write test cases to ensure that your project is worked as expected.
The purpose of a test case is to determine if different features within a system are performing as expected and to confirm that the system satisfies all related standards, guidelines and customer requirements.
Write your test cases in ```tests.py``` file in your django project.
To run test cases , open terminal and write below command :
```sh
python3 manage.py test <app-name>
```

## create .env file :
.env file is a convenient way to store environment-specific variables, such as API keys passwords, in a simple text file. This enables you to manage sensitive informations.
.env file is used to manage your sensitive credentials from other files.
create ```.env``` file in the application's root directory .
Apply all sensitive credenticals from ```settings.py``` into ```.env``` file.

in settings.py add and change following code.
```sh
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG =os.getenv('DEBUG')
```

In .env file add the following code.
```sh
SECRET_KEY=your-secret-key
DEBUG=True
```
copy your secret key and place it instead of 'your-secret-key'.