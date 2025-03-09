from flask import Flask, request, redirect, jsonify, make_response, render_template
from db import db, URL
from utils import get_client_id, generate_short_code
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///url.db'
with app.app_context():
    db.init_app(app)  # Initialize the app with the database
    db.create_all()   # Create the database tables

BASE_URL = "http://127.0.0.1:5000/"
request_counts = {}
REQUEST_LIMIT = 5  # Max requests per day per IP + agent

@app.route("/shorten", methods=["POST"])
def shorten_url():
    # identify user
    client_id = get_client_id()
    today = datetime.utcnow().date()
    
    # check if user reached the POST request limit for today
    if client_id in request_counts and request_counts[client_id].get(today, {}).get("post_request_count", 0) >= REQUEST_LIMIT:
        return redirect("https://httpbin.org/delay/5")
    
    request_counts.setdefault(client_id, {}).setdefault(today, {"post_request_count": 0})
    
    try:
        data = request.get_json()
        original_url = data.get("url")
        
        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        
        request_counts[client_id][today]["post_request_count"] += 1
    
        return make_response(jsonify({"short_url": BASE_URL + short_code}))
    except Exception:
        return jsonify({"error": "An error occurred. Please try again."}), 500

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404
    
    return redirect(url_entry.original_url)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)