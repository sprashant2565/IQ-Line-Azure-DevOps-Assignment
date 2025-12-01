from flask import Flask, jsonify, make_response
# In a real scenario, you would use 'requests' here to call the User and Order Services.
# Example: response = requests.get('http://user-service:5001/users/1')

app = Flask(__name__)
PORT = 5000

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return make_response(jsonify({'status': 'OK', 'service': 'API Gateway'}), 200)

@app.route('/v1/user-orders/<user_id>', methods=['GET'])
def get_user_and_orders(user_id):
    """
    Simulates calling User Service and Order Service to aggregate data.
    
    NOTE: When deployed to AKS, replace these dummy responses
    with actual service-to-service calls using Kubernetes Service DNS names.
    e.g., requests.get('http://user-service-clusterip/users/1')
    """
    
    # 1. Simulate call to User Service
    user_data = {
        "id": user_id,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "source_service": "User Service (Simulated)"
    }
    
    # 2. Simulate call to Order Service
    order_data = [
        {"order_id": "ORD001", "product": "Laptop", "status": "Shipped", "source_service": "Order Service (Simulated)"},
        {"order_id": "ORD002", "product": "Mouse", "status": "Pending", "source_service": "Order Service (Simulated)"}
    ]
    
    # 3. Aggregate results
    response_data = {
        "user_info": user_data,
        "recent_orders": order_data
    }
    
    return make_response(jsonify(response_data), 200)

if __name__ == '__main__':
    # Use 0.0.0.0 for Docker container
    app.run(host='0.0.0.0', port=PORT, debug=True)