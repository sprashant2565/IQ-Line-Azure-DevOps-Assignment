from flask import Flask, jsonify, make_response
from applicationinsights.requests import WSGIApplication # 1. Import the wrapper
import os # To access environment variables

# Initialize Flask app
app = Flask(__name__)
PORT = 5000

# 2. INSTRUMENTATION: Apply the WSGIApplication wrapper
app.wsgi_app = WSGIApplication(app.wsgi_app) 

# Check for iKey to confirm instrumentation status (optional)
if 'APPINSIGHTS_INSTRUMENTATIONKEY' in os.environ:
    app.logger.info("Application Insights Instrumentation Key found.")
else:
    app.logger.warning("APPINSIGHTS_INSTRUMENTATIONKEY is missing! Telemetry will not be sent.")


@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    app.logger.info("API Gateway Health check successful.") # Custom trace log
    return make_response(jsonify({'status': 'OK', 'service': 'API Gateway'}), 200)

@app.route('/v1/user-orders/<user_id>', methods=['GET'])
def get_user_and_orders(user_id):
    """Aggregates data."""
    
    # 3. Example custom telemetry logging:
    app.logger.info(f"API Gateway: Processing request for user {user_id}")
    
    user_data = {
        "id": user_id,
        "name": "Alice Johnson",
        "source_service": "User Service (Simulated)"
    }
    
    order_data = [
        {"order_id": "ORD001", "product": "Laptop", "status": "Shipped", "source_service": "Order Service (Simulated)"},
        {"order_id": "ORD002", "product": "Mouse", "status": "Pending", "source_service": "Order Service (Simulated)"}
    ]
    
    response_data = {
        "user_info": user_data,
        "recent_orders": order_data
    }
    
    return make_response(jsonify(response_data), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)