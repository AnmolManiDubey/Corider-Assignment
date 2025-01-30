from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Get MongoDB URI from environment variable
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI not set in .env file")

# MongoDB connection
client = MongoClient(mongo_uri)
db = client['user_database']
users_collection = db['users']

# Helper function to convert MongoDB document to JSON
def user_to_json(user):
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user

@app.route('/')
def index():
    return redirect(url_for('get_users'))

# GET /users - Returns a list of all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    return render_template('users.html', users=users)

# GET /users/<id> - Returns the user with the specified ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(f"Received ID: {id}")  # Debug statement
    try:
        if not ObjectId.is_valid(id):
            abort(400, description="Invalid user ID format")

        user = users_collection.find_one({'_id': ObjectId(id)})
        if user:
            return render_template('user_detail.html', user=user_to_json(user))
        else:
            abort(404, description="User not found")
    except InvalidId:
        abort(400, description="Invalid user ID")

# POST /users - Creates a new user with the specified data
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.form.to_dict()  # Convert ImmutableMultiDict to a regular dictionary
    if not user_data or not all(key in user_data for key in ['name', 'email', 'password']):
        abort(400, description="Missing required fields (name, email, password)")

    # Check if email already exists
    if users_collection.find_one({'email': user_data['email']}):
        abort(409, description="Email already exists")

    user_id = users_collection.insert_one(user_data).inserted_id
    return redirect(url_for('get_users'))

# PUT /users/<id> - Updates the user with the specified ID with the new data
@app.route('/users/<id>', methods=['POST'])
def update_user(id):
    user_data = request.form.to_dict()  # Convert ImmutableMultiDict to a regular dictionary
    if not user_data:
        abort(400, description="No data provided")

    try:
        result = users_collection.update_one({'_id': ObjectId(id)}, {'$set': user_data})
        if result.matched_count == 0:
            abort(404, description="User not found")
        return redirect(url_for('get_users'))
    except Exception as e:
        abort(400, description="Invalid user ID")

# DELETE /users/<id> - Deletes the user with the specified ID
@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    try:
        result = users_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, description="User not found")
        return redirect(url_for('get_users'))
    except Exception as e:
        abort(400, description="Invalid user ID")

# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description)}), 400

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error.description)}), 404

# Error handler for 409 Conflict
@app.errorhandler(409)
def conflict(error):
    return jsonify({"error": str(error.description)}), 409

if __name__ == '__main__':
    app.run(port=8080, debug=True)