import os
import logging
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

logging.getLogger('bonnie-flask').info("Serving on port 8080...")
app.run(host='0.0.0.0', port=8080, debug=True)
