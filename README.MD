# Test task for Traffic Light 

A test assignment, the requirements of which are as follows:
- There are department and employee models
- a department has a name and can be a child of another department
- an employee has a name, acceptance date, salary, position, department
- the test database contains 50k employees and necessary departments
- all of this is displayed in the tree form on the main page of the launched
    project
- django-admin is configured


## Installation and launch

! The project was developed and tested on Python3.11, not tested on versions
below.

To start, you need to get the code, install the necessary libraries, apply the
migrations, fill the database and run the project. Here are the steps that need
to be done (it is expected that Linux is used):

```shell
git clone https://github.com/tetelevm/tl_test_task
cd tl_test_task
python3.11 -m venv env
. ./env/bin/activate
pip3 install -f requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py filldata
python3 manage.py runserver
# go to 127.0.0.1:8000
```
