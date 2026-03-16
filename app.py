from flask import Flask
from pymongo import MongoClient
import os
app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.flasktest

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/test-db")
def test_db():
    db.test_collection.insert_one({"message": "Hello, World!"})
    doc = db.test_collection.find_one()
    return f"DB connected. Found: {doc['message']}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)