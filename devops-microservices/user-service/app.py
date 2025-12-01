from flask import Flask, jsonify, make_response

app = Flask(__name__)
PORT = 5001

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return make_response(jsonify({'status': 'OK', 'service': 'User Service'}), 200)

@app.route('/users/<user_id>', methods=['GET'])
def get_user_details(user_id):
    """Returns details for a specific user ID."""
    
    # In a real app, this would query a database.
    user_details = {
        "id": user_id,
        "name": "Alice Johnson",
        "age": 30,
        "city": "Seattle",
        "last_login": "2025-10-27T10:00:00Z"
    }
    return make_response(jsonify(user_details), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)