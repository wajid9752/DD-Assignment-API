Note :This configuration is only for Windows users.
# Step 1 : Clone the repository first

```
git clone https://github.com/wajid9752/DD-Assignment-API.git
```


# Step 2 : Install and Create a env.


```
pip install virtualenv 
```

```
virtualenv project_env
```

# Step 3: Activate the Env.

```
project_env\Scripts\activate
```

# Step 4 : Install the requirements using requirements.txt file

```
pip install -r requirements.txt
```

# step 5: Migrate the db 

```
python manage.py migrate
```

# Step 6: Create the superuser
In this project, Superuser will behave as admin, so you can login with superuser credentials.
Note : You can  create a user only using these domains ['drone.com','drone.in','drone.co','drone.org','drone.tech']
like : user@drone.com , user@drone.in
```
python manage.py createsuperuser
```

# step 6 : Run the server now 
```
python manage.py runserver
```