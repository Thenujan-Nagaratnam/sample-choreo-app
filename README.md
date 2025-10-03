# Sample API Debug Server

A simple Flask API that captures and logs all incoming request details including headers, payload, and other metadata.

## Features

- Logs all request headers
- Captures JSON, form data, and raw payloads
- Supports all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Prints detailed request information to console
- Returns structured response with request details

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python main.py
   ```

3. The server will start on `http://localhost:5000`

## Endpoints

- `GET /` - Home page with usage instructions
- `ALL /api/debug` - Debug endpoint that logs all request information
- `GET /health` - Health check endpoint

## Usage Examples

### Basic GET request
```bash
curl http://localhost:5000/api/debug
```

### POST with JSON payload
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30, "city": "New York"}' \
  http://localhost:5000/api/debug
```

### POST with form data
```bash
curl -X POST \
  -d "name=John&age=30&city=New York" \
  http://localhost:5000/api/debug
```

### Request with custom headers
```bash
curl -X GET \
  -H "X-Custom-Header: custom-value" \
  -H "Authorization: Bearer token123" \
  -H "User-Agent: MyApp/1.0" \
  http://localhost:5000/api/debug
```

### PUT request with query parameters
```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"status": "updated"}' \
  "http://localhost:5000/api/debug?id=123&source=api"
```

## What Gets Logged

The API logs the following information to the console:

- Request timestamp
- HTTP method
- Full URL and path
- Query string
- All headers
- Query parameters
- Form data
- JSON payload
- Raw data
- Content type and length
- Remote address
- User agent

## Response

The API returns a JSON response containing:
- Success message
- Complete request information in structured format
- Timestamp of the request