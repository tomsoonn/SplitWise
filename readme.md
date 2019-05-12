
flask server:
```
FLASK_APP = splitwise/server/app.py
FLASK_ENV = development
FLASK_DEBUG = 1
python -m flask run
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
