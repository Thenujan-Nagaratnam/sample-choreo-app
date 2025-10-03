from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/api/debug', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def debug_request():
    """
    Debug endpoint that prints and returns all request information
    """
    print("\n" + "="*50)
    print(f"Request received at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Print request method and URL
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Path: {request.path}")
    print(f"Query String: {request.query_string.decode('utf-8')}")
    
    # Print all headers
    print("\nHEADERS:")
    print("-" * 20)
    for header_name, header_value in request.headers:
        print(f"{header_name}: {header_value}")
    
    # Print query parameters
    print("\nQUERY PARAMETERS:")
    print("-" * 20)
    if request.args:
        for key, value in request.args.items():
            print(f"{key}: {value}")
    else:
        print("No query parameters")
    
    # Print form data (if any)
    print("\nFORM DATA:")
    print("-" * 20)
    if request.form:
        for key, value in request.form.items():
            print(f"{key}: {value}")
    else:
        print("No form data")
    
    # Print JSON payload (if any)
    print("\nJSON PAYLOAD:")
    print("-" * 20)
    try:
        if request.is_json and request.get_json():
            json_data = request.get_json()
            print(json.dumps(json_data, indent=2))
        else:
            print("No JSON payload")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
    
    # Print raw data
    print("\nRAW DATA:")
    print("-" * 20)
    raw_data = request.get_data(as_text=True)
    if raw_data:
        print(raw_data)
    else:
        print("No raw data")
    
    print("="*50)
    
    # Prepare response data
    response_data = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "url": request.url,
        "path": request.path,
        "query_string": request.query_string.decode('utf-8'),
        "headers": dict(request.headers),
        "query_parameters": dict(request.args),
        "form_data": dict(request.form),
        "json_payload": request.get_json() if request.is_json else None,
        "raw_data": request.get_data(as_text=True),
        "content_type": request.content_type,
        "content_length": request.content_length,
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent.string if request.user_agent else None
    }
    
    return jsonify({
        "message": "Request received and logged successfully",
        "request_info": response_data
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with usage instructions
    """
    return jsonify({
        "message": "Sample API Debug Server",
        "description": "This API logs all incoming request details",
        "endpoints": {
            "/": "This help message",
            "/api/debug": "Debug endpoint that logs all request information"
        },
        "usage": {
            "GET": "curl http://localhost:8005/api/debug",
            "POST_JSON": "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' http://localhost:8005/api/debug",
            "POST_FORM": "curl -X POST -d 'name=John&age=30' http://localhost:8005/api/debug",
            "WITH_HEADERS": "curl -H 'X-Custom-Header: custom-value' -H 'Authorization: Bearer token123' http://localhost:8005/api/debug"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    print("Starting Sample API Debug Server...")
    print("Available endpoints:")
    print("  GET  /           - Home page with usage instructions")
    print("  *    /api/debug  - Debug endpoint (accepts all HTTP methods)")
    print("  GET  /health     - Health check")
    print("\nServer will start on http://localhost:8005")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=8005)
