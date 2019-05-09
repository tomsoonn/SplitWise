from flask import Flask

from splitwise import configLogger

configLogger()
app = Flask(__name__)

# noinspection PyUnresolvedReferences
from splitwise.server import routes