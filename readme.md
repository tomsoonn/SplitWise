## SplitWise

flask server:
```
FLASK_APP = splitwise/server/app.py
FLASK_ENV = development
FLASK_DEBUG = 1
python -m flask run
```

setting mongo store location:
```
mongod --dbpath <custom_path>
```
database connection:
```
mongodb://localhost:27017/SplitwiseDatabase
```

desktop application:
```
python splitwise/desktop_starter.py
```
requirements:
pyqt5

recognise:
```
Google API key needs to be given in splitwise.recognise.config.py:
  GOOGLE_API_KEY = 'YOUR_API_KEY'
```
