import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from splitwise.server.app import app
from splitwise.server import routes

if __name__ == '__main__':
    app.run(debug=True)
