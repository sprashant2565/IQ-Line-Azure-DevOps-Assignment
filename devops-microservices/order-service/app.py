from flask import Flask, jsonify, make_response

app = Flask(__name__)
PORT = 5002

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return make_response(jsonify({'status': 'OK', 'service': 'Order Service'}), 200)

@app.route('/orders/user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Returns a list of orders for a specific user ID."""
    
    # In a real app, this would query a database.
    order_list = [
        {"order_id": "ORD001", "user_id": user_id, "item_count": 2, "total_usd": 1200.00, "status": "Shipped"},
        {"order_id": "ORD002", "user_id": user_id, "item_count": 1, "total_usd": 15.50, "status": "Pending"}
    ]
    
    return make_response(jsonify(order_list), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)