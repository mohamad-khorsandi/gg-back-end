# Green-Garden
This is our project for the software engineering course in University of Isfahan. 2023 | 1401


## Installation

1. Clone the repository to your local machine.

3. Navigate to the project directory.

5. Create a virtual environment for the project:

```
python -m venv env
```
4. Activate the virtual environmen:

- On Windows:
  ```
  env\Scripts\activate
  ```

- On macOS and Linux:
  ```
  source env/bin/activate
  ```
5. Install the project dependencies:

```
pip install -r requirements.txt
```
6. Set up the database:
```
python manage.py makemigrations
python manage.py migrate
```
7. now run it:
```
python manage.py runserver
```
## how to install needed packages?
1 make a virtual environment
```
python -m venv env
```

2 activate it
```
source env/bin/activate
```

3 install packages
```
pip install -r requirements.txt
```

## if you added new package to virtual environment
```
pip freeze > requirements.txt
```
