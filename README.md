# Bitvill-Contacts

## API Endpoints

### Users

* api/register/ - (registers users)
* api/login/ - (logs in users)
* api/logout/ - (logs out users)
* api/change-password/ - (change users password)
* api/me/ - (view users information)

### Contacts

* / - (view all todos)
* id/ - (view/edit/update/delete single todo)


## How to use

### Clone repo

    Clone repository - git clone https://github.com/blackxavier/Bitvill-Todo.git

### Create a virtual environment and install dependencies

    Create a virtual environment - virtualenv env
    Install requirements - pip install -r requirements.txt

### Make migartions and create super user

    Make migrations - py manage.py makemigrations
    Migrate - py manage.py migrate
    Create superuser - py manage.py createsuperuser
    Launch server - py manage.py runserver 
