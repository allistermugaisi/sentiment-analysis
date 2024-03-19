from app_backend import app
from flask_cors import CORS

if __name__ == "__main__":
    CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])
    app.run(host="0.0.0.0", port=8080, debug=True)
