##### Create a virtual environment inside your project
Python Version required: 3.12 \
```python3 -m venv .venv``` \
```source .venv/bin/activate```

##### Upgrade & Install the dependency
```python3 -m pip install --upgrade pip``` \
```pip install -r requirements.txt```

##### Install Redis for MAC
```brew install redis``` \
```brew services start redis```

To stop the redis service running in background: ```brew services stop redis```

###### For other platform [Install redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

###### To run the server
```fastapi dev app/main.py``` 
OR
```fastapi run app/main.py```

###### curl command to run the api
```
curl --location 'localhost:8000/scrape/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJuYW1lIjoidGVzdCB1c2VyIHdpdGggbm8gZXhwaXJhdGlvbiIsImlhdCI6MTcyNDYxMjU4OH0.GzwaK_x-pXIpzYYmDDQtmEAIMLLv2uLPMwzW2RgKcxg' \
--data '{
    "url": "https://dentalstall.com/shop/",
    "pages": "2"
}'
```

Image will be stored in local directory ```./images```
Product details will be saved in ```.products.json```

Sample from ```products.json```
```
[
    {
        "url": "https://dentalstall.com/wp-content/uploads/2021/11/GDC-Extraction-Forceps-Lower-Molars-86A-Standard-FX86AS-300x300.jpg",
        "path_to_image": "/Users/adityar/Documents/Personal/web-scraper/images/1 x GDC Extraction Forceps Lower Molars  86 Ergonomic FX86E118.png",
        "product_title": "1 x GDC Extraction Forceps Lower Molars - 86 Ergonomic (FX86E)118",
        "product_price": 850.0
    },
]
```