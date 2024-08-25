##### Create a virtual environment inside your project
```python3 -m venv .venv```
```source .venv/bin/activate```

##### Upgrade & Install the dependency
Python Version required: 3.12
```python3 -m pip install --upgrade pip```
```pip install -r requirements.txt```

##### Install Redis for MAC
```brew install redis```
```brew services start redis``` 

To stop the redis service running in background: ```brew services stop redis```

###### For other platform [Install redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

###### To run the server
```fastapi dev app/main.py``` 
OR
```fastapi run app/main.py``` 
