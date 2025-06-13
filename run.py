# run.py
from app import create_app
import os
app = create_app()

port = int(os.environ.get("PORT", 5000))  # default to 5000 if PORT is not set

if __name__ == '__main__':
    # app.run(debug=True,port=3001)
    app.run(host='0.0.0.0', port=port)
