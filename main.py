from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import json
from datetime import datetime
import uvicorn
from typing import Any, Dict, Optional

app = FastAPI(title="Sample API Debug Server", version="1.0.0")

@app.api_route('/api/debug', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def debug_request(request: Request):
    """
    Debug endpoint that prints and returns all request information
    """
    print("\n" + "="*50)
    print(f"Request received at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Get request body
    body = await request.body()
    
    # Try to parse JSON
    json_data = None
    try:
        if body and request.headers.get("content-type", "").startswith("application/json"):
            json_data = json.loads(body.decode('utf-8'))
    except:
        pass
    
    # Print request method and URL
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Path: {request.url.path}")
    print(f"Query String: {request.url.query}")
    
    # Print all headers
    print("\nHEADERS:")
    print("-" * 20)
    for header_name, header_value in request.headers.items():
        print(f"{header_name}: {header_value}")
    
    # Print query parameters
    print("\nQUERY PARAMETERS:")
    print("-" * 20)
    if request.query_params:
        for key, value in request.query_params.items():
            print(f"{key}: {value}")
    else:
        print("No query parameters")
    
    # Print form data (for form submissions)
    print("\nFORM DATA:")
    print("-" * 20)
    form_data = {}
    if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
        try:
            form = await request.form()
            form_data = dict(form)
            for key, value in form_data.items():
                print(f"{key}: {value}")
        except:
            print("Error parsing form data")
    else:
        print("No form data")
    
    # Print JSON payload (if any)
    print("\nJSON PAYLOAD:")
    print("-" * 20)
    if json_data:
        print(json.dumps(json_data, indent=2))
    else:
        print("No JSON payload")
    
    # Print raw data
    print("\nRAW DATA:")
    print("-" * 20)
    if body:
        print(body.decode('utf-8', errors='ignore'))
    else:
        print("No raw data")
    
    print("="*50)
    
    # Prepare response data
    response_data = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_string": request.url.query,
        "headers": dict(request.headers),
        "query_parameters": dict(request.query_params),
        "form_data": form_data,
        "json_payload": json_data,
        "raw_data": body.decode('utf-8', errors='ignore') if body else "",
        "content_type": request.headers.get("content-type"),
        "content_length": len(body) if body else 0,
        "client_host": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
    }
    
    return JSONResponse({
        "message": "Request received and logged successfully",
        "request_info": response_data
    })

@app.get('/getjwt')
async def get_jwt(x_jwt_assertion: str = Header(None)):
    """
    Endpoint to retrieve JWT token
    """
    # Simulate JWT token retrieval
    return JSONResponse({"jwt": x_jwt_assertion})

@app.get('/')
async def home(x_jwt_assertion: str = Header(None)):
    """
    Home endpoint with usage instructions
    """
    print(f"JWT Assertion Header: {x_jwt_assertion}")
    return JSONResponse({
        "message": "Sample API Debug Server",
        "description": "This API logs all incoming request details",
        "endpoints": {
            "/": "This help message",
            "/api/debug": "Debug endpoint that logs all request information"
        },
        "x-jwt-assertion": x_jwt_assertion,
        "usage": {
            "GET": "curl http://localhost:8005/api/debug",
            "POST_JSON": "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' http://localhost:8005/api/debug",
            "POST_FORM": "curl -X POST -d 'name=John&age=30' http://localhost:8005/api/debug",
            "WITH_HEADERS": "curl -H 'X-Custom-Header: custom-value' -H 'Authorization: Bearer token123' http://localhost:8005/api/debug"
        }
    })

@app.get('/health')
async def health_check():
    """
    Health check endpoint
    """
    return JSONResponse({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting Sample API Debug Server...")
    print("Available endpoints:")
    print("  GET  /           - Home page with usage instructions")
    print("  *    /api/debug  - Debug endpoint (accepts all HTTP methods)")
    print("  GET  /health     - Health check")
    print("\nServer will start on http://localhost:8005")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8005)
