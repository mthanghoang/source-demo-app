from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId  # Thêm import này
import uuid

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=['GET', 'POST', 'DELETE', 'OPTIONS'], allow_headers=['Content-Type'])

client = MongoClient('mongo-service', 27017)
db = client['attendees_db']
collection = db['attendees']

# Helper hàm chuyển đổi ObjectId thành string
def serialize_attendee(attendee):
    return {
        "id": str(attendee["_id"]),  # trả _id dưới dạng string ở trường "id"
        "name": attendee.get("name"),
        "school": attendee.get("school")
    }

@app.route('/api/attendees', methods=['GET', 'POST', 'OPTIONS'])
def attendees():
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        data = list(collection.find())
        serialized = [serialize_attendee(att) for att in data]
        return jsonify(serialized)
    elif request.method == 'POST':
        attendee = request.json
        if not attendee or not all(k in attendee for k in ("name", "school")):
            return jsonify({"error": "Invalid data"}), 400
        # Không cần tạo id thủ công, MongoDB tự tạo _id
        collection.insert_one(attendee)
        return jsonify({"message": "Attendee added"}), 201

@app.route('/api/attendees/<id>', methods=['DELETE', 'OPTIONS'])
def delete_attendee(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        obj_id = ObjectId(id)
    except Exception:
        return jsonify({"error": "Invalid id format"}), 400
    result = collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Attendee not found"}), 404
    return jsonify({"message": "Attendee deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
